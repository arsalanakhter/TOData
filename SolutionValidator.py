# Like a unit test for formulations
import plotly.offline as py
import plotly.graph_objs as go
from TO_InstanceGenerator import Instance_Generator
from TO_InstanceReader import InstanceReader
from TO_SysPathGenerator import SysPathGenerator
from F1TOBasicTaskFlowBasedSubtourNodeBasedFuel import F1Solver
from F2TOBasicTaskFlowBasedSubtourArcBasedFuel import F2Solver
from F3TOBasicTimeFlowBasedSubtourNodeBasedFuel import F3Solver
from F4TOBasicTimeFlowBasedSubtourArcBasedFuel import F4Solver
from F5TOMaxMinTaskFlowBasedSubtourNodeBasedFuel import F5Solver
from F6TOMaxMinTaskFlowBasedSubtourArcBasedFuel import F6Solver
from F7TOMaxMinTimeFlowBasedSubtourNodeBasedFuel import F7Solver
from F8TOMaxMinTimeFlowBasedSubtourArcBasedFuel import F8Solver
from TO_SolutionReader import Solution_Reader
import os
import numpy as np
import random as rnd
import sys


class SolutionValidator:
    def __init__(self, seed, no_of_robots, no_of_depots, no_of_tasks, delta, Tmax, path_to_data_folder=os.getcwd()):
        # Get the params
        self.seed = seed
        self.noOfRobots = no_of_robots
        self.noOfTasks = no_of_tasks
        self.noOfDepots = no_of_depots
        self.L = 1
        self.T_max = Tmax
        self.vel = 1
        self.arenaRadius = 100
        self.delta = delta
        self.no_of_instances = 1
        self.objectiveFunctionValueF1_4 = []
        self.objectiveFunctionValueF5_8 = []

    def solver_select(self, solver_string):
        solver_types = {
            'F1': F1Solver,
            'F2': F2Solver,            
            'F3': F3Solver,            
            'F4': F4Solver,            
            'F5': F5Solver,            
            'F6': F6Solver,            
            'F7': F7Solver,            
            'F8': F8Solver            
        }
        solver = solver_types.get(solver_string)
        return solver
    
    def solveAll(self):
        # Generating instance
        self.generate_instance = Instance_Generator(self.noOfRobots, self.noOfDepots, self.noOfTasks, self.delta, self.T_max,
                 self.no_of_instances, self.seed, path_to_data_folder=os.getcwd())
        self.generate_instance.generate_data()

        filePaths = SysPathGenerator(self.noOfRobots, self.noOfDepots, self.noOfTasks, self.delta, self.T_max)
        instance_folder_path = filePaths.instance_data_folder_path
        instance_filename_prefix = filePaths.instance_data_filename_prefix
        curr_instance_filename = instance_filename_prefix + 'Iter' + str(0) + '.json'
        instance = InstanceReader(curr_instance_filename)
        instance_data = instance.readData()
        
        for variant in range(1,5):
            # Basic Formulations
            solver_selected = self.solver_select("F"+str(variant))
            solver = solver_selected(instance_data)
            model = solver.solve()
            self.objectiveFunctionValueF1_4.append(model.objVal)
            solver.write_lp_and_sol_to_disk()
            
            # Max Min Obj Function Formulations
            solver_selected = self.solver_select("F"+str(variant+4))
            solver = solver_selected(instance_data)
            model = solver.solve()
            self.objectiveFunctionValueF5_8.append(model.objVal)
            solver.write_lp_and_sol_to_disk()
            
        
        #TODO any other metrics to compare?
        # Check for sanity : Comparing objective function value
        print("\nFor formualtions 1 to 4:")
        if all(x == self.objectiveFunctionValueF1_4[0] for x in self.objectiveFunctionValueF1_4):
            print("Objective function value matches = ", self.objectiveFunctionValueF1_4[0])
        else:
            print("Objective function value is different for formulation ")
            print(self.objectiveFunctionValueF1_4)

        print("\nFor formualtions 5 to 8:")
        if all(x == self.objectiveFunctionValueF5_8[0] for x in self.objectiveFunctionValueF5_8):
            print("Objective function value matches = ", self.objectiveFunctionValueF5_8[0])
        else:
            print("Objective function value is different for formulation ")
            print(self.objectiveFunctionValueF5_8)



def main():
    seed = [rnd.randrange(sys.maxsize)]
    no_of_robots = 5
    no_of_depots = 3
    no_of_tasks = 8
    delta = 50
    Tmax = 150
    validate = SolutionValidator(seed, no_of_robots, no_of_depots, no_of_tasks, delta, Tmax)
    validate.solveAll()


if __name__ == "__main__":
    main()