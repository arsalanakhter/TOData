from gurobipy import *
import random as rnd
import math
import numpy as np
import os
from TO_InstanceReader import InstanceReader
from TO_SysPathGenerator import SysPathGenerator


class F2Solver:

    def __init__(self, instance):
        '''
        param instance: A single instance that can be solved by the Basic Solver
        '''
        self.iteration = instance.iteration
        self.noOfRobots = instance.noOfRobots
        self.noOfTasks = instance.noOfTasks
        self.noOfDepots = instance.noOfDepots
        self.L = instance.L
        self.delta = instance.delta
        self.T_max = instance.T_max
        self.vel = instance.vel
        self.thisSeed = instance.thisSeed
        self.K = instance.K
        self.T = instance.T
        self.D = instance.D
        self.S = instance.S
        self.E = instance.E
        self.N = instance.N
        self.L = instance.L
        self.vel = instance.vel
        self.T_max = instance.T_max
        #R = json_data['R']
        self.T_loc = instance.T_loc
        self.D_loc = instance.D_loc
        self.S_loc = instance.S_loc
        self.E_loc = instance.E_loc
        self.N_loc = instance.N_loc
        self.edges = instance.edges
        self.c = instance.c
        self.f = instance.f
        self.arcs = instance.arcs
        self.arc_ub = instance.arc_ub
        self.k_y = instance.k_y # not used remove TODO
        # Generate names for model/solution_file
        self.filePaths = SysPathGenerator(self.noOfRobots, self.noOfDepots, self.noOfTasks, 
                                            self.delta, self.T_max)
        self.instance_folder_path = self.filePaths.instance_sol_folder_path
        self.instance_filename_prefix = '/F2' + self.filePaths.instance_sol_filename_prefix

        self.curr_instance_filename = self.instance_filename_prefix + \
            'Iter' + str(self.iteration)
        self.file_path = os.path.normpath(
            self.instance_folder_path + self.curr_instance_filename)

        # Initialize the model
        self.init_model()

    def init_model(self):
        # Initialize the model
        self.model = Model(
            'F2TOBasic-'+self.curr_instance_filename[1:]+'-Seed:' + str(self.thisSeed))
        # Decision variables and their bounds
        x = self.model.addVars(self.arcs, lb = 0, ub = self.arc_ub, name="x", vtype=GRB.INTEGER)
        y = self.model.addVars(self.T, name="y", vtype=GRB.BINARY)
        g = self.model.addVars(self.arcs, name="g", vtype=GRB.INTEGER)
        p = self.model.addVars(self.arcs, name="p", vtype=GRB.CONTINUOUS)

        # Objective function
        gamma = 0.0001
        objExpr1 = quicksum(y[i] for i in self.T)
        objExpr2 = quicksum(gamma * self.c[i, j] * x[i, j, k]
                            for k in self.K for i in self.N for j in self.N if i != j)
        objFun = objExpr1 - objExpr2
        self.model.setObjective(objFun, GRB.MAXIMIZE)

        # Constraints
        # For detail on what the constraints signify please see the
        # corresponding section in the report
        #c2_1 = self.model.addConstr((quicksum(x[s,j,k] for j in self.N for k in self.K for s in self.S if j not in self.S) == self.noOfRobots), name="c2_1")
        #c2_2 = self.model.addConstr((quicksum(x[i,e,k] for i in self.N for k in self.K for e in self.E if i!=e) == self.noOfRobots), name="c2_2")
        
        c3_1 = self.model.addConstrs(((quicksum(x[s,j,k] for s in self.S for j in self.N if j not in self.S)) == 1 for k in self.K), name="c3_1")
        c4_1 = self.model.addConstrs(((quicksum(x[j,s,k] for s in self.S for j in self.N if j not in self.S)) == 0 for k in self.K), name="c3_2")
        c3_2 = self.model.addConstrs(((quicksum(x[i,e,k] for e in self.E for i in self.N if i not in self.E)) == 1 for k in self.K), name="c4_1")
        c4_2 = self.model.addConstrs(((quicksum(x[e,i,k] for e in self.E for i in self.N if i not in self.E)) == 0 for k in self.K), name="c4_2")

        c5_1 = self.model.addConstrs(((quicksum(x[i,h,k] for i in self.N if i!=h and i not in self.E)) == (quicksum(x[h,j,k] for j in self.N if j!=h and j not in self.S)) 
                                            for h in self.N for k in self.K if h not in self.S and h not in self.E), name="c5_1")
        c5_2 = self.model.addConstrs(((quicksum(x[i,h,k] for k in self.K for i in self.N if i!=h)) == y[h] for h in self.T), name="c5_2")
        c5_3 = self.model.addConstrs(((quicksum(x[h,j,k] for k in self.K for j in self.N if j!=h)) == y[h] for h in self.T), name="c5_3")
        c5_4 = self.model.addConstrs((y[i] <= 1 for i in self.T), name="c5_4")

        c6 = self.model.addConstrs((quicksum(self.c[i,j]*x[i,j,k]*1/self.vel for i in self.N for j in self.N if i!=j) <= self.T_max 
                                                        for k in self.K), name="c6")
        
        # Task based flow constraints
        c7 = self.model.addConstrs(((quicksum((g[s,i,k] - g[i,s,k]) for i in self.N for s in self.S if i not in self.S)) == 
                        (quicksum(x[i,j,k] for i in self.T for j in self.N if i!=j)) for k in self.K), name="c7")
        c8 = self.model.addConstrs(((quicksum((g[j,i,k] - g[i,j,k]) for j in self.N if i!=j)) == 
                        (quicksum(x[i,j,k] for j in self.N if i!=j )) for i in self.T for k in self.K), name="c8")
        c9 = self.model.addConstrs(((quicksum((g[j,i,k] - g[i,j,k]) for j in self.N if j!=i)) 
                                                    == 0 for i in self.D for k in self.K), name="c9")
        #c10 = self.model.addConstrs(( 0 <= g[i,j,k] <= self.noOfTasks*x[i,j,k] for i in self.N for j in self.N for k in self.K if i!=j), name="c10")
        c10_1 = self.model.addConstrs(( 0 <= g[i,j,k] for i in self.N for j in self.N for k in self.K if i!=j), name="c10_1")
        c10_2 = self.model.addConstrs(( g[i,j,k] <= self.noOfTasks*x[i,j,k] for i in self.N for j in self.N for k in self.K if i!=j), name="c10_2")        


        
        # Arc based fuel constraints
        c11 = self.model.addConstrs((quicksum(p[t,i,k] for k in self.K for i in self.N if t!=i) - 
                        quicksum(p[i,t,k] for k in self.K for i in self.N if t!=i) == 
                               quicksum(self.f[t,i]*x[t,i,k] for k in self.K for i in self.N if t!=i)
                                                               for t in self.T), name='c11')
        c12 = self.model.addConstrs((p[b,i,k] == self.f[b,i]*x[b,i,k] for b in self.S+self.D for i in self.N for k in self.K if i!=b), name='c12')
        #c13 = self.model.addConstrs((0 <= p[i,j,k] <= self.L*x[i,j,k] for i in self.N for j in self.N for k in self.K if i != j), name='c13')
        c13_1 = self.model.addConstrs((0 <= p[i,j,k] for i in self.N for j in self.N for k in self.K if i != j), name='c13_1')
        c13_2 = self.model.addConstrs((p[i,j,k] <= self.L*x[i,j,k] for i in self.N for j in self.N for k in self.K if i != j), name='c13_2')

    def solve(self):
        # self.model.params.Heuristics = 0.0  # %age of time use a heuristic solution
        # self.model.params.Cuts = 0  # Do not use cuts, except lazy constraints
        # model.params.MIPGapAbs = 0.0005
        # self.model.params.TimeLimit = 30
        self.model.optimize()

        return self.model  

    def write_lp_and_sol_to_disk(self):
        if not os.path.exists(self.instance_folder_path):
            os.makedirs(self.instance_folder_path)
        # Save runtime, because after writing the lp file, 
        # runtime is lost. No idea why
        run_time = self.model.Runtime
        # Write both the LP file and the solution file
        self.model.write(self.file_path+'.lp')
        self.model.write(self.file_path+'.sol')
        # Add runtime in the sol file as well.
        with open(self.file_path+'.sol', "a") as myfile:
            myfile.write('runtime:{0:.2f}'.format(run_time))


def main():
    min_robots = 2
    max_robots = 2

    min_depots = 1
    max_depots = 1

    min_tasks = 10
    max_tasks = 10

    delta_range_start = 300
    delta_range_step = 100
    # delta_range_end = int(math.ceil(2*100*math.sqrt(2) /
    #                               delta_range_step)*delta_range_step)  # ~282
    delta_range_end = 300

    Tmax_range_start = 600
    Tmax_range_step = 100
    # Tmax_range_end = int(math.ceil(2*100*math.sqrt(2) /
    #                               Tmax_range_step)*Tmax_range_step)  # ~282
    Tmax_range_end = 600

    robots_range = list(range(min_robots, max_robots+1))
    depots_range = list(range(min_depots, max_depots+1))
    tasks_range = list(range(min_tasks, max_tasks+1))
    delta_range = list(range(delta_range_start, delta_range_end +
                            delta_range_step, delta_range_step))
    Tmax_range = list(range(Tmax_range_start, Tmax_range_end +
                            Tmax_range_step, Tmax_range_step,))

    no_of_instances = 1
    path_to_data_folder = os.getcwd()
    # instance_dictionary = {}

    for r in robots_range:
        for d in depots_range:
            for t in tasks_range:
                for f in delta_range:
                    for tmax in Tmax_range:
                        filePaths = SysPathGenerator(r, d, t, f, tmax)
                        instance_folder_path = filePaths.instance_data_folder_path
                        instance_filename_prefix = filePaths.instance_data_filename_prefix

                        for it in range(no_of_instances):
                            curr_instance_filename = instance_filename_prefix + \
                                'Iter' + str(it) + '.json'
                            file_path = os.path.normpath(
                                instance_folder_path+curr_instance_filename)
                            instance = InstanceReader(curr_instance_filename)
                            instance_data = instance.readData()
                            solver = F2Solver(instance_data)
                            model = solver.solve()
                            solver.write_lp_and_sol_to_disk()

if __name__ == "__main__":
    main()
