from robotic import ry
import time 
import numpy as np


C = ry.Config()
C.addFile('HW1-two-link.g')

# Provided missing code in the hw file with implementation
target = C.frame("target")
joint_angles = 2 * np.pi * np.random.rand(3)

def forward_kinematics(q):
    q0 = q[0]
    q1 = q[1]
    y = np.sin(q0) + np.sin(q0+q1)
    z = np.cos(q0) + np.cos(q0+q1)
    return np.array([0, y, z])

pos_target = forward_kinematics(joint_angles)
target.setPosition(pos_target)
C.setJointState(joint_angles)
C.view()

q = np.zeros(C.getJointDimension())
C.setJointState(q)
target.setPosition([0,0,0])

time.sleep(15)

