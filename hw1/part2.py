from robotic import ry
import time 

C = ry.Config()
C.addFile('HW1-two-link.g')
C.view()
C.watchFile('HW1-two-link.g')
time.sleep(5)
