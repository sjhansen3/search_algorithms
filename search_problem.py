import abc
from enum import Enum

#class searchProblemFactory

class searchProblem:
    """Abstract class for a search problem """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_start(self):
        pass
    @abc.abstractmethod
    def is_goal(Self):
        pass
    @abc.abstractmethod
    def get_successors(Self):
        pass

class PointSearch(searchProblem):
    def __init__(self, start, goal, world_instance, visualizer):
        """Initializes a point search problem with a single goal and start state
        Params
        ---
        start: a general start state
        goal: a general goal state
        world: a World to evolve state and check for collision
        """
        self.goal = goal
        self.start = start
        self.world_instance = world_instance
        self.visualizer = visualizer

    def get_start(self):
        """Returns the start state for the search problem"""
        return self.start

    def get_goal(self):
        return self.goal
    
    def get_successors(self, state):
        """finds all valid successors of a state
        Params
        ---
        state: a generic state representign the state of the world
        Returns:
        successors: a list of successors #TODO should this be a set
        """

        successors = []
        for action in self.world_instance.actions:
            next_state = self.world_instance.get_next(state, action)
            if self.world_instance.is_valid(next_state):
                cost = self.world_instance.get_cost(state,action)
                successors.append((next_state, action, cost))
        return successors

    def is_goal(self, state):
        """A goal test to check if the goal is reached. for a simple point search this 
        is when the state is the goal state.
        Params
        ---
        state: a generic state
        Returns
        ---
        isGoal: boolean, true if the state is the goal
        """
        self.visualizer.append_visited(state)
        return self.goal==state
