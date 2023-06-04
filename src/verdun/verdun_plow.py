from argparse import ArgumentParser
import argparse
import osmnx as ox
import pickle
import sys

sys.path.append('..')
from utils import pickle_load, display_graph
from opti import opti
from graph_manip import eulerian_path
from cost import VehicleT1Cost, VehicleT2Cost
from report import PlowReport

AREA = "Verdun"
MONTREAL_QC = "Montreal, QC, Canada"
FULL_AREA = f"{AREA}, {MONTREAL_QC}"
OSMNX_NETWORK_TYPE = "drive"
DEFAULT_BUDGET = 1000
DEFAULT_TIME = 2
DEFAULT_VEHICLE = 20


def create_and_save(eulerized, path, cost, filename, n=1):
    reportT1 = PlowReport(cost, n)
    reportT1.create_report(eulerized, path, n)
    reportT1.save(filename)


def optimal_vehicle(eulerized, path, time, budget, vehicle=1):
    graph = [opti(time, budget, eulerized, path, n)
             for n in range(1, vehicle + 1)]
    display_graph(graph, str(budget), str(time), f"{AREA}", vehicle + 1)


def need_upgrading(eulerized, path, time, budget, n=1):
    create_and_save(eulerized, path, VehicleT1Cost(), f"{AREA}-{n}-T1.json", n)
    create_and_save(eulerized, path, VehicleT2Cost(), f"{AREA}-{n}-T2.json", n)
    scoreT1 = opti(time, budget, eulerized, path, n, "T1")
    scoreT2 = opti(time, budget, eulerized, path, n, "T2")

    return scoreT1 >= scoreT2


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
    parser.add_argument("--budget", '-b', required=False, type=str)
    parser.add_argument("--time", '-t', required=False, type=str)
    parser.add_argument("--vehicle", '-n', required=False, type=str)
    parser.add_argument("--optimal", action="store_true")
    parser.add_argument("--upgrade", nargs=1)
    parser.add_argument("--report", nargs=2)
    args = parser.parse_args()

    load = args.load
    budget = int(args.budget) if args.budget else DEFAULT_BUDGET
    time = int(args.time) if args.time else DEFAULT_TIME
    vehicle = int(args.vehicle) if args.vehicle else DEFAULT_VEHICLE

    eulerized, path = loading_graph_and_path()

    if args.optimal:
        optimal_vehicle(eulerized, path, time, budget, vehicle)
    elif args.upgrade:
        vehicle = int(args.upgrade[0])
        need = need_upgrading(eulerized, path, time, budget, vehicle)
        if need:
            print("We suggest upgrading to T2 vehicle.")
        else:
            print("We suggest keeping the T1 vehicle.")
    elif args.report:
        n, vehicle_type = args.report
        n = int(n)
        if vehicle_type == "T1":
            cost = VehicleT1Cost()
        elif vehicle_type == "T2":
            cost = VehicleT2Cost()
        else:
            raise ValueError("Invalid vehicle type. Expected T1 or T2")
        reporting(eulerized, path, cost, n, vehicle_type)