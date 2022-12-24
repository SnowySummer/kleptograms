"""
	Generic class for elliptic curve :
"""

class EllipticCurve:
	"""
		We define the functions necessary to be defined for all curves
	"""
	def __init__(self, name = "Generic elliptic curve"):
		self.name = name


	def get_order(self):
		print("Unimplemented function!")
		raise NotImplementedError


	def on_curve(self, P):
		print("Unimplemented function!")
		raise NotImplementedError


	def add(self, P, Q):
		print("Unimplemented function!")
		raise NotImplementedError
	def double(self, P):
		print("Unimplemented function!")
		raise NotImplementedError
	def mult(self, P, m):
		print("Unimplemented function!")
		raise NotImplementedError



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

	def get_order(self):
		return self.q

	def on_curve(self, P):
		# Check infinity
		if P == [-1, -1]:
			return True 
		# Check on curve
		return (P[1] ** 2) % self.p == (P[0] ** 3 + self.a * P[0] + self.b) % self.p

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

"""
	Montgomery curve class:
"""
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


	def get_order(self):
		return self.q


	def on_curve(self, P):
		# Check infinity
		if P == [-1, -1]:
			return True 
		# Check on curve
		return (self.B * P[1] ** 2) % self.p == (P[0] ** 3 + self.A * P[0] ** 2 + P[0]) % self.p


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
		R[0] = (self.B * s ** 2 - self.A - P[0] - Q[0]) % self.p 
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
		s = ((3 * P[0] ** 2 + 2 * self.A * P[0] + 1) * pow(2 * self.B * P[1], -1, self.p)) % self.p

		R = [-1, -1] 
		R[0] = (self.B * s ** 2 - 2 * P[0] - self.A) % self.p 
		R[1] = (-P[1] - self.B * s ** 3 + s * (self.A  + 3*P[0]) ) % self.p 

		return R
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




# x25519 curve
x25519  = MontgomeryCurve(
	1,
	486662,
	pow(2, 255) - 19,
	[9, 14781619447589544791020593568409986887264606134616475288964881837755586237401],
	2 ** 252 + 27742317777372353535851937790883648493
)