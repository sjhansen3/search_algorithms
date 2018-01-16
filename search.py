import numpy as np
import os
import matplotlib.pyplot as plt
import sys
import search_problem
import search_method
import world

class Visualizer:
	def __init__(self, start, goal, walls, action_plan):
		self.start = start
		self.end = end
		self.walls = walls
		self.path = self._format_path(action_plan)
		self.visited = []

	def _format_path(self, action_plan):
		"""Converts an action plan into a trajectory
		Params
		---
		action_plan: a list of action tuples
		Returns
		---
		trajectory: a (2,N) path to the goal
		"""
		N = len(action_plan)
		traj = np.empty((2,N))
		traj[:] = np.nan()
		for idx, action in enumerate(action_plan):
			#TODO is there a difference between matrix coordinates and game coordinates
			dx, dy = world.BugDynamics.get_vector(action)
			traj[:,idx] = traj[1,idx]+dx, traj[2,idx]+dy
			#TODO test this
		return traj

	def show(self):
		"""Display the """
		len_c, len_r  = np.shape(self.walls)
		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)
		major_ticks = np.arange(0.5, 10, 1)
		ax.set_xticks(major_ticks)
		ax.set_yticks(major_ticks)
		ax.grid(which='both')
		ax.grid(which='major', alpha=0.5)

		plt.imshow(data["walls"], aspect='auto', cmap='Greys',interpolation='none', origin='upper')
		plt.scatter(data["start"][0],data["start"][1],c='g',s=300)
		plt.scatter(data["end"][0],data["end"][1],c='r',s=300)
		#TODO display the trajectory
		plt.show()

class Loader:
	@staticmethod
	def get_path(folder,file,suffix):
		script_dir = os.path.dirname(os.path.realpath('__file__'))
		rel_path = 'mazes/'+mazename+'.maze'
		abs_path = os.path.join(script_dir,rel_path)
		return abs_path

class MazeLoader:
	def __init__(self, mazename):
		self.path = Loader.get_path(mazename)
		self.walls = None
		self.start = None
		self.end = None

	def load():
		with open(path) as file_handle:
			lines = file_handle.read().split('\n')
			h,w = len(lines), len(lines[0])
		self.walls = np.empty((h,w))
		self.walls[:] = np.nan
		for r, line in enumerate(lines):
			for c, char in enumerate(line):
				if char == "X":
					walls[r,c] = 1
				elif char == " ":
					walls[r,c] = 0
				elif char == "S":
					walls[r,c] = 0
					start = (c,r)
				elif char == "G":
					print("G", c,r)
					end = (c,r)
					walls[r,c] = 0
				else:
					print('Error reading file')
			if start is None or end is None:
				print('You must specify start or end')

	def get_start(self):
		"""gets the start position in state coordinates"""
		return self.start
	def get_goal(self):
		"""gets the end position in state coordinates"""
		return self.end
	def get_walls(self):
		if not np.any(np.isnan(self.walls)):
			print("Warning one of the cells in the grid is nan")
		return self.walls

def search(mazename,dynamics,searchmethod,searchproblem):
	#maze_name, dynamics, search_method, search_problem
	maze = MazeLoader(mazename)
	maze.load()
	start = maze.get_start()
	goal = maze.get_goal()
	walls = maze.get_walls()
	
	print(maze)
	# #make world instance
	# if dynamics not in dir(world):
	# 	raise AttributeError("dynamics {} is not defined in world.py".format(dynamics))
	# world_class = getattr(world,dynamics)
	# world_instance = world_class(walls)
	
	# #define the searchproblem
	# if searchproblem not in dir(search_problem):
	# 	raise AttributeError("searchproblem {} is not defined in search_problem.py".format(searchmethod))
	# search_problem_class = getattr(search_problem,searchproblem)
	# print(search_problem_class,"search_problem_fn")
	# search_problem_instance = search_problem_class(start, goal, world)

	# #run the search method
	# if searchmethod not in dir(search_method):
	# 	raise AttributeError("searchmethod {} is jnot defined in search_method.py".format(searchmethod))
	# search_method = getattr(search_method,searchmethod)

	# action_plan = search_method(search_problem_instance)

	# #TODO somhow get the visited list into the visualizer
	# visualizer = Visualizer(start,goal,walls,action_plan)
	# visualizer.show()


def readinput(argv):
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("mazename", type=str,
						help="The name of a maze file in the maze folder, excluding .maze suffix")
	parser.add_argument("-m", "--searchmethod", type=str, default="bfs",
						help="The type of search method used")
	parser.add_argument("-p", "--searchproblem", type=str, default = "PointSearch",
					help="The search problem that is being solved")
	parser.add_argument("-d", "--dynamics", type=str, default="BugWorld",
				help="The agents dynamics in the world")
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	options = readinput(sys.argv)
	#print(options)
	search(**vars(options))
	#print(options)
	