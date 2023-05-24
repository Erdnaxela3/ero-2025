def to_indirected(nx):
    """
    set directed graph to an indirected graph and remove all the duplicated edges
    arg: nx: networkx.graph
    return: networkx.graph
    """
    pass

def weight_drone(nx):
    """
    weight the graph so the edge weight is the cost
    arg: nx: networkx.graph
    return: networkx.graph
    """
    pass

def shortest_cpp_path(nx):
    """
    find the shortest path that pass in every edge from the graph
    returns the passing order and the cost in a list
    arg: nx: networkx.graph
    return: list(edge) x float
    """
    pass

def evaluate_solution(cost, time, weights):
    """
    returns the effective cost according to the weigths given for cost and time
    arg: cost: float, time: float, weights: list(weight)
    return: float
    """
    pass

def drone_recon_montreal():
    """
    Do every steps for the drone path
    return: networkx.graph, list(edge) TODO stats
    """
    pass

def plow_region(region):
    """
    Do every steps for the vehicule path
    arg: region: string
    return: networkx.graph, list(edge) TODO numbers of vehicule, time taken, cost per day, cost per hour
    """
    pass
