import matplotlib.pyplot as plt
import numpy as np
import pickle


def display_graph(scores, budget, time, place, max_vehicule, intervalle=1, vehicle_type="T1"):
    # Create x-axis values
    max_score = max(scores)
    min_score = min(scores)
    max_score_index = scores.index(max_score) + 1
    x = range(1, max_vehicule, intervalle)

    plt.plot(x, scores, marker='o')

    plt.xlabel('Nombre de véhicule')
    plt.ylabel('Scores')
    plt.xticks(np.arange(1, max_vehicule, intervalle))
    plt.yticks(np.arange(int(min_score) - 1,
               int(max_score) + 2, 0.4 * intervalle))
    plt.title('Meilleur option Budget = ' + budget +
              ' - Temps = ' + time + ' - Place = ' + place)

    plt.axvline(x=max_score_index, color='r', linestyle='--')
    plt.axhline(y=max_score, color='r', linestyle='--')

    plt.text(1, min(scores) - 0.5, "On remarque que la meilleur option est de " + str(max_score_index) + f" véhicules {vehicle_type} pour " + place + " avec un budget de " + budget + '€ et un temps de ' + time
             + " heures ", fontsize=10, ha='left')
    plt.figtext(0.5, -0.1, 'Text at the bottom', fontsize=10, ha='center')

    plt.savefig("./"+place+"_output.png")
    plt.show()


def pickle_load(file_name):
    with open(file_name, "rb") as file:
        path = pickle.load(file)
        return path
