import numpy as np
import osmnx as ox
import pickle
import matplotlib.pyplot as plt

from cost import PlowCost
from report import PlowReport
from graph_manip import eulerian_path

VEHICULE_1 = [500,1.1,1.1,1.3,10]
VEHICULE_2 = [800,1.3,1.3,1.5,20]

def create_config(fix_cost, km_cost, h_cost, overtime_h_cost, overtime_h_lim, speed, eulerized, path, number_of_vehicules):
    costs = PlowCost(fix_cost, km_cost, h_cost, overtime_h_cost, overtime_h_lim, speed)

    r = PlowReport(costs)

    r.create_report(eulerized, path, number_of_vehicules)
    return r

def opti(time, money, eulerized, path, nbr_vehicules):

    time_coef = 0.6
    money_coef = 0.4

    r = create_config(VEHICULE_1[0],VEHICULE_1[1],VEHICULE_1[2],VEHICULE_1[3],8,VEHICULE_1[4], eulerized, path, nbr_vehicules)

    operation_hours = r.report['operation_duration']
    total_cost = r.report['total_cost']

    indice = (time_coef * (time - operation_hours) + money_coef * (money - total_cost) / money)
    return indice