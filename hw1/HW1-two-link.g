zero { X:"T t(0 0 0) d(180 0 0 1)" shape:sphere mass=1 size=[0. 0. 0.6 .05]}

link1 { shape:capsule mass=1 size=[0. 0. 1. .05] color: [0 0 1]}

(zero link1) { joint:hingeX, pre:"T t(0 0 .00)" B:"T t(0 0 .55)" }

link2 { shape:capsule mass=1 size=[0. 0. 1. .05] color: [1 0 0]}

(link1 link2) { joint:hingeX, pre:"T t(0 0.0 .5)" B:"T t(0 0.0 .5)" } 

endeffector { shape:sphere mass=1 size=[0. 0. 0.6 .05] color: [0 1 0]}

(link2 endeffector) { joint:hingeX, pre:"T t(0 0.0 .54)" B:"T t(0 0.0 .0)" }

target: { X: "t(0 1 1) d(0 0 0 1)", shape: box, size: [0.2 0.2 0.2 0.5], color: [1 1 0], mass: .1, contact: true }