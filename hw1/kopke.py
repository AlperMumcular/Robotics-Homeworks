from robotic import ry
import time
C = ry.Config()
C.addFile(ry.raiPath('../rai-robotModels/objects/kitchen.g'))
C.addFrame('part1.g')

#Part c - State1
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

"""qHome = C.getJointState()
komo = ry.KOMO(C, 1, 1, 0, False)
komo.addObjective(times=[], feature=ry.FS.jointState, frames=[], type=ry.OT.sos, scale=[1e-1], target=qHome);
komo.addObjective([], ry.FS.positionDiff, ['handR', 'item2'], ry.OT.eq, [1e1]);
ret = ry.NLP_Solver(komo.nlp(), verbose=4) .solve()
print(ret)
q = komo.getPath()
print(type(q), len(q))
del komo
C.setJointState(q[0])"""
C.view()
time.sleep(10)
