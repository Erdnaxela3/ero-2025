import networkx as nx

def dfs_edge_path(graph, visited_edges, path):
    last_v = None
    for u,v,k in graph.edges(keys=True):
        if (u,v,k) not in visited_edges:
            if last_v is not None:
                sp = nx.shortest_path(graph, last_v, u)
                spe = []
                for i in range(len(sp) - 1):
                    path_e = (sp[i], sp[i + 1], 0)
                    spe.append(path_e)
                    visited_edges.add(path_e)
                path += spe

            visited_edges.add((u,v,k))
            path.append((u,v,k))
            last_v = v
        

def find_edge_path(graph):
    # Initialize visited edges set to keep track of visited edges
    visited_edges = set()

    # Choose an arbitrary starting node

    # Perform DFS traversal to find the edge path
    path = []
    dfs_edge_path(graph, visited_edges, path)

    return path

def eulerian_path(G):
    """
    Computes the Eulerian path in a given graph.

    Parameters:
        G (networkx.Graph): The input graph.

    Returns:
        tuple: A tuple containing the modified graph and the Eulerian path.

    Notes:
        - If the input graph is not Eulerian (does not contain an Eulerian path), the graph is first
          modified using the `nx.eulerize` function.
        - The modified graph and the corresponding Eulerian path are returned as a tuple.
        - The duplicated edge done by eulerize creates an additional edge with an empty dict as information.
          The edges in the modified graph are duplicated by copying their source for plotting purposes.
    """
    if len(G.nodes()) > 4000:
        eulerized = G
        eulerian_path = find_edge_path(G)
    else:
        for u,v,k in G.edges(keys=True):
            G[u][v][k]['weight'] = G[u][v][k]['length']

        eulerized = nx.eulerize(G) if (not nx.has_eulerian_path(G)) else G

        eulerian_path = list(nx.eulerian_path(eulerized, keys=True))
    # duplicated the edges copy their source for plotting purposes

    for u, v, k in eulerian_path:
        print(eulerized[u][v])
        print(u,v,k)
        if eulerized[u][v][k] == dict():
            g = k - 1
            while eulerized[u][v][g] == dict():
                g = g - 1
            for key,_ in eulerized[u][v][g].items():
                eulerized[u][v][k][key] = eulerized[u][v][g][key]

    return eulerized, eulerian_path
