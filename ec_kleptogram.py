from elliptic_curve import *
import random as rand
import sys

def eck_generate(curve, Q, w, a, b):
    """
        Generate a random number as well as its representation
        through elliptic curve from nothing
    """

    # Generate a number
    c1 = rand.randrange(2, curve.q)
    m1 = curve.mult(curve.G, c1)

    # Prepare seed of second number
    t = rand.randrange(2)
    z0 = curve.mult(curve.G, c1-w*t)
    z1 = curve.mult(Q, -a*c1 - b)
    z = curve.add(z0, z1)
    rand.seed(z[0] * 2 + (abs(z[1]) // z[1] + 1) // 2)

    # Generate second number
    c2 = rand.randrange(2, curve.q)
    m2 = curve.mult(curve.G, c2)

    m = [m1, m2]
    return m, c2
def eck_continue(curve, Q, w, a, b, c1):
    """
        Generate a random number as well as its representation
        through elliptic curve from previous seed
    """

    # Prepare seed
    t = rand.randrange(2)
    z1 = curve.mult(curve.G, c1-w*t)
    z2 = curve.mult(Q, -a*c1 - b)
    z = curve.add(z1, z2)
    rand.seed(z[0] * 2 + (abs(z[1]) // z[1] + 1) // 2)

    # Generate number
    c2 = rand.randrange(2, curve.q)
    m2 = curve.mult(curve.G, c2)

    return m2, c2
def eck_decrypt(curve, k, w, a, b, m1, m2):
    """
        Recover random number from 2 elliptic curve
        representation
    """

    # Recover initial seed
    r0 = curve.mult(m1, a)
    r1 = curve.mult(curve.G, b)
    r = curve.add(r0, r1)
    z1 = curve.mult(r, -k)
    z1 = curve.add(m1, z1)

    # Manually check the seed (choice from 2 options)
    rand.seed(z1[0] * 2 + (abs(z1[1]) // z1[1] + 1) // 2)
    c2 = rand.randrange(2, curve.q)
    if curve.mult(curve.G, c2) != m2:
        point = curve.add(z1, curve.mult(curve.G, -w))
        rand.seed(point[0] * 2 + (abs(point[1]) // point[1] + 1) // 2)
        c2 = rand.randrange(2, curve.q)
    
    return c2

if __name__ == "__main__":

    # Attackers toolbox
    k = 5
    Q = x25519.mult(x25519.G, k)
    w = 7
    a = 1
    b = 4

    # Start attack
    num_messages = 100
    print(f"Start test with {num_messages} messages")
    m, cn = eck_generate(x25519, Q, w, a, b)

    # List of correct random numbers
    c_check = [cn]

    # Continue attack
    for i in range(num_messages):
        m.append(0)
        m[-1], cn = eck_continue(x25519, Q, w, a, b, cn)
        c_check.append(cn)



    # Recalculate random values
    c = []
    for i in range(len(m) - 1):
        c.append(eck_decrypt(x25519, k, w, a, b, m[i], m[i + 1]))
    
    for i in range(num_messages):
        if (c[i] != c_check[i]):
            print(c[i])
            print(c_check[i], '\n')
            sys.exit()
    print("Test passed")