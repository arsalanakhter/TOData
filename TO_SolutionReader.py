from pprint import pprint
from gurobipy import *
import random as rnd
import math
import numpy as np
import os
import regex as re
import csv
import networkx as nx


class Solution_Reader:

    def __init__(self, instance_string, path_to_data_folder=os.getcwd()):
        temp = [int(s) for s in re.findall(
            '\d+', instance_string)]  # extract numbers
        self.formulationNo = temp[0]
        self.noOfRobots = temp[1]
        self.noOfDepots = temp[2]
        self.noOfTasks = temp[3]
        self.L = temp[4]
        self.T_max = temp[5]
        # It should ideally be read from file, but lets just go ahead for now
        self.K = ["K" + str(i) for i in range(self.noOfRobots)]
        self.T = ["T" + str(i) for i in range(self.noOfTasks)]
        self.D = ["D" + str(i) for i in range(self.noOfDepots)]
        self.S = ['S0']
        self.E = ['E0']
        self.N = self.K + self.T + self.D + self.S + self.E
        # ------------------------------------------------------------------
        self.iteration = temp[6]
        self.vel = 1
        self.instance_folder_path_suffix = \
            '/sol' + \
            '/R' + str(self.noOfRobots) + \
            '/D' + str(self.noOfDepots) + \
            '/T' + str(self.noOfTasks) + \
            '/F' + str(self.L) + \
            '/Tmax' + str(self.T_max)
        self.instance_folder_path = \
            path_to_data_folder + self.instance_folder_path_suffix
        self.instance_filename_prefix = \
            '/F' + str(self.formulationNo) + \
            'R' + str(self.noOfRobots) + \
            'D' + str(self.noOfDepots) + \
            'T' + str(self.noOfTasks) + \
            'F' + str(self.L) + \
            'Tmax' + str(self.T_max) + \
            'Iter' + str(self.iteration)
        # self.instance_lp_file = os.path.normpath(
        #    self.instance_folder_path + self.instance_filename_prefix + '.lp')
        self.instance_sol_file = os.path.normpath(
            self.instance_folder_path + self.instance_filename_prefix + '.sol')
        # self.model = read(self.instance_lp_file)
        # It seems gurobi cannot read the sol file in the above model
        # We'll read it manually, in varibale sol
        self.sol = {}
        with open(self.instance_sol_file, newline='\n') as csvfile:
            reader = csv.reader((line.replace('  ', ' ')
                                 for line in csvfile), delimiter=' ')
            next(reader)  # skip header
            next(reader)  # skip the best objective value line
            for line in reader:
                if len(line) == 2:
                    var = line[0]
                    value = line[1]
                    self.sol[var] = float(value)
                else:
                    _, self.runtime = line[0].split(':')

    def copmute_arcs_in_order(self):
        self.finalArcs = {k: [] for k in self.K}
        self.remainingFuel = {t: 0 for t in self.T}
        for i in self.sol:
            if self.sol[i] >= 0.9 and i[0] == 'x':
                x, y, k = i.split(',')
                x = x.replace("x[", "")
                k = k.replace("]", "")
                for q in range(math.ceil(self.sol[i])):
                    self.finalArcs[k].append((x, y))
            if self.sol[i] >= 0.9 and i[0] == 'r':
                x, y = i.split('[')
                y = y.replace("]", "")
                self.remainingFuel[y] = self.sol[i]

        # Create a grpah for each robot
        G = {k: nx.MultiDiGraph() for k in self.K}
        # Add all nodes in the graph for each robot
        for k in self.K:
            G[k].add_nodes_from(self.N)
            G[k].add_edges_from(self.finalArcs[k])
            #print("Nodes in G["+k+"]: ", G[k].nodes(data=True))
            #print("Edges in G["+k+"]: ", G[k].edges(data=True))
        # Now compute the paths in the above graphs
        self.arcsInOrder = {k: [] for k in self.K}
        tempArcsInOrder = {k: [] for k in self.K}
        for k in self.K:
            tempArcsInOrder[k] = list(nx.edge_dfs(G[k], source=self.S[0]))
            for arc in tempArcsInOrder[k]:
                newArc = tuple((arc[0], arc[1]))
                self.arcsInOrder[k].append(newArc)

    def convert_to_nodes_in_order(self):
        self.nodesInOrder = {k: [] for k in self.K}
        for k in self.K:
            nodeBasedPath = [arc[0] for arc in self.arcsInOrder[k]]
            nodeBasedPath.append(self.arcsInOrder[k][-1][1])
            self.nodesInOrder[k] = nodeBasedPath[:]


def main():
    instance_prefix = 'F1R3D2T5F50Tmax150Iter'

    for i in range(5):
        instance = instance_prefix + str(i)
        sol = Solution_Reader(instance)
        print(sol.runtime)


if __name__ == "__main__":
    main()
