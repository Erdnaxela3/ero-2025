def create_test_graph():
    """
    Returns a networkx graph compatible with osmnx with 4 nodes and 6 edges
    Shaped like a square with diagonals
    edge order is not ordered
    """
    G = nx.Graph()
    G.add_node(0)
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)

    pos = [
        [0,0],
        [1,0],
        [0,1],
        [1,1],
    ]

    G.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    I=nx.MultiDiGraph(G) #step 3

    for i,node in enumerate(I.nodes(data=True)):
        node[1]['x']=pos[i][0]
        node[1]['y']=pos[i][1]

    I.graph={'crs':'epsg:4326'}

    return I