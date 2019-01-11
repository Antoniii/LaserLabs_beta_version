import numpy as np 

def decLU3(a,b,c):
	n = len(a)
	d = np.copy(a)
	u = np.copy(b)
	l = np.copy(c)

	for i in range(1,n):
		al = l[i] / d[i-1]
		d[i] = d[i] - al*u[i-1]
		l[i] = al
	return d, u, l

def solveLU3(a,b,c,f):
	n = len(a)
	d, u, l = decLU3(a,b,c)
	x = np.copy(f)
	for i in range(1,n):
		x[i] = x[i] - l[i]*x[i-1]
	x[n-1] = x[n-1] / d[n-1]
	for i in range(n-2,-1,-1):
		x[i] = (x[i] - u[i]*x[i+1]) / d[i]
	return x