import numpy as np

EDGE_VISIT_COLOR = np.array([1, 0.5, 0.13])


def edge_index_path2color(edge_index_path, edge_colors, already_done=0, n=1):
    """
    Colorizes edges in a graph based on the given edge index path for a step according
    to the number n of ressources to divided the color work.

    Args:
        edge_index_path (numpy.ndarray): Array of edge indices representing the path.
        edge_colors (numpy.ndarray): Array of edge colors for the graph.
        already_done (int): The starting index for coloring the edges. Defaults to 0.
        n (int): Number of segments to divide the edge coloring work. Defaults to 1.

    Returns:
        numpy.ndarray: Array of edge colors with the specified edges colored.

    Raises:
        None

    """
    n_edges = len(edge_index_path)
    step = round(n_edges / n)
    indices = np.arange(already_done, n_edges, step)
    edge_colors[edge_index_path[indices]] = EDGE_VISIT_COLOR
    return edge_colors


def node_path2edge_path(node_path):
    """
    Converts a node path to an edge path.

    Args:
        node_path (list): List of nodes representing the path.

    Returns:
        list: List of edges representing the path.

    Raises:
        None

    """
    res = []
    for i in range(len(node_path) - 1):
        res.append((node_path[i], node_path[i+1]))
    return res


def edge_path2edge_index(G, edge_path):
    """
    Converts an edge path to an array of edge indices.

    Args:
        G (networkx.Graph): The input graph.
        edge_path (list): List of edges representing the path.

    Returns:
        numpy.ndarray: Array of edge indices representing the path.

    Raises:
        None

    """
    edge_idx = dict_edge_index(G)
    res = np.array([edge_idx[edge] for edge in edge_path])
    return res


def node_path2edge_index(G, node_path):
    """
    Converts a node path to an array of edge indices.

    Args:
        G (networkx.Graph): The input graph.
        node_path (list): List of nodes representing the path.

    Returns:
        numpy.ndarray: Array of edge indices representing the path.

    Raises:
        None

    """
    edge_path = node_path2edge_path(node_path)
    res = edge_path2edge_index(G, edge_path)
    return res


def dict_edge_index(G):
    """
    Creates a dictionary mapping each edge in the graph to its index in G.edges().
    Can be use for colorizing when plotting.

    Args:
        G (networkx.Graph): The input graph.

    Returns:
        dict: Dictionary mapping each edge to its index.

    Raises:
        None

    """
    edge_l = list(G.edges())
    res = dict()
    for u, v in G.edges():
        edge_index = edge_l.index((u, v))
        res[(u, v)] = edge_index
        res[(v, u)] = edge_index
    return res
