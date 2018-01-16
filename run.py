import numpy as np
import os
import matplotlib.pyplot as plt
import sys
import search_problem
import search_method
import world
import visualization
import util

class Search:
    """create and run a search as specified by the user"""
    def __init__(self, mazename, world, searchmethod, searchproblem):
        self.maze_name = mazename
        self.world = world
        self.search_method = searchmethod
        self.search_problem = searchproblem
    
    def run(self):
        """run the search """
        #load the maze from file
        maze = visualization.MazeLoader(self.maze_name)
        maze.load()
        start = maze.get_start()
        goal = maze.get_goal()
        walls = maze.get_walls()
        print("walls******")
        print(walls)

        # create a world from user input which defines how states evolve
        # which states are valid and how cost is assigned
        world_class = util.get_class(world, self.world)
        world_instance = world_class(walls)

        # create visualizer to visualize the search problem and solution
        visualizer = visualization.Visualizer(start, goal, walls)

        # create a search problem to run the search on
        search_problem_class = util.get_class(search_problem, self.search_problem)
        search_problem_instance = search_problem_class(start, goal, world_instance, visualizer)

        # pick the search algorithm to use
        search_fn = util.get_class(search_method, self.search_method)
        action_plan = search_fn(search_problem_instance)

        # visualize the solution to the search algorithm
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

def readinput():
    """Read the input from the command line"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("mazename", type=str,
                        help="The name of a maze file in the maze folder, excluding .maze suffix")
    parser.add_argument("-m", "--searchmethod", type=str, default="bfs",
                        help="The type of search method used e.g. (bfs, astar)")
    parser.add_argument("-p", "--searchproblem", type=str, default = "PointSearch",
                    help="The search problem that is being solved, must be in search_method.py")
    parser.add_argument("-w", "--world", type=str, default="VideoGameWorld",
                help="The agents world in world.py, defines how states evolve, which states are valid and how cost is assigned")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    options = readinput()
    search = Search(**vars(options))
    search.run()