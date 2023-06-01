import matplotlib.pyplot as plt
import numpy as np
import pickle

def display_graph(scores, budget, time, place, max_vehicule) : 
    # Create x-axis values
    max_score = max(scores)
    min_score = min(scores)
    max_score_index = scores.index(max_score)
    x = range(1, max_vehicule)

    plt.plot(x, scores, marker='o')

    plt.xlabel('Nombre de véhicule')
    plt.ylabel('Scores')
    plt.xticks(np.arange(1, max_vehicule))
    plt.yticks(np.arange(int(min_score) - 2, int(max_score) + 2, 0.4))
    plt.title('Graphique meilleur option avec budget ' + budget + ' et un temps ' + time + ' heures pour ' + place)
    
    
    plt.axvline(x= max_score_index, color='r', linestyle='--')
    plt.axhline(y= max_score, color='r', linestyle='--')
    
    plt.text(1, min(scores) - 0.5, 'On remarque que la meilleur option pour un budget de '+ budget + ' et un temps de ' + time
             + " heures est de " + str(max_score_index) + " véhicules pour " + place
             , fontsize=10, ha='left')
    plt.figtext(0.5, -0.1, 'Text at the bottom', fontsize=10, ha='center')

    plt.savefig("./Outremont_output.png")
    plt.show()

def pickle_load(file_name) :
    with open(file_name, "rb") as file:
        path = pickle.load(file)
        return path