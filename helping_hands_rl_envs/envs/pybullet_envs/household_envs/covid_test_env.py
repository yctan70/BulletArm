import os
import pybullet as pb
import copy
import numpy as np
import numpy.random as npr

import helping_hands_rl_envs
from helping_hands_rl_envs.simulators.pybullet.equipments.box_color import BoxColor
from helping_hands_rl_envs.simulators.pybullet.equipments.rack import Rack
from helping_hands_rl_envs.simulators.pybullet.objects.plate import PLACE_RY_OFFSET, PLACE_Z_OFFSET
from helping_hands_rl_envs.envs.pybullet_envs.pybullet_env import PyBulletEnv
from helping_hands_rl_envs.simulators import constants
from helping_hands_rl_envs.simulators.pybullet.utils import transformations
from helping_hands_rl_envs.simulators.constants import NoValidPositionException
from helping_hands_rl_envs.planners.shelf_bowl_stacking_planner import ShelfBowlStackingPlanner

class CovidTestEnv(PyBulletEnv):
  def __init__(self, config):
    super().__init__(config)
    # self.shelf = Shelf()
    # self.rack = Rack(n=self.num_obj+1, dist=0.05)
    self.object_init_space = np.asarray([[0.3, 0.7],
                                         [-0.4, 0],
                                         [0, 0.40]])
    self.plate_model_id = None
    self.place_offset = None
    self.place_ry_offset = None

    self.box = BoxColor()
    self.box_pos1 = [0.3, 0.12, 0]
    self.box_pos2 = [0.3, 0.03, 0]
    self.box_pos3 = [0.3, -0.045, 0]
    self.box_pos4 = [0.3, -0.12, 0]
    self.new_tube_box_size = [0.12, 0.08, 0.02]
    self.swap_box_size = [0.12, 0.08, 0.05]
    self.santilizing_box_size = [0.12, 0.04, 0.08]
    self.used_tube_box_size = [0.12, 0.08, 0.03]
    # self.box_range = np.array([[self.box_pos[0] - self.box_size[0] / 2, self.box_pos[0] + self.box_size[0] / 2],
    #                            [self.box_pos[1] - self.box_size[1] / 2, self.box_pos[1] + self.box_size[1] / 2]])

  def initialize(self):
    super().initialize()
    self.box.initialize(pos=self.box_pos1, size=self.new_tube_box_size, color=[0.9, 0.9, 1, 1])
    self.box.initialize(pos=self.box_pos2, size=self.swap_box_size, color=[1, 0.5, 0.5, 1])
    self.box.initialize(pos=self.box_pos3, size=self.santilizing_box_size, color=[0.5, 0.5, 0.5, 0.6])
    self.box.initialize(pos=self.box_pos4, size=self.used_tube_box_size, color=[1, 1, 0.5, 1])
    # self.shelf.initialize(pos=[0.6, 0.3, 0])
    # if self.physic_mode == 'slow':
    #   pb.changeDynamics(self.shelf.id, -1, linearDamping=0.04, angularDamping=0.04, restitution=0,
    #                     contactStiffness=3000, contactDamping=100)
    # self.rack.initialize(pos=[0.3, -0.3, 0], rot=transformations.quaternion_from_euler(0, 0, 0), fixed=True)
    # if self.physic_mode == 'slow':
    #   for rack_id in self.rack.ids:
    #     pb.changeDynamics(rack_id, -1, linearDamping=0.04, angularDamping=0.04, restitution=0,
    #                       contactStiffness=3000, contactDamping=100)
    self.robot.gripper_joint_limit = [0, 0.15]
    pass

  def reset(self):
    ''''''
    # self.plate_model_id = np.random.choice([1, 2, 6, 7, 8, 9])
    self.plate_model_id = 0
    self.place_ry_offset = PLACE_RY_OFFSET[self.plate_model_id]
    self.place_offset = PLACE_Z_OFFSET[self.plate_model_id]
    # while True:
    #   self.resetPybulletEnv()
    #   try:
    #     plate_pos_list = self.rack.getObjInitPosList()
    #     for pos in plate_pos_list:
    #       self._generateShapes(constants.PLATE, 1, pos=[pos], rot=[transformations.quaternion_from_euler(0, -np.deg2rad(100), 0)], model_id=self.plate_model_id)
    #   except NoValidPositionException as e:
    #     continue
    #   else:
    #     break
    while True:
      self.resetPybulletEnv()
      try:
        # self._generateShapes(constants.RANDOM_BLOCK, self.num_obj, random_orientation=self.random_orientation,
        #                      pos=[(0.3, 0.12, 0.12)])
        for i in range(5):
          self._generateShapes(constants.TEST_TUBE, random_orientation=self.random_orientation,
                               pos=[(0.3, 0.12, 0.12)])
        for i in range(5):
          self._generateShapes(constants.SWAB, random_orientation=self.random_orientation,
                               pos=[(0.3, 0.03, 0.12)])
      except NoValidPositionException:
        continue
      else:
        break

    return self._getObservation()

  def getPlaceRyOffset(self):
    return PLACE_RY_OFFSET[self.plate_model_id]

  def anyObjectOnTarget1(self):
    for obj in self.objects:
      if self.shelf.isObjectOnTarget1(obj):
        return True
    return False

  def _checkTermination(self):
    return self._checkStack() and self.anyObjectOnTarget1()

  def _getValidOrientation(self, random_orientation):
    if random_orientation:
      orientation = pb.getQuaternionFromEuler([0., 0., np.pi * -(np.random.random_sample() * 0.5 + 0.5)])
    else:
      orientation = pb.getQuaternionFromEuler([0., 0., 0.])
    return orientation
    
  def getValidSpace(self):
    return self.object_init_space

def createShelfPlateStackingEnv(config):
  return ShelfPlateStackingEnv(config)
  

if __name__ == '__main__':
  object_init_space = np.asarray([[0.3, 0.7],
                          [-0.4, 0.4],
                          [0, 0.40]])
  workspace = np.asarray([[0.2, 0.8],
                          [-0.3, 0.3],
                          [0, 0.50]])
  env_config = {'workspace': workspace, 'object_init_space': object_init_space, 'max_steps': 10, 'obs_size': 128,
                'render': True, 'fast_mode': True, 'seed': 0, 'action_sequence': 'pxyzrrr', 'num_objects': 9,
                'random_orientation': True, 'reward_type': 'step_left', 'simulate_grasp': True, 'perfect_grasp': False,
                'robot': 'kuka', 'object_init_space_check': 'point', 'physics_mode': 'slow'}
  planner_config = {'random_orientation': True}

  env = CovidTestEnv(env_config)
  # planner = ShelfBowlStackingPlanner(env, planner_config)
  s, in_hand, obs = env.reset()
  a = 1