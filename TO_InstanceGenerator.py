import random as rnd
import math
import numpy as np
import os
import sys
import json


class Instance_Generator:

    def __init__(self, no_of_robots, no_of_depots, no_of_tasks, fuel, Tmax,
                 no_of_instances=1, seed_list=[rnd.randrange(sys.maxsize)],
                 path_to_data_folder=os.getcwd()):
        self.noOfRobots = no_of_robots
        self.noOfTasks = no_of_tasks
        self.noOfDepots = no_of_depots
        self.L = fuel
        self.T_max = Tmax
        self.vel = 1
        self.no_of_instances = no_of_instances
        if len(seed_list) == no_of_instances:
            self.seed_list = seed_list
        elif len(seed_list) == 1:
        # Handling the case if only no_of_instances are provided
            self.seed_list = []
            for i in range(self.no_of_instances):
                self.seed_list.append(rnd.randrange(sys.maxsize))
        else:
            raise Exception('Number of instances not equal to number of seeds.')
        self.instance_folder_path_suffix = \
            '/data' + \
            '/R' + str(self.noOfRobots) + \
            '/D' + str(self.noOfDepots) + \
            '/T' + str(self.noOfTasks) + \
            '/F' + str(self.L) + \
            '/Tmax' + str(self.T_max)
        self.instance_folder_path = os.path.normpath(
            path_to_data_folder + self.instance_folder_path_suffix)
        self.instance_filename_prefix = '\\R' + str(self.noOfRobots) + \
                                        'D' + str(self.noOfDepots) + \
                                        'T' + str(self.noOfTasks) + \
                                        'F' + str(self.L) + \
                                        'Tmax' + str(self.T_max)

    def create_instance(self, iteration, seed):
        self.iteration = iteration
        self.thisSeed = seed
        rnd.seed(self.thisSeed)
        self.K = ["K" + str(i) for i in range(self.noOfRobots)]
        self.T = ["T" + str(i) for i in range(self.noOfTasks)]
        self.D = ["D" + str(i) for i in range(self.noOfDepots)]
        self.S = ['S0']
        self.E = ['E0']
        self.N = self.T + self.D + self.S + self.E

        # R = {task: 1 for task in T}

        self.T_loc = {task: (100*rnd.random(), 100*rnd.random())
                      for task in self.T}
        self.D_loc = {loc: (100*rnd.random(), 100*rnd.random())
                      for loc in self.D}
        self.S_loc = {loc: self.D_loc['D0'] for loc in self.S}
        self.E_loc = {loc: self.D_loc['D0'] for loc in self.E}
        self.N_loc = {**self.T_loc, **self.D_loc, **self.S_loc, **self.E_loc}

        self.edges = [(i, j) for i in self.N for j in self.N if i != j]
        self.c = {t: np.linalg.norm(
            np.array(self.N_loc.get(t[0]))-np.array(self.N_loc.get(t[1])))
            for t in iter(self.edges)}
        self.f = self.c  # Just for consistency with the paper

        self.arcs = [(i, j, k)
                     for i in self.N for j in self.N for k in self.K if i != j]
        self.arc_ub = {
            (i, j, k): 1 for i in self.N for j in self.N for k in self.K if i != j}
        for arc in self.arc_ub:
            if arc[0] in self.D and arc[1] in self.D:
                self.arc_ub[arc] = self.noOfTasks
        self.k_y = [(i, k) for i in self.T for k in self.K]

    def create_json_data(self):
        self.json_data = {
            'iteration': self.iteration,
            'thisSeed': self.thisSeed,
            'noOfTasks': self.noOfTasks,
            'noOfDepots': self.noOfDepots,
            'noOfRobots': self.noOfRobots,
            'K': self.K,
            'T': self.T,
            'D': self.D,
            'S': self.S,
            'E': self.E,
            'N': self.N,

            'L': self.L,
            'vel': self.vel,
            'T_max': self.T_max,
            # 'R': self.R,

            'T_loc': self.T_loc,
            'D_loc': self.D_loc,
            'S_loc': self.S_loc,
            'E_loc': self.E_loc,
            'N_loc': self.N_loc,

            'edges': self.edges,
            'c': dict((':'.join(k), v) for k, v in self.c.items()),
            'f': dict((':'.join(k), v) for k, v in self.f.items()),

            'arcs': [[arc[0], arc[1], arc[2]] for arc in self.arcs],
            'k_y': self.k_y,
            'arc_ub': dict((':'.join(k), v) for k, v in self.arc_ub.items())
        }

    def write_instance_to_json(self):
        curr_instance_filename = self.instance_filename_prefix + \
            'Iter' + str(self.iteration) + '.json'
        file_path = os.path.normpath(
            self.instance_folder_path+curr_instance_filename)

        if not os.path.exists(self.instance_folder_path):
            os.makedirs(self.instance_folder_path)

        with open(file_path, 'w') as fp:
            json.dump(self.json_data, fp, sort_keys=True, indent=4)

    def generate_data(self):
        for iteration, seed in zip(range(self.no_of_instances), self.seed_list):
            self.create_instance(iteration, seed)
            self.create_json_data()
            self.write_instance_to_json()


def main():
    min_robots = 2
    max_robots = 3

    min_depots = 2
    max_depots = 3

    min_tasks = 5
    max_tasks = 10

    fuel_range_start = 150
    fuel_range_step = 100
    # fuel_range_end = int(math.ceil(2*100*math.sqrt(2) /
    #                               fuel_range_step)*fuel_range_step)  # ~282
    fuel_range_end = 150

    Tmax_range_start = 600
    Tmax_range_step = 100
    # Tmax_range_end = int(math.ceil(2*100*math.sqrt(2) /
    #                               Tmax_range_step)*Tmax_range_step)  # ~282
    Tmax_range_end = 600

    robots_range = list(range(min_robots, max_robots+1))
    depots_range = list(range(min_depots, max_depots+1))
    #tasks_range = list(range(min_tasks, max_tasks+1))
    tasks_range = [5, 10]
    #fuel_range = list(range(fuel_range_start, fuel_range_end +
    #                        fuel_range_step, fuel_range_step))
    fuel_range = [50,75,150]
    #Tmax_range = list(range(Tmax_range_start, Tmax_range_end +
    #                        Tmax_range_step, Tmax_range_step,))
    Tmax_range = [150,300,600]

    no_of_instances = 10
    # Create a list of seeds
    list_of_seeds = [rnd.randrange(sys.maxsize) for i in range(no_of_instances)]

    for r in robots_range:
        for d in depots_range:
            for t in tasks_range:
                for f in fuel_range:
                    for tmax in Tmax_range:
                        instance = Instance_Generator(
                            r, d, t, f, tmax, no_of_instances, list_of_seeds)
                        instance.generate_data()


if __name__ == "__main__":
    main()
