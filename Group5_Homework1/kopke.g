waist: { X: "t(0 1.25 1.) d(180 0 0 1)", shape: capsule, mass: 1, size: [0., 0., .2, .05] }

upArmR: { shape: capsule, mass: .1, size: [.15, .15, .5, .075] }
dnArmR: { shape: capsule, mass: .1, size: [.15, .15, .4, .075] }
upWristR: { shape: capsule, mass: .1, size: [.15, .15, .3, .06], contact }



(waist upArmR): { joint: hingeX, pre: "d(-90 0 0 0) t(0 0 .075)", post: "t(0 0 .25)" }
(upArmR dnArmR): { joint: hingeX, pre: "t(0 0 .075) d( 90 0 1 0) d(30 1 0 0)", post: "d(-90 0 1 0) t(0 0 .075)" }
(dnArmR upWristR): { joint: hingeX, pre: "t(0 0 .2) d(90 1  0 0)", post: "t(0 0 .15)" }



## left & right hand

dnWristR: { shape: capsule, mass: .01, size: [.1, .1, .2, .055] }
ddnWristR: { shape: capsule, mass: .01, size: [.5, .5, .1, .05] }
handR: { shape: ssBox, mass: .01, size: [.1, .04, .1, .05], color: [0, 0, 0] }

(upWristR dnWristR): { joint: hingeX, pre: "t(0 0 .1) d( 90 0 1 0) d(90 1 0 0)", post: "d(-90 0 1 0) t(0 0 .1)" }
(dnWristR ddnWristR): { joint: hingeX, pre: "t(0 0 .075) d( 90 0 0 1)", post: "d(-90 0 0 1) t(0 0 .05)" }
(ddnWristR handR): { joint: hingeX, pre: "t(0 0 .045)", post: "t(0 0 .075) d(180 0 1 0)" }

## legs
body:  {mass:  2, size[0.5, 1, 0.2, 0.12], shape: ssBox}
flhip: { mass: 1, size: [.15, .15, .03, .08], shape: capsule }
frhip: { mass: 1, size: [.15, .15, .03, .08], shape: capsule }
rlhip: { mass: 1, size: [.15, .15, .03, .08], shape: capsule }
rrhip: { mass: 1, size: [.15, .15, .03, .08], shape: capsule }

flup: { mass: 1, size: [.15, .15, .26, .11], shape: capsule } 
frup: { mass: 1, size: [.15, .15, .26, .11], shape: capsule } 
rlup: { mass: 1, size: [.15, .15, .26, .11], shape: capsule } 
rrup: { mass: 1, size: [.15, .15, .26, .11], shape: capsule } 
fldn: { mass: 1, size: [.15, .15, .45, .09], shape: capsule } 
frdn: { mass: 1, size: [.15, .15, .45, .09], shape: capsule } 
rldn: { mass: 1, size: [.15, .15, .45, .09], shape: capsule } 
rrdn: { mass: 1, size: [.15, .15, .45, .09], shape: capsule } 
flfoot: { mass: 1, size: [.15, .45, .05, .02], shape: ssBox }
frfoot: { mass: 1, size: [.15, .45, .05, .02], shape: ssBox }
rlfoot: { mass: 1, size: [.15, .45, .05, .02], shape: ssBox }
rrfoot: { mass: 1, size: [.15, .45, .05, .02], shape: ssBox }



(waist body) : { joint: hingeX, pre: "t(0 .5 -.08) d(90 0 0 1)",post: "d(90 0 0 1) t(0 0 -.015)" }
(body flhip): { joint: hingeX, pre: "t(-.15 .45 0) d(90 0 0 1)", post: "d(90 0 0 1) t(0 0 -.015)" }
(body frhip): { joint: hingeX, pre: "t(+.15 .45 0) d(90 0 0 1)", post: "d(90 0 0 1) t(0 0 -.015)" }
(body rlhip): { joint: hingeX, pre: "t(-.15 -.45 0) d(90 0 0 1)", post: "d(90 0 0 1) t(0 0 -.015)" }
(body rrhip): { joint: hingeX, pre: "t(+.15 -.45 0) d(90 0 0 1)", post: "d(90 0 0 1) t(0 0 -.015)" }

(flhip flup): { joint: hingeX, pre: "t(0 0 -.015) d(-20 1 0 0)", post: "t(0 0 -.19)" }
(frhip frup): { joint: hingeX, pre: "t(0 0 -.015) d(-20 1 0 0)", post: "t(0 0 -.19)" }
(rlhip rlup): { joint: hingeX, pre: "t(0 0 -.015) d(-20 1 0 0)", post: "t(0 0 -.19)" }
(rrhip rrup): { joint: hingeX, pre: "t(0 0 -.015) d(-20 1 0 0)", post: "t(0 0 -.19)" }
(flup fldn): { joint: hingeX, pre: "t(0 0 -.19) d(40 1 0 0)", post: "t(0 .015 -.23)" }
(frup frdn): { joint: hingeX, pre: "t(0 0 -.19) d(40 1 0 0)", post: "t(0 .015 -.23)" }
(rlup rldn): { joint: hingeX, pre: "t(0 0 -.19) d(40 1 0 0)", post: "t(0 .015 -.23)" }
(rrup rrdn): { joint: hingeX, pre: "t(0 0 -.19) d(40 1 0 0)", post: "t(0 .015 -.23)" }
(fldn flfoot): { joint: hingeX, pre: "t(0 -.1 -.25) d(-20 1 0 0)", post: "t(0 .06 -.038)" }
(frdn frfoot): { joint: hingeX, pre: "t(0 -.1 -.25) d(-20 1 0 0)", post: "t(0 .06 -.038)" }
(rldn rlfoot): { joint: hingeX, pre: "t(0 -.1 -.25) d(-20 1 0 0)", post: "t(0 .06 -.038)" }
(rrdn rrfoot): { joint: hingeX, pre: "t(0 -.1 -.25) d(-20 1 0 0)", post: "t(0 .06 -.038)" }
