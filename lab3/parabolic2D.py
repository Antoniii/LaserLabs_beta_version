import numpy as np 
from lu3 import solveLU3

'''
u'_t = u''_{x_1^2} + u''_{x_2^2} + f(X,t), X = {x_1, x_2}
u(X,t) = 0, 0 < t <= T
u(X,0) = v(X) 
'''

def parabolic2D(f, v, l1, l2, tEnd, n1, n2, tau):
	h1 = l1 / n1
	h2 = l2 / n2
	a1 = np.ones((n1+1), 'float')
	b1 = np.zeros((n1+1), 'float')
	c1 = np.zeros((n1+1), 'float')
	q1 = np.zeros((n1+1), 'float')
	a2 = np.ones((n2+1), 'float')
	b2 = np.zeros((n2+1), 'float')
	c2 = np.zeros((n2+1), 'float')
	q2 = np.zeros((n2+1), 'float')
	t0 = 0.
	y0 = np.zeros((n1+1, n2+1), 'float')

	for i in range(1, n1):
		for j in range(1, n2):
			y0[i,j] = v(i*h1,j*h2)
	y = np.copy(y0)

	while t0 < tEnd - 0.001*tau:
		tau = min(tau, tEnd - t0)
		
		# x1 direction
		for j in range(1, n2):
			for i in range(1,n1):
				a1[i] = 2. / tau + 2./h1**2
				b1[i] = -1./h1**2
				c1[i] = -1./h1**2
				q1[i] = f(i*h1, j*h2, t0+tau/2.) + 2.*y[i,j]/tau \
						+ (y[i,j+1]-2.*y[i,j]+y[i,j-1])/h2**2
			y0[:,j] = solveLU3(a1, b1, c1, q1)
		# x2 direction
		for i in range(1, n1):
			for j in range(1, n2):
				a2[j] = 2./tau + 2./h2**2
				b2[j] = -1./h2**2
				c2[j] = -1./h2**2
				q2[j] = f(i*h1, j*h2, t0+tau/2.) + 2.*y0[i,j]/tau \
						+ (y0[i+1,j]-2.*y0[i,j]+y0[i-1,j])/h1**2
			y[i,:] = solveLU3(a2, b2, c2, q2)
		t0 = t0 + tau
	return t0, y