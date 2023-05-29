import numpy as np

EDGE_VISIT_COLOR = np.array([1, 0.5, 0.13])


def edge_index_path2color(G, edge_index_path, edge_colors, already_done=0, n=1):
    n_edges = len(edge_index_path)
    step = round(n_edges / n)
    indices = np.arange(already_done, n_edges, step)
    print(indices)
    # Set edge color to red
    edge_colors[edge_index_path[indices]] = EDGE_VISIT_COLOR
    return edge_colors


def node_path2edge_path(node_path):
    res = []
    for i in range(len(node_path) - 1):
        res.append((node_path[i], node_path[i+1]))
    return res


def edge_path2edge_index(G, edge_path):
    edge_idx = dict_edge_index(G)
    res = np.array([edge_idx[edge] for edge in edge_path])
    return res


def node_path2edge_index(G, node_path):
    edge_path = node_path2edge_path(node_path)
    res = edge_path2edge_index(G, edge_path)
    print(res)
    return res


def dict_edge_index(G):
    edge_l = list(G.edges())
    res = dict()
    for u, v in G.edges():
        edge_index = edge_l.index((u, v))
        res[(u, v)] = edge_index
        res[(v, u)] = edge_index
    return res
