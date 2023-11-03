from robotic import ry
import time
import numpy as np
C = ry.Config()

#C.addFile('cargobot.g')
# Imported cargobot into the library folder
C.addFile(ry.raiPath('../rai-robotModels/scenarios/cargobot.g'))
C.addFile('cargo.g')
C.addFile('maze.g')
qHome = C.getJointState()
S = ry.Skeleton()
S.addEntry([1.,6.], ry.SY.touch,  ["l_gripper", "cargo_handle"])
S.addEntry([1.,6], ry.SY.stable,  ["l_gripper", "cargo_handle"])
S.addEntry([2, 2], ry.SY.poseEq, ["base", "cp1"])
S.addEntry([3, 3], ry.SY.poseEq, ["base", "cp15"])
S.addEntry([4, 4.], ry.SY.poseEq, ["base", "cp2"])
S.addEntry([5,5.], ry.SY.poseEq, ["base", "cp25"])
S.addEntry([6,6.], ry.SY.poseEq, ["cargo_handle", "final"])
S.addEntry([5.9, 6], ry.SY.downUp, ["l_gripper"])

S.enableAccumulatedCollisions(True)
komo = S.getKomo_waypoints(C, 1e-1, 1e-2,1e+1)

nlp = komo.nlp()
sol = ry.NLP_Solver()
sol.setProblem(nlp)
sol.setOptions( stopTolerance=1e-2 )
ret = sol.solve()
waypoints = komo.getPath_qAll()

print(ret)
time.sleep(5)
m = len(waypoints)
rrt_dofs = []
rrt_paths = []
for t in range(0,int(m)):
    # grab config and waypoints
    [Ctmp, q0, q1] = S.getTwoWaypointProblem(t, komo)
    Ctmp.setJointState(q0)
#    Ctmp.view(True, 'waypoint configuration phase ' + str(t) + ' START')
    Ctmp.setJointState(q1)
#    Ctmp.view(True, 'waypoint configuration phase ' + str(t) + ' STOP')

#    Ctmp.view(True, 'Continue')

    # call path finder
    sol = ry.PathFinder()
    sol.setProblem(Ctmp, q0, q1)
    ret = sol.solve()
    
    rrt_paths.append(ret.x)
    
    rrt_dofs.append(Ctmp.getDofIDs())
    
    #display the rrt path
#    for i in range(0,ret.x.shape[0]):
#        Ctmp.setJointState(ret.x[i])
#        Ctmp.view(False, 'rrt path ' + str(i))
#        time.sleep(.02)

komo = S.getKomo_path(C,40, 1e0, 1e2, 1e-2,1e4)
komo.initWithWaypoints(waypoints)
for t in range(0,int(m)):
    komo.initPhaseWithDofsPath(t, rrt_dofs[t], rrt_paths[t], True)


nlp = komo.nlp()
sol = ry.NLP_Solver()
sol.setProblem(nlp)
sol.setOptions( stopTolerance=1e-2 )
ret = sol.solve()
# report on result, view, and play
print(ret)
#print(nlp.report(2))
komo.view_play(True, .2)