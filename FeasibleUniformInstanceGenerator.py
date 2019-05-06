from TO_InstanceGenerator import Instance_Generator
import os


class Feasible_Uniform_Instance_Generator(Instance_Generator):

    def __init__(self, no_of_robots, no_of_depots, no_of_tasks, fuel, Tmax,
                 no_of_instances=1, path_to_data_folder=os.getcwd()):

        Instance_Generator.__init__(self, no_of_robots, no_of_depots,
                                    no_of_tasks, fuel, Tmax, no_of_instances=1,
                                    path_to_data_folder=os.getcwd())

    def create_feasible_uniform_instance(self, iteration):
        self.create_instance(iteration)
        # Check if each task node is in feasible region. If not, sample another
        # point and check if that point is in feasible region. Ensure all
        # points are in feasible region
