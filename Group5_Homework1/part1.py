from robotic import ry
import time
C = ry.Config()
C.addFile(ry.raiPath('../rai-robotModels/objects/kitchen.g'))
C.addFrame('part1.g')

#Part a
C.addFrame(name="item1", parent="sink1") \
.setShape(ry.ST.ssBox, size=[.1, .1, .25, .02]) \
.setRelativePosition([-.1, -.1, .52]) \
.setColor([1,0,0])

# Verifying the answer of part a
f = C.frame("item1")
print("position:", f.getPosition())
print("orientation:", f.getQuaternion())

#Part b
C.addFrame(name="item2", parent="sink1") \
.setShape(ry.ST.ssBox, size=[.1, .1, .25, .02]) \
.setRelativePosition([.1, .1, .52]) \
.setColor([1,1,0])

C.addFrame(name="tray", parent="stove1") \
.setShape(ry.ST.ssBox, size=[.2, .2, .05, .02]) \
.setColor([0,1,0]) \
.setRelativePose('t(0 0 .42) d(45 0 0 1)')

C.view()
time.sleep(15)


