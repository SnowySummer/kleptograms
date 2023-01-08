# Kleptograms

A showcase of an elliptic curve kleptogram.

This repository contains 2 files :
 - elliptic_curve.py : set-up the framework for using elliptic curves
 - ec_kleptogram.py : set up the actual kleptogram
 
 ## Elliptic curve
 
 The Elliptic curve class is a class where we define the following operations :
 - get the order of the curve
 - check if a point is on the curve
 - addition
 - doubling
 - scalar multiplication
 
 We've defined 2 types of curve, the Weierstrass form and the Montgomery curve
 
 ## Kleptogram
 
 The idea behind the kleptogram is to generate numbers $c_n$ and to send $c_n$ $G$. We carefully define $c_n$ such that it can be rediscovered by the attacker, but not by other agents.
 
First, we generate $c_1$, we then define $c_2$ as follows :
$$t \in \\{0, 1\\}$$
$$z = (c_1 - wt) G + (-ac_1 - b) . Q$$ 
$$c_2 = H(z)$$

Where $w$ is an odd number, $a$, $b$ are integers and $Q = k G$ where $k$ is only known by the attacker.  H is a non-invertible function.


The attacker can find $c_2$ from $M_1$ $=$ $c_1$ $G$ and $M_2$ $=$ $c_2$ $G$ by calculating the following :
$$R = aM_1 + bG$$
$$Z = M_1 - kR$$

If $H(Z)G = M_2$, then $c_2 = H(Z)$

If not, then $c_2 = H(Z - wG)$
