# TODO: Extract information from the combination of instance and solution.
#  That can include functions which extract information such as
# - Given a node, how far is the closest task/depot?
# - Given a node, How far is the farthest task/depot?
# - Given a solution, for each node, did the robot pick a task node or a depot
# node, given the fuel at the node?

from pprint import pprint
import random as rnd
import math
import numpy as np
import os
import regex as re
import csv
from TO_InstanceReader import InstanceReader
from TO_SolutionReader import Solution_Reader


class SolutionInformationExtractor:

    def __init__(self, instance, sol):
        self.instance = instance
        self.sol = sol

    def recharge_recharge_task_frequency(self):
        self.recharge_recharge_count = 0
        self.recharge_task_count = 0
        for k in self.instance.K:
            it1 = iter(self.sol.nodesInOrder[k])
            it2 = iter(self.sol.nodesInOrder[k])
            it2.__next__()
            for n1, n2 in zip(it1, it2):
                if n1 in self.instance.D:
                    if n2 in self.instance.D:
                        self.recharge_recharge_count += 1
                    elif n2 in self.instance.T:
                        self.recharge_task_count += 1
                # Deal the edge cases for start/end nodes here
                if n1 in self.instance.S:
                    if n2 in self.instance.D and n2 not in self.instance.D[0]:
                        self.recharge_recharge_count += 1
                    elif n2 in self.instance.T:
                        self.recharge_task_count += 1

                if n2 in self.instance.E:
                    if n1 in self.instance.D and n1 not in self.instance.D[0]:
                        self.recharge_recharge_count += 1


'''
    def compute_data_filepath(self):
        instance_data_folder_path_suffix = \
            '/data' + \
            '/R' + str(self.noOfRobots) + \
            '/D' + str(self.noOfDepots) + \
            '/T' + str(self.noOfTasks) + \
            '/F' + str(self.L) + \
            '/Tmax' + str(self.T_max)
        instance_data_folder_path = \
            self.path_to_data_folder + instance_data_folder_path_suffix
        instance_data_filename_prefix = \
            '\\R' + str(self.noOfRobots) + \
            'D' + str(self.noOfDepots) + \
            'T' + str(self.noOfTasks) + \
            'F' + str(self.L) + \
            'Tmax' + str(self.T_max) + \
            'Iter' + str(self.iteration)
        self.instance_data_file = os.path.normpath(
            instance_data_folder_path + instance_data_filename_prefix + '.json')

    def compute_sol_filepath(self):
        instance_sol_folder_path_suffix = \
            '/sol' + \
            '/R' + str(self.noOfRobots) + \
            '/D' + str(self.noOfDepots) + \
            '/T' + str(self.noOfTasks) + \
            '/F' + str(self.L) + \
            '/Tmax' + str(self.T_max)
        instance_sol_folder_path = \
            self.path_to_data_folder + instance_sol_folder_path_suffix
        instance_sol_filename_prefix = \
            '\\R' + str(self.noOfRobots) + \
            'D' + str(self.noOfDepots) + \
            'T' + str(self.noOfTasks) + \
            'F' + str(self.L) + \
            'Tmax' + str(self.T_max) + \
            'Iter' + str(self.iteration)
        self.instance_sol_file = os.path.normpath(
            instance_sol_folder_path + instance_sol_filename_prefix + '.sol')
'''


def main():
    instance_prefix = 'R3D2T7F125Tmax175Iter'
    for i in range(5):
        instance_name = instance_prefix + str(i)
        instance = InstanceReader(instance_name)
        sol = Solution_Reader(instance_name)
        pprint(sol.nodesInOrder)
        sol_info = SolutionInformationExtractor(instance, sol)
        sol_info.recharge_recharge_task_frequency()
        print(sol_info.recharge_recharge_count)
        print(sol_info.recharge_task_count)


if __name__ == "__main__":
    main()
