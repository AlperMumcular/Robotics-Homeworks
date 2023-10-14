from robotic import ry
import numpy as np
import time
C = ry.Config()
C.addFile(ry.raiPath('../rai-robotModels/objects/kitchen.g'))
C.addFrame('part1.g')
#C.view()

#Part c - State1
target = C.addFrame(name="tray", parent="stove1") 
target.setShape(ry.ST.ssBox, size=[.4, .4, .05, .02]) 
target.setColor([0,1,0]) 
target.setRelativePose('t(0 0 .42) d(135 0 0 1)')

target2 = C.addFrame(name="item1", parent="tray") 
target2.setShape(ry.ST.ssBox, size=[.1, .1, .25, .02]) 
target2.setRelativePosition([-.1, -.1, .15]) 
target2.setColor([1,0,0])

target3 = C.addFrame(name="item2", parent="tray") 
target3.setShape(ry.ST.ssBox, size=[.1, .1, .25, .02]) 
target3.setRelativePosition([.1, .1, .15]) 
target3.setColor([1,1,0])

C.addFile('kopke.g')

def IK(C):
    qHome = C.getJointState()
    komo = ry.KOMO(C, 7, 10, 1, True)
    komo.addControlObjective([], 0, 1e-1)
    komo.addControlObjective([], 1, 1e0)
    komo.addObjective(times=[], feature=ry.FS.jointState, frames=[], type=ry.OT.sos, scale=[1e-1], target=qHome)
    komo.addObjective([], ry.FS.jointState, [], ry.OT.sos, [1e-1], qHome)
    komo.addObjective([3], ry.FS.positionDiff, ['handR', 'item2'], ry.OT.eq, [1e1])
    komo.addObjective([5], ry.FS.positionDiff, ['handR', 'tray'], ry.OT.eq, [1e1])
    komo.addObjective([7], ry.FS.positionDiff, ['handR', 'item1'], ry.OT.eq, [1e1])
    ret = ry.NLP_Solver(komo.nlp(), verbose=4) .solve()
    return komo.getPath()

q = IK(C)

for t in range(q.shape[0]):
    C.setJointState(q[t])
    C.view(False, f'waypoint {t}')
    time.sleep(0.1)
time.sleep(5)
