from robotic import ry
import time
import numpy as np

C = ry.Config()
C.addFile(ry.raiPath('../rai-robotModels/objects/kitchen.g'))
C.addFrame('part1.g')

C.addFrame(name="tray", parent="stove1") \
.setShape(ry.ST.ssBox, size=[.4, .4, .05, .02]) \
.setColor([0,1,0]) \
.setRelativePose('t(0 0 .42) d(135 0 0 1)')

C.addFrame(name="item1", parent="tray") \
.setShape(ry.ST.ssBox, size=[.1, .1, .25, .02]) \
.setRelativePosition([-.1, -.1, .15]) \
.setColor([1,0,0])

C.addFrame(name="item2", parent="tray") \
.setShape(ry.ST.ssBox, size=[.1, .1, .25, .02]) \
.setRelativePosition([.1, .1, .15]) \
.setColor([1,1,0])

C.addFile('robo.g')

F = C.feature(ry.FS.position, ["waist"])
[y,J] = F.eval(C)
print('hand position:', y)
print('Jacobian:', J)
print('Jacobian shape:', J.shape)
input()
