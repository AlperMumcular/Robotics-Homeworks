worldbase {}

# Useful Info: Difference between X and Q is; Q is relative Pose
cargo: { X: "t(.0 -1. 0.23) d(0 0 0 1)", shape: ssBox, size: [.4 .4 .4,.05], color: [1 .5 0], mass: .1, contact: 1 }

cargo_handle_l(cargo): { Q: "t(0.1 0 0.225) d(0 0 0 1)", shape: capsule, size: [.05 .012], color: [1 0 0], mass: .1, contact: 1 }
cargo_handle_r(cargo): { Q: "t(-0.1 0 0.225) d(0 0 0 1)", shape: capsule, size: [.05 .012], color: [1 0 0], mass: .1, contact: 1 }
cargo_handle(cargo): { Q: "t(0.0 0 0.25) d(-90 0 1 0)", shape: capsule, size: [.2 .012], color: [1 0 0], mass: .1, contact: 1 }

#Checkpoints
cp1: {X: "t(4 -3 0.48) d(-90 0 1 0)", shape: marker,size: [.1]}  #Checkpoint_1
cp15: {X: "t(4 0 0.48) d(-90 0 1 0)", shape: marker,size: [.1]}  #Checkpoint_1.5

cp2: {X: "t(-2 3. 0.48) d(-90 0 1 0)", shape: marker,size: [.1]}  #Checkpoint_2
cp25: {X: "t(-3 -3. 0.48) d(-90 0 1 0)", shape: marker,size: [.1]}  #Checkpoint_2.5
final: {X: "t(-4.5 -3. 0.48) d(-90 0 1 0)", shape: marker,size: [.1]} #Final_Destination
