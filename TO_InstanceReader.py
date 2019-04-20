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


with open('data.json', 'r') as f:
    json_data = json.load(f)


thisSeed = json_data['thisSeed']

noOfTasks = json_data['noOfTasks']
noOfDepots = json_data['noOfDepots']
noOfRobots = json_data['noOfRobots']
K = json_data['K']
T = json_data['T']
D = json_data['D']
S = json_data['S']
E = json_data['E']
N = json_data['N']

L = json_data['L']
vel = json_data['vel']
T_max = json_data['T_max']
R = json_data['R']

T_loc = json_data['T_loc']
T_loc = {k: tuple(v) for k, v in T_loc.items()}

D_loc = json_data['D_loc']
D_loc = {k: tuple(v) for k, v in D_loc.items()}

S_loc = json_data['S_loc']
S_loc = {k: tuple(v) for k, v in S_loc.items()}

E_loc = json_data['E_loc']
E_loc = {k: tuple(v) for k, v in E_loc.items()}

N_loc = json_data['N_loc']
N_loc = {k: tuple(v) for k, v in N_loc.items()}

edges = json_data['edges']
edges = [tuple(n) for n in edges]
c = json_data['c']
c = {tuple(k.split(':')): v for k, v in c.items()}
f = json_data['f']
f = {tuple(k.split(':')): v for k, v in f.items()}

arcs = json_data['arcs']
arcs = [tuple(arc) for arc in arcs]

arc_ub = json_data['arc_ub']
arc_ub = {tuple(k.split(':')): v for k, v in arc_ub.items()}

k_y = json_data['k_y']
k_y = [tuple(arc) for arc in k_y]
