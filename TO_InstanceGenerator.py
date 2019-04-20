from gurobipy import *
import random as rnd
import math
import numpy as np
import pickle
import glob
import os
import glob
import sys
import json

thisSeed = rnd.randrange(sys.maxsize)

noOfTasks = 5
noOfDepots = 5
noOfRobots = 3
K = ["K" + str(i) for i in range(noOfRobots)]
T = ["T" + str(i) for i in range(noOfTasks)]
D = ["D" + str(i) for i in range(noOfDepots)]
S = ['S0']
E = ['E0']
N = T + D + S + E

L = 150
vel = 1
T_max = 300
R = {task: 1 for task in T}

T_loc = {task: (100*rnd.random(), 100*rnd.random()) for task in T}
D_loc = {loc: (100*rnd.random(), 100*rnd.random()) for loc in D}
S_loc = {loc: D_loc['D0'] for loc in S}
E_loc = {loc: D_loc['D0'] for loc in E}
N_loc = {**T_loc, **D_loc, **S_loc, **E_loc}

edges = [(i, j) for i in N for j in N if i != j]
c = {t: np.linalg.norm(
    np.array(N_loc.get(t[0]))-np.array(N_loc.get(t[1]))) for t in iter(edges)}
f = c  # Just for consistency with the paper

arcs = [(i, j, k) for i in N for j in N for k in K if i != j]
arc_ub = {(i, j, k): 1 for i in N for j in N for k in K if i != j}
for arc in arc_ub:
    if arc[0] in D and arc[1] in D:
        arc_ub[arc] = noOfTasks
    if arc[0] in E and arc[1] in S:
        arc_ub[arc] = 0  # You cannot go from end to start
k_y = [(i, k) for i in T for k in K]


json_data = {
    'thisSeed': thisSeed,
    'noOfTasks': noOfTasks,
    'noOfDepots': noOfDepots,
    'noOfRobots': noOfRobots,
    'K': K,
    'T': T,
    'D': D,
    'S': S,
    'E': E,
    'N': N,

    'L': L,
    'vel': vel,
    'T_max': T_max,
    'R': R,

    'T_loc': T_loc,
    'D_loc': D_loc,
    'S_loc': S_loc,
    'E_loc': E_loc,
    'N_loc': N_loc,

    'edges': edges,
    'c': dict((':'.join(k), v) for k, v in c.items()),
    'f': dict((':'.join(k), v) for k, v in f.items()),

    'arcs': [[arc[0], arc[1], arc[2]] for arc in arcs],
    'k_y': k_y,
    'arc_ub': dict((':'.join(k), v) for k, v in arc_ub.items())
}
with open('data.json', 'w') as fp:
    json.dump(json_data, fp, sort_keys=True, indent=4)
