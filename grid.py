# extra libs
import numpy as np


class Grid2D_TX:
	def __init__(self,
				 x_start: float = 0.0, x_end: float = 1.0, dx: float = 0.001,
				 t_start: float = 0.0, t_end: float = 1.0, dt: float = 0.001):
		self.x_start = x_start
		self.x_end = x_end
		self.dx = dx
		self.t_start = t_start
		self.t_end = t_end
		self.dt = dt

		# iniializing grid
		self._set_grid()

	def _set_grid(self):
		self.X = np.arange(self.x_start, self.x_end + self.dx, self.dx, dtype = complex)
		self.T = np.arange(self.t_start, self.t_end + self.dt, self.dt)

	def make_grid(self, dtype: str = "complex") -> (np.ndarray, float, np.ndarray, float):
		if dtype == "real":
			return self.X.real, self.dx, self.T.real, self.dt 
		elif dtype == "complex":
			return self.X, self.dx, self.T, self.dt 


if __name__ == '__main__':
	... 