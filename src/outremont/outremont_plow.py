from argparse import ArgumentParser
import argparse
import osmnx as ox
import pickle
import sys

sys.path.append('..')
from graph_manip import eulerian_path
from opti import opti
from utils import pickle_load, display_graph

AREA="Outremont"
MONTREAL_QC = "Montreal, QC, Canada"
FULL_AREA = f"{AREA}, {MONTREAL_QC}"
OSMNX_NETWORK_TYPE = "drive"
DEFAULT_BUDGET = 1000
DEFAULT_TIME = 2
DEFAULT_VEHICLE = 20

if __name__ == '__main__':
    budget = DEFAULT_BUDGET
    time = DEFAULT_TIME
    vehicle = DEFAULT_VEHICLE
    load = False

    #Recup les arguments
    parser = ArgumentParser()
    parser.add_argument("--load", '-l', action=argparse.BooleanOptionalAction)
    parser.add_argument("--budget", '-b', required=False, type=str)
    parser.add_argument("--time", '-t', required=False, type=str)
    parser.add_argument("--vehicle", '-n', required=False, type=str)
    args = parser.parse_args()

    load = args.load
    if args.budget: 
        budget = int(args.budget)
    if args.time:
        time = int(args.time)
    if args.vehicle:
        vehicle = int(args.vehicle)

    if not load:
        network = ox.graph_from_place(FULL_AREA, network_type=OSMNX_NETWORK_TYPE)
        eulerized, path = eulerian_path(network.to_undirected())
        pickle.dump(path, open(f"{AREA}-path.p", "wb"))
        pickle.dump(eulerized, open(f"{AREA}-eulerized.p", "wb"))
    else :
        try:
            eulerized= pickle_load(f"{AREA}-eulerized.p")
            path = pickle_load(f"{AREA}-path.p")
        except FileNotFoundError:
            print("Générer le fichier avant de lancer l'étude")

    graph = [opti(time, budget, eulerized, path, n) for n in range(1,vehicle + 1)]
    display_graph(graph, str(budget), str(time), f"{AREA}", vehicle + 1)