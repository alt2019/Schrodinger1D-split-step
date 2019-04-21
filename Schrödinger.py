# pre-installed libs
import math as m
from math import factorial as fact
import cmath as cm

# extra libs
import numpy as np

# needed project files
from grid import Grid2D_TX


# global variable for precise solution
n = 1


class SchrödingerEquation:
	"""
	Class implementing a numerical split-step solution of the time-dependent
	Schrodinger equation for an arbitrary potential with arbitrary initial
	function
	"""
	def __init__(self, 
				 grid: Grid2D_TX, 
				 potential: np.ndarray = None,
				 init_func: function = None):
		self.grid = grid
		self.potential = potential 
		self.init_func = init_func

		# initialise grid
		self._set_grid()
		# enter k-space
		self._make_k_space()
		# initialize precise solution
		self._set_precise_solution()

	def _set_precise_solution(self) -> None:
		self.prec_sol = np.zeros((len(self.T), len(self.X)), dtype = complex)
		self.phase = np.zeros((len(self.T), len(self.X)), dtype = complex)
		E_n = n + 0.5
		for t in range(len(self.T)):
			self.prec_sol[t] = np.exp(-1j * E_n * self.T[t]) * self.init_func
			for x in range(len(self.X)):
				self.phase[t][x] = cm.phase(self.prec_sol[t][x]) 

	def get_precise_solution(self):
		return self.prec_sol

	def get_phase(self):
		return self.phase

	def _set_grid(self):
		self.X, self.dx, self.T, self.dt = self.grid.make_grid("real")

	def _make_k_space(self):
		self.K = np.array([ 2 * m.pi / abs(self.X[0] - self.X[-1])\
		 * (n - len(self.X) / 2)\
		  for n in range(len(self.X)) ], dtype = complex)

	def get_k_space(self, dtype = "complex"):
		if dtype == "real":
			return self.K.real
		else: 
			return self.K

	def solve(self):
		# pre-step. initiaizing arrays 
		psi = np.zeros((len(self.T), len(self.X)), dtype = complex)
		self.phase = np.zeros((len(self.T), len(self.X)), dtype = complex)
		# step 0. initial condition 
		psi[0] = self.init_func
		for x in range(len(self.X)):
			self.phase[0][x] = cm.phase(psi[0][x])
		for t in range(1, len(self.T)):
			# step 1. before fourier transform 
			for x in range(len(self.X)):
				psi[t][x] = np.exp(-1j * self.dt / 2 * (self.potential(self.X[x]))) * psi[t-1][x] * np.power(-1, x)
			# step 2. fourier transform
			psi[t] = np.fft.fft(psi[t])
			# step 3. reformation in k-space
			for k in range(len(self.K)):
				psi[t][k] *= cm.exp(-1j * self.dt / 2 * pow(self.K[k], 2))
			# step 4. inverse fourier transform
			psi[t] = np.fft.ifft(psi[t])
			# step 5. after fourier transform & phase 
			for x in range(len(self.X)):
				psi[t][x] = np.exp(-1j * self.dt / 2 * (self.potential(self.X[x]))) * psi[t][x] * np.power(-1, x)
				self.phase[t][x] = cm.phase(psi[t][x])
		return psi


if __name__ == '__main__':
	... 
