# pre-installed libs
import math as m 

# extra libs
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 

# needed project files
from grid import Grid2D_TX


def maximize_window(is_maximazed_window_needed: bool = False, 
					is_full_screen_needed: bool = False) -> None:
	manager = plt.get_current_fig_manager() 
	if is_maximazed_window_needed is True:
		manager.window.state('zoomed') # maximized window
	if is_full_screen_needed is True:
		manager.full_screen_toggle() # full-screen mode	


def draw(grid: Grid2D_TX, 
		 sol1: np.ndarray, 
		 sol2: np.ndarray, 
		 do_animation: bool = True, 
		 at_time_ID: int = 0, 
		 at_point_ID: int = 0, 
		 repeat_animation: bool = True,  
		 is_maximazed_window_needed: bool = False, 
		 is_full_screen_needed: bool = False) -> None:
	# sol1, sol2: 2d array
	# sol1 -> psi, sol2 -> phase

	X, dx, T, dt = grid.make_grid("real")

	plt.style.use('dark_background') 
	fig = plt.figure() 
	ax1 = fig.add_subplot(3,1,1, 
						  xlim = (X[0], X[-1]))
	ax2 = fig.add_subplot(3,1,2, 
						   xlim = (X[0], X[-1]))
	ax3 = fig.add_subplot(3,1,3, 
						   xlim = (T[0], T[-1]))

	def animate(t): 
		ax1.clear() 
		ax1.set_ylabel(r'$|\psi(x)|$') 
		ax1.set_ylim(min(abs(sol1[0]))*0.9, 
					 max(abs(sol1[0]))*1.5)
		aux_str4latex = r'$x_{markered\ point}$'
		string =  't = {t}, T = {T:10f}, '.format(
					 t = t,
					 T = (T[-1] - T[0]) / len(T) * t)\
			 		+ aux_str4latex +\
			  		' = {x:10f}'.format(x = X[at_point_ID])
		text_pos_ID = int((len(X) - len(string)) / 4)
		ax1.text(X[text_pos_ID], max(abs(sol1[0]))*1.6, s = string)
		ax1.plot(X, abs(sol1[t])) 
		ax1.plot(X[at_point_ID], abs(sol1[t])[at_point_ID], ".b", markersize=12)
		ax1.grid(True) 

		ax2.clear() 
		ax2.set_xlabel('$X$') 
		ax2.set_ylabel('$phase$') 
		ax2.set_ylim(-m.pi, m.pi)
		ax2.plot(X, sol2[t].real)
		ax2.plot(X[at_point_ID], sol2[t][at_point_ID].real, ".b", markersize=12)
		ax2.grid(True) 
 
		ax3.clear() 
		ax3.set_xlabel('$T$') 
		ax3.set_ylabel('$phase$') 
		ax3.set_xlim(T[0], T[-1])
		ax3.set_ylim(-m.pi, m.pi)
		ax3.plot(T, np.transpose(sol2.real)[at_point_ID], "r")
		ax3.plot(T[t], np.transpose(sol2.real)[at_point_ID][t], ".b" , markersize=12)
		ax3.grid(True)

	do_repeat = True if repeat_animation else False
	anim = animation.FuncAnimation(fig, 
								   animate, 
								   frames=len(sol1), 
								   interval=1, 
								   repeat = do_repeat) 

	maximize_window(is_maximazed_window_needed, is_full_screen_needed)

	plt.show()


if __name__ == '__main__':
	... 