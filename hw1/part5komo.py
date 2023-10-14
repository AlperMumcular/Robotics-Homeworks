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
pos = target.getPosition()
cen = pos.copy()
C.view()

target2 = C.addFrame(name="item1", parent="tray") 
target2.setShape(ry.ST.ssBox, size=[.1, .1, .25, .02]) 
target2.setRelativePosition([-.1, -.1, .15]) 
target2.setColor([1,0,0])
pos2 = target.getPosition()
cen2 = pos2.copy()
C.view()

target3 = C.addFrame(name="item2", parent="tray") 
target3.setShape(ry.ST.ssBox, size=[.1, .1, .25, .02]) 
target3.setRelativePosition([.1, .1, .15]) 
target3.setColor([1,1,0])
pos3 = target.getPosition()
cen3 = pos3.copy()
C.addFile('kopke.g')

def IK(C,pos):
    qHome = C.getJointState()
    komo = ry.KOMO(C, 1, 1, 0, False)
    komo.addObjective(times=[], feature=ry.FS.jointState, frames=[], type=ry.OT.sos, scale=[1e-1], target=qHome);
    komo.addObjective([], ry.FS.jointState, [], ry.OT.sos, [1e-1], qHome)
    komo.addObjective([], ry.FS.positionDiff, ['handR', 'item2'], ry.OT.eq, [1e1]);
    ret = ry.NLP_Solver(komo.nlp(), verbose=4) .solve()
    return [komo.getPath()[0], ret]

for t in range(20):
   time.sleep(.1)
   pos = cen + .98 * (pos-cen) + 0.02 * np.random.randn(3)
   target.setPosition(pos)
   q_target, ret = IK(C, pos)
   print(ret)
   C.setJointState(q_target)
   C.view()
time.sleep(10)
