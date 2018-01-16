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
		if not action_plan:
			print("No solution found to goal")
			action_plan = [world.Direction.EAST]
		self._format_path(action_plan)

	def append_visited(self, state):
		self.visited.append(state)

	def _format_path(self, action_plan):
		"""Converts an action plan into a trajectory and sets the trajectory
		Params
		---
		action_plan: a list of action tuples
		"""
		N = len(action_plan)
		traj = np.empty((2,N))
		traj[:] = np.nan
		traj[:,0] = np.asarray(self.start)
		for idx, action in enumerate(action_plan[:-1]):
			dx, dy = world.BugDynamics.get_vector(action)
			traj[:,idx+1] = traj[0,idx]+dx, traj[1,idx]+dy
		self.traj = traj

	def show(self):
		"""Display the """
		len_c, len_r  = np.shape(self.walls)
		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)
		y_ticks = np.arange(0.5, self.height, 1)
		print(self.width)
		x_ticks = np.arange(0.5, self.width, 1)
		ax.set_xticks(x_ticks)
		ax.set_yticks(y_ticks)
		ax.grid(which='both')
		ax.grid(which='major', alpha=0.5)

		plt.imshow(self.walls, aspect='equal', cmap='Greys',interpolation='none', origin='upper')
		plt.scatter(self.start[0],self.start[1],c='g',s=300)
		plt.scatter(self.goal[0],self.goal[1],c='r',s=300)
		plt.scatter(self.traj[0],self.traj[1],c='y',s=100)
		visited = np.asarray(self.visited).T
		plt.scatter(visited[0],visited[1],c='b')
		#TODO display the trajectory
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

def search(mazename,dynamics,searchmethod,searchproblem):
	#maze_name, dynamics, search_method, search_problem
	maze = MazeLoader(mazename)
	maze.load()
	start = maze.get_start()
	goal = maze.get_goal()
	walls = maze.get_walls()
	print("walls******")
	print(walls)
	#make world instance
	if dynamics not in dir(world):
		raise AttributeError("dynamics {} is not defined in world.py".format(dynamics))
	world_class = getattr(world,dynamics)
	world_instance = world_class(walls)

	visualizer = Visualizer(start,goal,walls)

	#define the searchproblem
	if searchproblem not in dir(search_problem):
		raise AttributeError("searchproblem {} is not defined in search_problem.py".format(searchmethod))
	search_problem_class = getattr(search_problem,searchproblem)
	search_problem_instance = search_problem_class(start, goal, world_instance, visualizer)

	#run the search method
	if searchmethod not in dir(search_method):
		raise AttributeError("searchmethod {} is jnot defined in search_method.py".format(searchmethod))
	search_fn = getattr(search_method,searchmethod)
	action_plan = search_fn(search_problem_instance)

	visualizer.set_action_plan(action_plan)
	visualizer.show()

def testlargemaze(search_problem_instance):
	prob = search_problem_instance
	print(prob.get_successors((9,2)),"EAST,WEST")

def testpointtopointproblem(search_problem_instance):
	print(search_problem_instance.get_successors((1,1)),"EAST and South")
	print(search_problem_instance.get_successors((2,1)),"West")
	print(search_problem_instance.get_successors((2,2)),"North and West")
	print(search_problem_instance.is_goal((1,2)),"true")
	print(search_problem_instance.is_goal((2,2)),"false")

def testBugWorld(world_instance):
	print(world_instance.get_next((0,0),world.Direction.SOUTH), "(0,1)")
	print(world_instance.is_valid((0,0)), "false")
	print(world_instance.is_valid((0,-1)), "false")
	print(world_instance.is_valid((1,1)), "true")
	print(world_instance.get_next((1,1),world.Direction.EAST),"(2,1)")
	print(world_instance.get_next((3,3),world.Direction.EAST),"(4,3)")
	print(world_instance.is_valid((4,3)), "false")

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
	search(**vars(options))
	