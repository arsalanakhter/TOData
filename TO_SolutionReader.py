from pprint import pprint
from gurobipy import *
import random as rnd
import math
import numpy as np
import os
import regex as re
import csv


class Solution_Reader:

    def __init__(self, instance_string, path_to_data_folder=os.getcwd()):
        temp = [int(s) for s in re.findall(
            '\d+', instance_string)]  # extract numbers
        self.noOfRobots = temp[0]
        self.noOfDepots = temp[1]
        self.noOfTasks = temp[2]
        self.L = temp[3]
        self.T_max = temp[4]
        self.iteration = temp[5]
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
            '\\R' + str(self.noOfRobots) + \
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
        # We'll read it manually, in varibale x
        self.x = {}
        with open(self.instance_sol_file, newline='\n') as csvfile:
            reader = csv.reader((line.replace('  ', ' ')
                                 for line in csvfile), delimiter=' ')
            next(reader)  # skip header
            next(reader)  # skip the best objective value line
            for var, value in reader:
                self.x[var] = float(value)


def main():
    instance = 'R2D1T1F55Tmax50Iter1'
    sol = Solution_Reader(instance)
    pprint(sol.x)


if __name__ == "__main__":
    main()
