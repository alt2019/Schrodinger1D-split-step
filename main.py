# check version
import sys
assert sys.version_info >= (3, 7)

# pre-installed libs
import math as m
from math import factorial as fact

# extra libs
import numpy as np

# needed project files
from plotter import draw
from grid import Grid2D_TX
from Schrödinger import SchrödingerEquation

def V(x): return np.power(x, 2)/2

def hermitian_polynome(n, x): 
	if n == 0: return 1 
	elif n == 1: return 2*x 
	else: return 2*x*hermitian_polynome(n-1,x) - 2*(n-1)*hermitian_polynome(n-2,x) 

def un(n, x): 
	return hermitian_polynome(n,x) * np.exp(-x*x/2) / m.sqrt(pow(2,n) * pow(np.pi,0.5) * fact(n))

def U(x, p, q, N, n): 
	z = complex(q, p) / m.sqrt(2)
	exp = np.exp(-0.5 * np.power(abs(z), 2))
	series = 0
	for n in range(N): # must be infinity
		series += np.power(z, n) / m.sqrt(fact(n)) * un(n, x)
	res = exp*series
	return res


if __name__ == '__main__':
	g = Grid2D_TX(
		x_start = -5.0, 
		x_end = 5.0, 
		dx = 0.01, 
		t_start = 0.0, 
		t_end = 12.56, 
		dt = 0.2)

	n = 2
	p = 0.6
	q = 0.8
	N = 20

	S = SchrödingerEquation(grid = g, potential = V, 
							 init_func = un(x = g.X, n = n))
	def f1():
		prec_sol = S.prec_sol
		phase = S.phase
		draw(grid = S.grid, sol1 = prec_sol, sol2 = phase,
			 at_point_ID = int(len(g.X)/2), at_time_ID = 4, 
			 do_animation = True)

	S1 = SchrödingerEquation(grid = g, potential = V, 
							 init_func = un(x = g.X, n = n))
	def f2():
		solved1 = S1.solve()
		draw(grid = S1.grid, sol1 = solved1, sol2 = S1.phase,
			 at_point_ID = int(len(g.X)/2), at_time_ID = 4, 
			 do_animation = True)

	S2 = SchrödingerEquation(grid = g, potential = V,  
							 init_func = U(g.X, p = p, q = q, N = N, n = n)) 
	def f3():
		solved2 = S2.solve()
		draw(grid = S2.grid, sol1 = solved2, sol2 = S2.phase,
			 at_point_ID = int(len(g.X)/2), at_time_ID = 4, 
			 do_animation = True)

	f1()
	# f2()
	# f3()

	
