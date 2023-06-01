import pickle

import sys
sys.path.append('..')

from opti import opti
with open("Outremont-eulerized.p", "rb") as file:
    el = pickle.load(file)

with open("Outremont-drone.p", "rb") as file:
    path = pickle.load(file)

scores = [opti(2,1000, el, path, n) for n in range(1,len(path))]
max_score = max(scores)
print(scores)
print(scores.index(max_score))