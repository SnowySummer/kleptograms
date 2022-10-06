# Kleptograms

A repo showcasing elliptic curve kleptograms

This repository contains 2 files :
 - elliptic_curve.py : set-up the framework for elliptic curves
 - ec_kleptogram.py : set up the actual kleptogram
 
 ## Elliptic curve
 
 The Elliptic curve is a class where we define elliptic curves operation :
 - addition
 - doubling
 - scalar multiplication
 - check if a point is on the curve
 - get the order of the curve
 
 We've defined 2 types of curve, the Weierstrass form and the Montgomery curve
 
 ## Kleptogram
 
 The idea behind the kleptogram is to generate numbers $c_n$ and to send $c_n$ $G$. We carefully define $c_n$ such that it can be rediscovered by the attacker, but not by other agents.
 
First, we generate $c_1$, we then define $c_2$ as follows :
- Set t as 0 or 1
- Define z = ($c_1$ - $wt$) $G$ . ($-ac_1$ - $b$) . $Q$
- Define $c_2$ = H(z)
