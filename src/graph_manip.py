import networkx as nx


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
    eulerized = nx.eulerize(G) if (not nx.has_eulerian_path(G)) else G

    eulerian_path = list(nx.eulerian_path(eulerized, keys=True))

    # duplicated the edges copy their source for plotting purposes
    for u, v, k in eulerian_path:
        if eulerized[u][v][k] == dict():
            g = k - 1
            while eulerized[u][v][g] == dict():
                g = g - 1
            for key, val in eulerized[u][v][g].items():
                eulerized[u][v][k][key] = eulerized[u][v][g][key]

    return eulerized, eulerian_path
