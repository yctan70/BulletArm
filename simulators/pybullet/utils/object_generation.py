import os

import pybullet as pb
import numpy as np
import numpy.random as npr

import helping_hands_rl_envs
from helping_hands_rl_envs.simulators.pybullet.objects.cube import Cube
from helping_hands_rl_envs.simulators.pybullet.objects.rectangle import Rectangle
from helping_hands_rl_envs.simulators.pybullet.objects.triangle import Triangle

def generateCube(pos, rot, scale):
  ''''''
  return Cube(pos, rot, scale)

def generateBrick(pos, rot, scale):
  root_dir = os.path.dirname(helping_hands_rl_envs.__file__)
  brick_urdf_filepath = os.path.join(root_dir, 'simulators/urdf/object/brick_small.urdf')
  return pb.loadURDF(brick_urdf_filepath, basePosition=pos, baseOrientation=rot, globalScaling=scale)

def generateTriangle(pos, rot, scale):
  root_dir = os.path.dirname(helping_hands_rl_envs.__file__)
  brick_urdf_filepath = os.path.join(root_dir, 'simulators/urdf/object/0.urdf')
  return pb.loadURDF(brick_urdf_filepath, basePosition=pos, baseOrientation=rot, globalScaling=scale)

def generateRoof(pos, rot, scale):
  root_dir = os.path.dirname(helping_hands_rl_envs.__file__)
  roof_urdf_filepath = os.path.join(root_dir, 'simulators/urdf/object/roof.urdf')
  return pb.loadURDF(roof_urdf_filepath, basePosition=pos, baseOrientation=rot, globalScaling=scale)