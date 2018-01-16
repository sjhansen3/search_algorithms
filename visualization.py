import numpy as np
import os
import matplotlib.pyplot as plt
import sys
import search_problem
import search_method
import world

class Visualizer:
	def __init__(self, start, goal, walls):
		self.start = start
		self.goal = goal
		self.walls = walls
		self.visited = []
		self.width = len(walls[0])
		self.height = len(walls)

	def set_action_plan(self, action_plan):
        """Formats and sets the trajectory (self.traj) for visualization 
        Params
        ---
        action_plan: a list of Directinos representing the optimal set of actions from start to goal
        """
		if not action_plan:
			print("No solution found to goal")
			action_plan = [world.Direction.EAST]
		#TODO VideoGAmeActions should be a general actions
		self.traj = world.VideoGameActions.get_trajectory(self.start, action_plan)

	def append_visited(self, state):
        """Adds a state to the list of nodes that have been visited 
        for visualization of the effeciency of a particular heuristic or alorithm
        Params
        ---
        state: the visited state
        """
		self.visited.append(state)

	def show(self):
		"""Display the walls, visited nodes and optimal trajectory to the user"""
		len_c, len_r  = np.shape(self.walls)
		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)

        #create a grid to see the grid cells better
		y_ticks = np.arange(0.5, len_c, 1)
		x_ticks = np.arange(0.5, len_r, 1)
		ax.set_xticks(x_ticks)
		ax.set_yticks(y_ticks)
		ax.grid(which='both')
		ax.grid(which='major', alpha=0.5)

        #display
		plt.imshow(self.walls, aspect='equal', cmap='Greys',interpolation='none', origin='upper')
		plt.scatter(self.start[0],self.start[1],c='g',s=300)
		plt.scatter(self.goal[0],self.goal[1],c='r',s=300)
		plt.scatter(self.traj[0],self.traj[1],c='y',s=100)
		visited = np.asarray(self.visited).T
		plt.scatter(visited[0],visited[1],c='b')
		plt.show()

class MazeLoader:
	def __init__(self, mazename):
		self.path = self._get_path(mazename)
		self.walls = None
		self.start = None
		self.goal = None

	def _get_path(self, mazename):
		script_dir = os.path.dirname(os.path.realpath('__file__'))
		rel_path = 'mazes/'+mazename+'.maze'
		abs_path = os.path.join(script_dir,rel_path)
		return abs_path

	def load(self):
		with open(self.path) as file_handle:
			lines = file_handle.read().split('\n')
			h,w = len(lines), len(lines[0])
		self.walls = np.empty((h,w))
		self.walls[:] = np.nan
		for r, line in enumerate(lines):
			for c, char in enumerate(line):
				if char == "X":
					self.walls[r,c] = True
				elif char == " ":
					self.walls[r,c] = False
				elif char == "S":
					self.walls[r,c] = False
					self.start = (c,r)
					print("Start set at coordinates", self.start)
				elif char == "G":
					self.goal = (c,r)
					self.walls[r,c] = False
					print("Goal set at coordinates", self.goal)
				else:
					print('Error reading file: {} at row: {} col: {}'.format(self.path,r,c))
		if self.start is None or self.goal is None:
			print('Start or goal is not defined in the file {} properly'.format(self.path))

	def get_start(self):
		"""gets the start position in state coordinates"""
		return self.start
	def get_goal(self):
		"""gets the goal position in state coordinates"""
		return self.goal
	def get_walls(self):
		if np.any(np.isnan(self.walls)):
			print("Warning one of the cells in the grid is nan")
		return self.walls