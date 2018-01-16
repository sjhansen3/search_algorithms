import numpy as np
import os
import matplotlib.pyplot as plt
import sys
import search_problem
import search_method
import world
import visualization

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

def testVideoGameWorld(world_instance):
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
	parser.add_argument("-d", "--dynamics", type=str, default="VideoGameWorld",
				help="The agents dynamics in the world")
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	options = readinput(sys.argv)
	search(**vars(options))
	