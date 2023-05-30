import osmnx as ox
import networkx as nx

def to_indirected(multi_graph):
    """
    set directed graph to an indirected graph and remove all the duplicated edges
    arg: nx: networkx.graph
    return: networkx.graph
    """
    # Convert to undirected graph
    undirected_graph = nx.Graph(multi_graph)
    
    # Remove duplicated edges
    undirected_graph = nx.Graph(undirected_graph)
    
    return undirected_graph

def weight_drone(graph):
    """
    weight the graph so the edge weight is the cost
    arg: nx: networkx.graph
    return: networkx.graph
    """
    graph_with_weight = nx.Graph(graph)
    for u, v, data in graph_with_weight.edges(data=True):
        distance = ox.distance.great_circle_vec(
            graph_with_weight.nodes[u]['y'], graph_with_weight.nodes[u]['x'],
            graph_with_weight.nodes[v]['y'], graph_with_weight.nodes[v]['x']
        ).min()
        
        # Set the edge weight 
        data['weight'] = round(distance * 6378.1370 * 0.01, 3) #euros
    
    return graph_with_weight

def shortest_cpp_path(graph):
    """
    find the shortest path that pass in every edge from the graph
    returns the passing order and the cost in a list
    arg: nx: networkx.graph
    return: list(edge) x float
    """
    subgraph = nx.Graph(graph.edges())
    
    # Compute the minimum spanning tree (Steiner tree) of the subgraph
    steiner_tree = nx.algorithms.approximation.steinertree.steiner_tree(subgraph, list(subgraph.nodes()))
    
    # Get the edges in the passing order
    passing_order = list(steiner_tree.edges())
    
    # Compute the cost of the shortest path
    cost = sum([graph[u][v]['weight'] for u, v in passing_order])
    
    return passing_order, cost

def eulerian_path(G):
    """
    G: networkx.graph
    Returrns the list of node representing the eulerian cycle in G

    #pseudo-code not doc
    eulerize G
    find a eulerian path in the eulerized graph
    create a valid edge path containing existing edges in G:
        check the path if an edge existed in G no problem
        if it did not: replace with the shortest path from source to destination of this
        edge that didn't exist using djikstra
    convert to a node list for coloring and consistency
    """
    # DON'T ASK ME IF THE CODE IS ALREADY GOOD, IT ISN'T
    # THESE ARE JUST GENERAL INSTRUCTIONS TO IMPLEMENT
    # DON'T FOLLOW IF IT DOSN'T WORK FOR YOU
    # EACH LINE OF CODE IS TO BE TAKEN AS 'DO SOMETHING RESSEMBLING THAT' NOT 'DO THAT'
    # eulerized = nx.eulerize() # eulerized will add edges to make the graph eulerian
    # eulerian_path = nx.eulerian_path(eulerized) # O(E) apparently, find a path to visit all edges
    # caution this eulerian path contains edge that didn't exist in the original G graph
    # iterate over the path and verify that the edge already existed in the originial G
    # if it did OK, if it didn't change it using djikstra
    # for src, dst in eulerian_path: # maybe iterate with an i and range(len(eulerian_path))
    # try: 
    #   G[src][dst] # good no problem
    # except: 
    #   try:
    #       G[dst][src]  # good no problem
    #   except:
    #       change this src -> dst in eulerian_path to nx.dijkstra_path(G, src, dst)
    # DON'T ASK ABOUT THE REPRESENTATION, 1->3 ISN'T HOW IT IS ACTUALLY CODED
    # example eulerian path is [(1->3),(3->4),(4->2)] but 3->4 didn't exist in the original graph
    # assuming 3->1->4 is a valid path and the shortest from 3 to 4 that actually exists
    # change the path to [(1->3),(3->1),(1->4),(4->2)]
    # NOW change this edge path to a node path
    # [1,3,1,4,2]
    # FIXME
    eulerized = nx.eulerize(G) if (not nx.has_eulerian_path(G)) else G
    
    eulerian_path = list(nx.eulerian_path(eulerized, keys=True))
    return eulerized, eulerian_path


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
    
    # Load Montreal street network
    graph = ox.graph_from_place('Outremont, Montreal, QC, Canada', network_type='drive')

    # Convert directed graph to undirected and remove duplicated edges
    undirected_graph = to_indirected(graph)
    
    # Weight the graph based on edge costs
    weighted_graph = weight_drone(undirected_graph)
    print(nx.get_edge_attributes(weighted_graph, 'weight'))
    shortest_cpp_path(weighted_graph)

def plow_region(region):
    """
    Do every steps for the vehicule path
    arg: region: string
    return: networkx.graph, list(edge) TODO numbers of vehicule, time taken, cost per day, cost per hour
    """
    # Load Montreal street network
    graph = ox.graph_from_place('Outremont, Montreal, QC, Canada', network_type='drive')

    # Convert directed graph to undirected and remove duplicated edges
    undirected_graph = to_indirected(graph)
    
    # Weight the graph based on edge costs
    weighted_graph = weight_drone(undirected_graph)
    print(nx.get_edge_attributes(weighted_graph, 'weight'))
    shortest_cpp_path(weighted_graph)


#drone_recon_montreal()