from elliptic_curve import *
import random as rand

def eck_generate(curve, Q, w, a, b):

    c1 = rand.randrange(2, q)
    m1 = curve.mult(curve.G, c1)

    t = rand.randrange(2)
    z0 = curve.mult(curve.G, c1-w*t)
    z1 = curve.mult(Q, -a*c1 - b)
    z = curve.add(z0, z1)

    rand.seed(z[0] * 2 + (abs(z[1]) // z[1] + 1) // 2)
    c2 = rand.randrange(2, q)
    m2 = curve.mult(curve.G, c2)

    m = [m1, m2]
    return m, c2


def eck_continue(curve, Q, w, a, b, c1):

    t = rand.randrange(2)
    z1 = curve.mult(curve.G, c1-w*t)
    z2 = curve.mult(Q, -a*c1 - b)
    z = curve.add(z1, z2)

    rand.seed(z[0] * 2 + (abs(z[1]) // z[1] + 1) // 2)
    c2 = rand.randrange(2, q)
    m2 = curve.mult(curve.G, c2)

    return m2, c2

def eck_decrypt(curve, k, w, a, b, m1, m2):

    r0 = curve.mult(m1, a)
    r1 = curve.mult(curve.G, b)
    r = curve.add(r0, r1)
    
    z1 = curve.mult(r, -k)
    z1 = curve.add(m1, z1)
 
    rand.seed(z1[0] * 2 + (abs(z1[1]) // z1[1] + 1) // 2)
    c2 = rand.randrange(2, q)
    if curve.mult(curve.G, c2) != m2:
        point = curve.add(z1, curve.mult(curve.G, -w))
        rand.seed(point[0] * 2 + (abs(point[1]) // point[1] + 1) // 2)
        c2 = rand.randrange(2, q)
        
    m2 = curve.mult(curve.G, c2)
    return c2