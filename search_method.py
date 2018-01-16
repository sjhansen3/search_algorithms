import copy
import util
import math

def generic_treesearch(searchproblem, priority_function):
    """Solve a search tree problem
    Params
    ---
    searchproblem: a searchProblem for which to search over
    priority_function: a function which assigns a priority to a value (higher number means higher priority)
    Returns
    ---
    plan: an optimal sequence of actions to arrive at the goal
    """
    fringe = util.PriorityQueue(priority_function)
    start_state = searchproblem.get_start()

    fringe.push((start_state,[],0))
    expanded = set()

    while not fringe.isEmpty():
        cur_state, cur_plan, cur_cost = fringe.pop()

        if searchproblem.is_goal(cur_state):
            return cur_plan

        if cur_state not in expanded:
            expanded.add(cur_state)
            for state, direction, cost_to_come in searchproblem.get_successors(cur_state):
                if state not in expanded:
                    child_plan = copy.deepcopy(cur_plan) #TODO could this be copy
                    child_plan.append(direction)
                    child_cost_to_come = cur_cost+cost_to_come
                    node = (state, child_plan, child_cost_to_come)
                    #print("adding", state, "to the fringe")
                    fringe.push(node)

    return [] #if there are no more nodes to explore and goal hasn't been found, their is not plan

def bfs_priorityfn(item):
    state, plan, cost_to_come = item
    return len(plan)

def manhattan_distance(state, searchproblem):
    x,y = state
    goal_X, goal_y = searchproblem.get_goal()
    return abs(x-goal_X)+abs(y-goal_y)

def euclidean_distance(State, searchproblem):
    x,y = State
    goal_x, goal_y = searchproblem.get_goal()
    return math.sqrt((x-goal_x)**2+(y-goal_y)**2)

def breadth_first_search(searchproblem):
    return generic_treesearch(searchproblem, bfs_priorityfn)

def a_star_search(searchproblem):
    def a_star_priorityfn(item):
        state, plan, cost_to_come = item
        return cost_to_come + manhattan_distance(state, searchproblem)

    return generic_treesearch(searchproblem,a_star_priorityfn)

bfs = breadth_first_search
astar = a_star_search