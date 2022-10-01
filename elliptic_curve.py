"""
	Generic class for elliptic curve :
"""

class EllipticCurve:
	def __init__(self, name = "Generic elliptic curve"):
		self.name = name

	def add(self, P, Q):
		pass
	def double(self, P):
		pass
	def on_curve(self, P):
		pass
	def mult(self, P, m):
		pass
	def get_order(self):
		pass



"""
	Weierstrass curve class:
"""
class WeirstrassCurve(EllipticCurve):
	def __init__(self, a, b, p, G, q):
		"""
			Weierstrass form is of the following : y^2 = x^3 + ax + b [mod p]

			Here we have given a, b and p.
			G is the generator and q is the order of the group
		"""
		super().__init__("Weierstrass curve")
		self.a = a
		self.b = b
		self.p = p
		self.G = G
		self.q = q

	def add(self, P, Q):
		# Check for infinity
		if P == [-1, -1]:
			return Q
		
		if Q == [-1, -1]:
			return P

		# Doubling
		if (P == Q): 
			return self.double(P)

		# Next point should be infinity
		if (P[0] - Q[0]) % self.p == 0:
			return [-1, -1] 

		# Adding
		s = ((P[1] - Q[-1]) * pow(P[0] - Q[0], -1, self.p)) % self.p 

		R = [-1, -1] 
		R[0] = (s ** 2 - P[0] - Q[0]) % self.p 
		R[1] = (-P[1] + s * (P[0] - R[0])) % self.p 
		
		return R
	def double(self, P):
		# Check for infinity
		if P == [-1, -1]:
			return P

		# Next point should be infinity
		if (2 * P[1]) % self.p == 0:
			return [-1, -1] 

		# Doubling
		s = ((3 * P[0] ** 2 + self.a) * pow(2 * P[1], -1, self.p)) % self.p 

		R = [-1, -1] 
		R[0] = (s ** 2 - 2 * P[0]) % self.p 
		R[1] = (-P[1] + s * (P[0] - R[0])) % self.p 

		return R
	def on_curve(self, P):
		# Check infinity
		if P == [-1, -1]:
			return True 
		# Check on curve
		return (P[1] ** 2) % self.p == (P[0] ** 3 + P[0] * self.a + self.b) % self.p
	def mult(self, P, m):
		# Make m positive
		m = m % self.q

		# Transform m into list of 1/0
		M = []
		while m != 0:
			M.append(m % 2)
			m = m >> 1
		M = list(reversed(M))

		# Double and add algorithm
		R = [-1, -1]
		for i in M:
			R = self.double(R)
			if i == 1:
				R = self.add(P, R)
		return R
	def get_order(self):
		return self.q

class MontgomeryCurve(EllipticCurve):
	def __init__(self, B, A, p, G, q):
		"""
			Montgomery form is of the following : By^2 = x^3 + Ax^2 + x [mod p]

			Here we have given B, A and p.
			G is the generator and q is the order of the group
		"""
		super().__init__("Montgomery curve")
		self.B = B
		self.A = A
		self.p = p
		self.G = G
		self.q = q
	def add(self, P, Q):
		# Check for infinity
		if P == [-1, -1]:
			return Q
		
		if Q == [-1, -1]:
			return P

		# Doubling
		if (P == Q): 
			return double(P)

		# Next point should be infinity
		if (P[0] - Q[0]) % self.p == 0:
			return [-1, -1] 

		# Adding
		s = ((P[1] - Q[1]) * pow(P[0] - Q[0], -1, self.p)) % self.p 

		R = [-1, -1] 
		R[0] = (B * s ** 2 - self.A - P[0] - Q[0]) % self.p 
		R[1] = (-P[1] -self.B * s**3 + s * (self.A  + 2*P[0] + Q[0])) % self.p 
		
		return R
	def double(self, P):
		# Check for infinity
		if P == [-1, -1]:
			return P

		# Next point should be infinity
		if (2 * P[1]) % self.p == 0:
			return [-1, -1] 

		# Doubling
		s = ((3 * P[0] ** 2 + 2 * self.A * P[0] + 1) * pow(2 * B * P[1], -1, self.p)) % self.p

		R = [-1, -1] 
		R[0] = (self.B * s ** 2 - 2 * P[0] - self.A) % self.p 
		R[1] = (-P[1] - self.B * s ** 3 + s * (self.A  + 3*P[0]) ) % self.p 

		return R
	def on_curve(self, P):
		# Check infinity
		if P == [-1, -1]:
			return True 
		# Check on curve
		return (self.B * P[1] ** 2) % self.p == (P[0] ** 3 + self.A * P[0] ** 2 + P[0]) % self.p
	def mult(self, P, m):
		# Make m positive
		m = m % self.q

		# Transform m into list of 1/0
		M = []
		while m != 0:
			M.append(m % 2)
			m = m >> 1
		M = list(reversed(M))

		# Double and add algorithm
		R = [-1, -1]
		for i in M:
			R = self.double(R)
			if i == 1:
				R = self.add(P, R)
		return R
	def get_order(self):
		return self.q