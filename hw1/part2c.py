from robotic import ry
import time 
import numpy as np

#part2c
def calculate_Jacobian(q):
	q0 = q[0]
	q1 = q[1]
	jacobian_matrix = np.array([[np.cos(q0) + np.cos(q0+q1),np.cos(q0+q1)],[-np.sin(q0) - np.sin(q0+q1),-np.sin(q0+q1)]])
	return jacobian_matrix

joint_angles= [1.95205226, 3.15753276,0]
res = calculate_Jacobian(joint_angles)
print(res)

