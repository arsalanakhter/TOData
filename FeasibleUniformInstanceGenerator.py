from TO_InstanceGenerator import Instance_Generator
import os
import random as rnd


class Feasible_Uniform_Instance_Generator(Instance_Generator):

    def __init__(self, no_of_robots, no_of_depots, no_of_tasks, fuel, Tmax,
                 no_of_instances=1, path_to_data_folder=os.getcwd()):

        Instance_Generator.__init__(self, no_of_robots, no_of_depots,
                                    no_of_tasks, fuel, Tmax, no_of_instances=1,
                                    path_to_data_folder=os.getcwd())

    def create_feasible_uniform_instance(self, iteration):
        self.create_instance(iteration)
        # First check each depot node can be reached from another depot.
        for d1 in self.D:
            for d2 in self.D:
                while self.c[d1, d2] > self.L:
                    self.D_loc[d2] = tuple(100*rnd.random(), 100*rnd.random())
        # Then
        # Check if each task node is in feasible region. If not, sample another
        # point and check if that point is in feasible region. Ensure all
        # points are in feasible region
        for task in self.T:
            feasible = self.check_task_in_feasible_region(task)
            while not feasible:
                self.T_loc[task] = tuple(100*rnd.random(), 100*rnd.random())

    def check_task_in_feasible_region(self, task):
        # Check if the point can be reached from any of the depots, and then
        # a depot can be reached from the task location, such that the total
        # distance travelled is less than self.L
        in_feasible_region = 0
        for d1 in self.D:
            for d2 in self.D:
                if (self.c[d1, task] + self.c[task, d2]) < self.L:
                    in_feasible_region = 1
                    return in_feasible_region
        return in_feasible_region


