from robotic import ry
import time 
import numpy as np


C = ry.Config()
C.addFile('HW1-two-link.g')
C.view()
C.watchFile('HW1-two-link.g')