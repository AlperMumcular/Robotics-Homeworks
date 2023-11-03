base_origin: { X: [0, 0, 0.08] }

base (base_origin): {
 joint: transXYPhi, limits: [-20,20,-20,20,-4,4],
 shape: ssCylinder, size: [.1, .3, .02], contact: 1 }