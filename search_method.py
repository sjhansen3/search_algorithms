import copy
import util
import search_problem #TODO is thi needed?

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

        if(searchproblem.is_goal(cur_state)):
            return cur_plan

        if cur_state not in expanded:
            expanded.add(cur_state)
            #print "expanding", (currentState, currentPlan, currentWeight)
            for state, direction, cost_to_come in searchproblem.get_successors(cur_state):
                if state not in expanded:
                    child_plan = copy.deepcopy(cur_plan) #TODO could this be copy
                    child_plan.append(direction)
                    child_cost_to_come = cur_cost+cost_to_come
                    node = (state, child_plan, child_cost_to_come)
                    #print "adding", node, "to the fringe with priority ", fringe.priorityFunction(node)
                    fringe.push(node)

    return [] #if there are no more nodes to explore and goal hasn't been found, their is not plan

def bfs_priorityfn(item):
    state, plan, cost_to_come = item
    return len(plan)

# def manhattan_heuristic(item):
#     state, plan, cost_to_come = item
#     return cost_to_come+

def breadth_first_search(searchproblem):
    return generic_treesearch(searchproblem, bfs_priorityfn)

# def a_star_search(searchproblem):
#     return generic_treesearch(searchproblem,)

