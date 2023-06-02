from argparse import ArgumentParser
from pathlib import Path
import pickle
import sys
sys.path.append('..')
from opti import opti
import matplotlib.pyplot as plt
import numpy as np
from utils import *

try:
    el = pickle_load("../../Saint-Léonard-eulerized.p")
    path = pickle_load("../../Saint-Léonard-drone.p")
    budget = 1000 #valeur par défaut
    time = 2 #valeur par défaut
    vehicle = 20 #valeur par défaut
    #Recup les arguments
    parser = ArgumentParser()
    parser.add_argument("--budget", required=False, type=str)
    parser.add_argument("--time", required=False, type=str)
    parser.add_argument("--vehicle", required=False, type=str)
    args = parser.parse_args()
    
    if args.budget != "" : 
        budget = int(args.budget)
    if args.time != "" :
        time = int(args.time)
    if args.vehicle != "" :
        vehicle = int(args.vehicle)

    graph = [opti(time, budget, el, path, n) for n in range(1,vehicle + 1)]
    display_graph(graph, str(budget), str(time), "Saint-Léonard", vehicle + 1)
except FileNotFoundError:
    print("Générer le fichier avant de lancer l'étude")