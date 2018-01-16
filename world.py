import enum
import abc

class Direction(enum.Enum):
    """Direction enum for pacman like motion"""
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
    STOP = 4

class BugDynamics:
    """Static methods for manipulating Directions"""
    vectors = { Direction.NORTH:(0,-1), 
                Direction.SOUTH:(0,1), 
                Direction.EAST:(1,0), 
                Direction.WEST:(-1,0), 
                Direction.STOP:(0,0)}

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
        return BugDynamics.vectors[direction]

    @staticmethod
    def reverse_direction(direction):
        """ reverses an enum Direction, e.g. North-> South, West->East
        Params
        ---
        direction: a direction Enum
        Returns
        ---
        reversed direction: a reversided Direction enum
        """
        if direction==Direction.NORTH: return Direction.SOUTH
        if direction==Direction.SOUTH: return Direction.NORTH
        if direction==Direction.EAST: return Direction.WEST
        if direction==Direction.WEST: return Direction.EAST
        if direction==Direction.STOP: return Direction.STOP

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
        if dx<0: return Direction.WEST
        if dx>0: return Direction.EAST
        if dy>0: return Direction.NORTH
        if dy<0: return Direction.SOUTH
        if dx==0 and dy==0:
            return Direction.STOP
    @staticmethod
    def state_to_col(vector):
        #TODO converst state to 
        pass
#TODO implement a second search problem, multiple goals perhaps

class World:
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

#TODO implement a second world, with more complicated dynamics or states

class BugWorld(World):
    """implements a 2D world with NSEW actions"""
    def __init__(self,walls):
        self.actions = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
        super(BugWorld,self).__init__(self.actions,walls)
        self.width = len(walls[0])
        self.height = len(walls)

    def get_next(self,state,action):
        """Evolve the state for a bug
        Params
        ---
        action: a Direction enum (NSEW)
        state: the robot position in (x,y) coordinates
        Returns:
        next_state: a tuple representing the resulting state (x,y)
        """
        cur_x, cur_y = state
        dx, dy = BugDynamics.get_vector(action)
        return (cur_x+dx,cur_y+dy)

    def is_valid(self, state):
        """Checks if a state is valid
        Params
        ---
        state: a tuple representing the position of the robot (x,y)
        Returns
        ---
        is_valid: a boolean, True if the position is not inside a wall
        """
        #TODO this isnt correct - which way is positive y for a matrix
        # which way is positive y for an image
        
        col = state[0] #x position is col in matrix
        row = state[1] #y position is row in matrix
        if col >= self.width or row >= self.height:
            return False
        return not self.obstacles[row,col]

    def get_cost(self, state, action):
        """compute the cost for being in state and taking action
            Params
            ---
            state: a tuple representing (x,y) position
            action: a Direction enum
            Returns
            ---
            cost: always 1, regardless of the action
        """
        return 1

def testBugDynamics():
    print(BugDynamics.reverse_direction(Direction.SOUTH), "should be NORTH")
    print(BugDynamics.get_direction((0,1)), "should be NORTH")
    print(BugDynamics.get_vector(Direction.NORTH), "should be (0,1)")