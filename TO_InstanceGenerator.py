import random as rnd
import math
import numpy as np
import os
import sys
import json


class Instance_Generator:

    def __init__(self, no_of_robots, no_of_depots, no_of_tasks, fuel, Tmax,
                 no_of_instances=1, path_to_data_folder=os.getcwd()):
        self.noOfRobots = no_of_robots
        self.noOfTasks = no_of_tasks
        self.noOfDepots = no_of_depots
        self.L = fuel
        self.T_max = Tmax
        self.vel = 1
        self.no_of_instances = no_of_instances
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

    def create_instance(self, iteration):
        self.iteration = iteration
        self.thisSeed = rnd.randrange(sys.maxsize)
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
        for iteration in range(self.no_of_instances):
            self.create_instance(iteration)
            self.create_json_data()
            self.write_instance_to_json()


def main():
    min_robots = 3
    max_robots = 3

    min_depots = 3
    max_depots = 3

    min_tasks = 7
    max_tasks = 7

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
    tasks_range = list(range(min_tasks, max_tasks+1))
    fuel_range = list(range(fuel_range_start, fuel_range_end +
                            fuel_range_step, fuel_range_step))
    Tmax_range = list(range(Tmax_range_start, Tmax_range_end +
                            Tmax_range_step, Tmax_range_step,))

    no_of_instances = 5

    for r in robots_range:
        for d in depots_range:
            for t in tasks_range:
                for f in fuel_range:
                    for tmax in Tmax_range:
                        instance = Instance_Generator(
                            r, d, t, f, tmax, no_of_instances)
                        instance.generate_data()


if __name__ == "__main__":
    main()
