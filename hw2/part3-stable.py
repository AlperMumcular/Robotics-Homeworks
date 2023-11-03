from robotic import ry
import math
import time
ry.params_add({'physx/motorKp': 10000., 'physx/motorKd': 1000., 'physx/angularDamping': 10.})

def calculateDistance( cargo_location, cp_location ):

    distX, distY = cp_location[0] - cargo_location[0], cp_location[1] - cargo_location[1]
    totalDistance = math.sqrt( distX ** 2 + distY ** 2 )
    print("total ", totalDistance, " distX ", distX, " distY ", distY)
    computedDistance = totalDistance + 1

    # computedDistance = totalDistance + 0.4 + 0.3


    baseX = computedDistance * distX / totalDistance
    baseY = computedDistance * distY / totalDistance

    baseX = cp_location[0] - baseX
    baseY = cp_location[1] - baseY

    return [baseX, baseY, 0.08]



C = ry.Config()
C.addFile('cargobot_base.g')
C.addFile('push_cargo.g')
C.addFile('push_maze.g')

C.view()

new_cargo_coordinates = C.addFrame('new_cargo_coordinates', 'cargo')
new_cargo_coordinates.setShape(ry.ST.marker, size=[.1])
new_cargo_coordinates.setPosition(C.frame('cargo').getPosition())

new_base_coordinates = C.addFrame('new_base_coordinates', 'base')
new_base_coordinates.setShape(ry.ST.marker, size=[.1])
new_base_coordinates.setPosition(C.frame('base').getPosition())

way0 = C.addFrame('way0')
way0.setShape(ry.ST.marker, size=[.1])
way0.setPosition([1, -3, 0.4])

way1 = C.addFrame('way1')
way1.setShape(ry.ST.marker, size=[.1])
way1.setPosition([-3., -3., 0.4])

tmp = C.addFrame('tmp','cargo')
tmp.setShape(ry.ST.marker, size=[.1])

# fakecargo = C.addFrame('fakecargo')
# fakecargo.setShape(ry.ST.sphere, size=[.45,.45,.45,.45])
# fakecargo.setColor([1,1,1,0])
# fakecargo.setPosition(C.frame('cargo').getPosition())
# fakecargo.setContact(True)


checkpointLevel = 0

bot = ry.BotOp(C, False)
# time.sleep(5)

while True:   
    #print("=== Iteration", x, "===")

    curr_cargo_pos = C.frame('new_cargo_coordinates').getPosition()

    if checkpointLevel == 0:
        print("TARGET: way0")
        new_location = calculateDistance(curr_cargo_pos, way0.getPosition())

    elif checkpointLevel == 1:
        print("TARGET: cp2")
        new_location = calculateDistance(curr_cargo_pos, C.frame('cp2').getPosition())

    elif checkpointLevel == 2:
        print("TARGET: cp3")
        new_location = calculateDistance(curr_cargo_pos, C.frame('cp3').getPosition())

    elif checkpointLevel == 3:
        print("TARGET: cp4")
        new_location = calculateDistance(curr_cargo_pos, C.frame('cp4').getPosition())
    
    elif checkpointLevel == 4:
        print("TARGET: way1")
        new_location = calculateDistance(curr_cargo_pos, way1.getPosition())

    elif checkpointLevel == 5:
        print("TARGET: finish_line")
        new_location = calculateDistance(curr_cargo_pos, C.frame('finish_line').getPosition())

        
    tmp.setPosition(new_location)
    print(tmp.getPosition())

    komo = ry.KOMO()
    
    komo.setConfig(C, True)
    komo.initRandom(3)
    komo.setTiming(2, 1, 10., 1)

    komo.addControlObjective([], 1, 1e1)
    komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.eq, [1e3])
    # komo.addObjective([], ry.FS.accumulatedCollisions, ['new_base_coordinates', 'new_cargo_coordinates'], ry.OT.eq, [1e9]) # DOES THIS MAKE SENSE ????
    komo.addObjective([1], ry.FS.positionDiff, ['new_base_coordinates', 'tmp'], ry.OT.eq, [1e1])
    komo.addObjective([2], ry.FS.positionDiff, ['new_base_coordinates', 'new_cargo_coordinates'], ry.OT.eq, [1e1])    

    

    ret = ry.NLP_Solver(komo.nlp(), verbose=0 ) .solve()
    #print(ret)

    path = komo.getPath()

    for pos in path:
        bot.moveTo(pos, 50)

        bot.wait(C, True, True)

        # while bot.getTimeToEnd()>0:
        #    bot.sync(C, .02)

    


    new_base_coordinates.setPosition(path[-1])
    cargo_loc = C.frame('cargo').getPosition()
    new_cargo_coordinates.setPosition(cargo_loc)


    if new_cargo_coordinates.getPosition()[1] < C.frame('cp1').getPosition()[1] and new_cargo_coordinates.getPosition()[0] < 5 and new_cargo_coordinates.getPosition()[0] > -1:
        checkpointLevel = 1
        print("CHECKPOINT: 0 -> 1")

    elif new_cargo_coordinates.getPosition()[1] > C.frame('cp2').getPosition()[1] and new_cargo_coordinates.getPosition()[0] < 5 and new_cargo_coordinates.getPosition()[0] > 3:
        checkpointLevel = 2
        print("CHECKPOINT: 1 -> 2")

    elif new_cargo_coordinates.getPosition()[0] < C.frame('cp3').getPosition()[0] and new_cargo_coordinates.getPosition()[1] < 4 and new_cargo_coordinates.getPosition()[1] > 2:
        checkpointLevel = 3
        print("CHECKPOINT: 2 -> 3")
    
    elif new_cargo_coordinates.getPosition()[1] < C.frame('cp4').getPosition()[1] and new_cargo_coordinates.getPosition()[0] < -1 and new_cargo_coordinates.getPosition()[0] > -3:
        checkpointLevel = 4
        print("CHECKPOINT: 3 -> 4")
    
    elif new_cargo_coordinates.getPosition()[0] < C.frame('way1').getPosition()[0] and new_cargo_coordinates.getPosition()[0] > C.frame('finish_line').getPosition()[0] and new_cargo_coordinates.getPosition()[1] < -2 and new_cargo_coordinates.getPosition()[1] > -4:
        checkpointLevel = 5
        print("CHECKPOINT: 4 -> 5")
    
    elif cargo_loc[0] < -4 and cargo_loc[0] > -5 and cargo_loc[1] < -2 and cargo_loc[1] > -4:
        print("IN THE BOX")
        del komo 
        break

    del komo

del bot