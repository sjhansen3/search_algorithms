import enum
import abc
import numpy as np

class Direction(enum.Enum):
    """Direction enum for pacman like motion"""
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
    NE = 4
    NW = 5
    SE = 6
    SW = 7

class VideoGameActions:
    """Static methods for manipulating actions (directions)"""
    vectors = { Direction.NORTH:(0,-1), 
                Direction.SOUTH:(0,1), 
                Direction.EAST:(1,0), 
                Direction.WEST:(-1,0),
                Direction.NE:(1,-1),
                Direction.SE:(1,1),
                Direction.SW:(-1,1),
                Direction.NW:(-1,-1)}

    @staticmethod
    def get_vector(direction):
        """ gets tuple (dx,dy) associated with a NSEW direction enum
            Params
            ---
            direction: Direction enum (e.g. Direction.North)
            Returns
            ---
            vector: a tuple represnting the direction in (x,y) coordinates
        """
        return VideoGameActions.vectors[direction]

    @staticmethod
    def get_direction(vector):
        """ gets the direction associated with a vector by checking for equality. 
        this assumes that (1,0) is the same as (2,0).
        Params
        ---
        vector: a tuple representing a direction e.g. (1,0)
        Returns
        ---
        direction: a direction Enum e.g. Direction.NORTH
        """
        dx, dy = vector
        if dx<0 and dy==0: return Direction.WEST
        if dx>0 and dy==0: return Direction.EAST
        if dx==0 and dy>0: return Direction.NORTH
        if dx==0 and dy<0: return Direction.SOUTH
        
        if dx<0 and dy<0: return Direction.NW
        if dx<0 and dy>0: return Direction.SW
        if dx>0 and dy<0: return Direction.NE
        if dx>0 and dy>0: return Direction.SE
        raise ValueError("vector value {} not allowed".format(vector))
    
    @staticmethod
    def get_trajectory(start, action_list):
		"""Converts an action plan into a trajectory and sets the trajectory
		Params
		---
		action_list: a list of action tuples
        start: a tuple representing the start state
        Returns
        ---
        traj: a (2,N+1) numpy array of states where N is the length of action list
		"""
		N = len(action_list)
		traj = np.empty((2,N+1))
		traj[:] = np.nan
		traj[:,0] = np.asarray(start)
		for idx, action in enumerate(action_list):
			dx, dy = VideoGameActions.get_vector(action)
			traj[:,idx+1] = traj[0,idx]+dx, traj[1,idx]+dy
		return traj

#TODO implement a second search problem, multiple goals perhaps

class World:
    """Abstract world class, defines how states evolve, which states are valid and how cost is assigned"""
    __metaclass__ = abc.ABCMeta
    def __init__(self, actions, obstacles):
        self.actions = actions
        self.obstacles = obstacles
    @abc.abstractmethod
    def is_valid(self, state):
        """ Checks if the state is valid """
        pass
    @abc.abstractmethod
    def get_next(self, state, action):
        """Evolve the dynamics to get the next state"""
        pass
    @abc.abstractmethod
    def get_cost(self, state, action):
        pass

class VideoGameWorld(World):
    """implements a 2D world with NSEW actions"""
    def __init__(self,walls):
        self.actions = list(Direction)
        super(VideoGameWorld,self).__init__(self.actions,walls)
        self.width = len(walls[0])
        self.height = len(walls)
        self.straight_directions = set(list(Direction)[0:3])

    def get_next(self,state,action):
        """evolves the state for a VideoGame like world
        Params
        ---
        action: a Direction enum (NSEW)
        state: the robot position in (x,y) coordinates
        Returns:
        next_state: a tuple representing the resulting state (x,y)
        """
        cur_x, cur_y = state
        dx, dy = VideoGameActions.get_vector(action)
        return (cur_x+dx,cur_y+dy)

    def is_valid(self, state):
        """checks if a state is valid
        Params
        ---
        state: a tuple representing the position of the robot (x,y)
        Returns
        ---
        is_valid: a boolean, True if the position is not inside a wall
        """
       
        col = state[0] #x position is col in matrix
        row = state[1] #y position is row in matrix
        if col >= self.width or row >= self.height:
            return False
        return not self.obstacles[row,col]

    def get_cost(self, state, action):
        """computes the cost for being in state and taking action
        Params
        ---
        state: a tuple representing (x,y) position
        action: a Direction enum
        Returns
        ---
        cost: the distance traveled by the agent
        """
        if action in self.straight_directions:
            return 1
        return 1.41 #sqrt(2) for the diagonal movements

def testVideoGameActions():
    print(VideoGameActions.get_direction((0,1)), "should be NORTH")
    print(VideoGameActions.get_vector(Direction.NORTH), "should be (0,1)")