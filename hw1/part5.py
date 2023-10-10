from robotic import ry
import time

C = ry.Config()
C.addFile(ry.raiPath('../rai-robotModels/objects/kitchen.g'))
C.addFile('robot.g')
C.view()
time.sleep(10)