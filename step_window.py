import numpy as np

def step_window(array, window, step):
	"""
	This function is built to take a numpy array and convert it
	to a 3D array where the specified window size will be the new
	array row length, column number will not change, and the array
	depth (epochs) will depend on both the window and step size.
	NOTE: based on the specified window and step size, your new
	array may be truncated 

	array: numpy array
	window: window size based on array index
	step: number of rows between captured windows (may overlap with
		other windows)

	And sorry, people reading this, but I like to think of matricies
	in Cartesian coordinates. It's the only way I can keep everything
	straight in my head. So to me, x = columns, y = rows, z = depth.
	If you really hate that, then feel free to change the code :)
	"""

	if array.ndim < 2:
		array = array.reshape(len(array), 1)
		columns = 1
	else:
		columns = array.shape[1]
	rows = array.shape[0]
	new_x, new_y = columns, window
	new_z = int(1 + (rows - window) / step)
	new_array = np.empty([new_y, new_x, new_z])
	for x in range(new_z):
		new_array[:,:,x] = array[(0 + step * x):(window + step * x)]
	return new_array 