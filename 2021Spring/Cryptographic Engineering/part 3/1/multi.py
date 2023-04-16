import time
T = 10
def int_multi_op(a,b):
	C = [0 for i in range(2*T)]
	A = bin(a).replace('0b','')[::-1].ljust(T,'0')
	A = [int(x) for x in A]
	B = bin(b).replace('0b','')[::-1].ljust(T,'0')
	B = [int(x) for x in B]
	for i in range(T):
		u = 0
		for j in range(T):
			uv = C[i+j] + A[i]*B[j] + u
			v = uv % 2
			u = uv >> 1
			C[i+j] = v
		C[i+T] = u
	c = ''.join(map(str, C))[::-1]
	c = int(c, 2)
	return int(c)

def int_multi_prod(a, b):
	C = [0 for i in range(2*T)]
	A = bin(a).replace('0b','')[::-1].ljust(T,'0')
	A = [int(x) for x in A]
	B = bin(b).replace('0b','')[::-1].ljust(T,'0')
	B = [int(x) for x in B]

	r0 = 0
	r1 = 0
	r2 = 0

	for k in range(2*T - 2):
		for i in range (T - 1):
			j = k - i
			if not j in range(T): break
			uv = A[i]*B[j]
			v = uv % 2
			u = uv >> 1

			er0 = r0 + v
			r0 = er0 % 2
			epsilon = er0 >> 1
			
			er1 = r1 + u + epsilon
			r1 = er1 % 2
			epsilon = er1 >> 1

			r2 = r2 + epsilon
			# print(r2)
		C[k] = r0
		r0 = r1
		r1 = r2
		r2 = 0
	C[2*T - 1] = r0

	c = ''.join(map(str, C))[::-1]
	c = int(c, 2)
	return int(c)

start_time = time.time()
print(int_multi_op(24,32))
print(time.time()-start_time)

start_time = time.time()
print(int_multi_prod(24,32))
print(time.time()-start_time)
