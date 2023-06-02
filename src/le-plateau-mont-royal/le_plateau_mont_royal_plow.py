from argparse import ArgumentParser
from pathlib import Path
import pickle
import sys
sys.path.append('..')
from opti import opti
import matplotlib.pyplot as plt
import numpy as np
from utils import *

import osmnx as ox
from graph_manip import eulerian_path

try:
    budget = 1000 #valeur par défaut
    time = 2 #valeur par défaut
    vehicle = 20 #valeur par défaut
    load = False
    
    #Recup les arguments
    parser = ArgumentParser()
    parser.add_argument("--load", required=False, type=str)
    parser.add_argument("--budget", required=False, type=str)
    parser.add_argument("--time", required=False, type=str)
    parser.add_argument("--vehicle", required=False, type=str)
    args = parser.parse_args()
    

    if args.load != "" :     
        load = args.load == "True"
    if args.budget != "" : 
        budget = int(args.budget)
    if args.time != "" :
        time = int(args.time)
    if args.vehicle != "" :
        vehicle = int(args.vehicle)
    
    if  (not load):
        network = ox.graph_from_place("Le Plateau-Mont-Royal, Montreal, QC, Canada", network_type="drive")
        eulerized, path = eulerian_path(network.to_undirected())
        pickle.dump(path, open("../../Le Plateau-Mont-Royal-drone.p", "wb"))
        pickle.dump(eulerized, open("../../Le Plateau-Mont-Royal-eulerized.p", "wb"))
    else :
        eulerized= pickle_load("../../Le Plateau-Mont-Royal-eulerized.p")
        path = pickle_load("../../Le Plateau-Mont-Royal-drone.p")
    
    graph = [opti(time, budget, eulerized, path, n) for n in range(1,vehicle + 1)]
    display_graph(graph, str(budget), str(time), "Le Plateau-Mont-Royal", vehicle + 1)
except FileNotFoundError:
    print("Générer le fichier avant de lancer l'étude")

