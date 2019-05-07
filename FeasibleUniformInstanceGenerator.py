from TO_InstanceGenerator import Instance_Generator
import os
import random as rnd
import numpy as np


class Feasible_Uniform_Instance_Generator(Instance_Generator):

    def __init__(self, no_of_robots, no_of_depots, no_of_tasks, fuel, Tmax,
                 no_of_instances=1, path_to_data_folder=os.getcwd()):

        Instance_Generator.__init__(self, no_of_robots, no_of_depots,
                                    no_of_tasks, fuel, Tmax, no_of_instances,
                                    path_to_data_folder)

    def create_feasible_uniform_instance(self, iteration):
        self.create_instance(iteration)
        # First check each depot node can be reached from another depot.
        for d1 in self.D:
            for d2 in self.D:
                if d1 != d2:
                    dist = self.compute_distance(
                        self.D_loc[d1], self.D_loc[d2])
                    while dist > self.L:
                        self.D_loc[d2] = (100*rnd.random(), 100*rnd.random())
                        dist = self.compute_distance(
                            self.D_loc[d1], self.D_loc[d2])

        # Then
        # Check if each task node is in feasible region. If not, sample another
        # point and check if that point is in feasible region. Ensure all
        # points are in feasible region
        for task in self.T:
            feasible = self.check_task_in_feasible_region(task)
            while not feasible:
                self.T_loc[task] = (100*rnd.random(), 100*rnd.random())
                feasible = self.check_task_in_feasible_region(task)

        # Once feasible task and depot locations have been generated, compute
        # the remaining parameters of the instance.
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

    def check_task_in_feasible_region(self, task):
        # Check if the point can be reached from any of the depots, and then
        # a depot can be reached from the task location, such that the total
        # distance travelled is less than self.L
        in_feasible_region = 0
        for d1 in self.D:
            for d2 in self.D:
                dist1 = self.compute_distance(
                    self.D_loc[d1], self.T_loc[task])
                dist2 = self.compute_distance(
                    self.T_loc[task], self.D_loc[d2])

                if (dist1 + dist2) < self.L:
                    in_feasible_region = 1
                    return in_feasible_region
        return in_feasible_region

    def compute_distance(self, p1, p2):
        return np.linalg.norm(np.array(p1)-np.array(p2))

    def generate_data(self):
        for iteration in range(self.no_of_instances):
            self.create_feasible_uniform_instance(iteration)
            self.create_json_data()
            self.write_instance_to_json()


def main():
    min_robots = 3
    max_robots = 3

    min_depots = 3
    max_depots = 3

    min_tasks = 7
    max_tasks = 7

    fuel_range_start = 50
    fuel_range_step = 100
    # fuel_range_end = int(math.ceil(2*100*math.sqrt(2) /
    #                               fuel_range_step)*fuel_range_step)  # ~282
    fuel_range_end = 50

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
                        instance = Feasible_Uniform_Instance_Generator(
                            r, d, t, f, tmax, no_of_instances)
                        instance.generate_data()


if __name__ == "__main__":
    main()
