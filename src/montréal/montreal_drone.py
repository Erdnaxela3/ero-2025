from argparse import ArgumentParser
import argparse
import osmnx as ox
import pickle
import sys

sys.path.append('..')
from utils import pickle_load, display_graph
from opti import opti
from graph_manip import eulerian_path
from cost import ClassicDroneCost
from report import DroneReport

AREA = "Montreal"
MONTREAL_QC = "QC, Canada"
FULL_AREA = f"{AREA}, {MONTREAL_QC}"
OSMNX_NETWORK_TYPE = "drive"


def create_and_save(eulerized, path, filename):
    costs = ClassicDroneCost()
    report = DroneReport(costs)
    report.create_report(eulerized, path)
    report.save(filename)

def reporting(eulerized, path, cost, n=1, type="T1"):
    create_and_save(eulerized, path, cost, f"{AREA}-{n}-{type}.json", n)


def loading_graph_and_path():
    if not load:
        network = ox.graph_from_place(
            FULL_AREA, network_type=OSMNX_NETWORK_TYPE)
        eulerized, path = eulerian_path(network.to_undirected())
        pickle.dump(path, open(f"{AREA}-path.p", "wb"))
        pickle.dump(eulerized, open(f"{AREA}-eulerized.p", "wb"))
    else:
        try:
            eulerized = pickle_load(f"{AREA}-eulerized.p")
            path = pickle_load(f"{AREA}-path.p")
        except FileNotFoundError:
            raise Exception(
                f"Please use --load or -l only if {AREA}-path.p and {AREA}-eulerized.p have been generated")

    return eulerized, path


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--load", '-l', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    load = args.load

    eulerized, path = loading_graph_and_path()
    create_and_save(eulerized, path, f"{AREA}-path.json")