import os
import csv

from TO_SolutionReader import Solution_Reader


class SolutionRuntimeDataAggregator:

    def __init__(self, formulations_list,
                        no_of_robots_list,
                        no_of_depots_list,
                        no_of_tasks_list,
                        fuel_param_list,
                        Tmax_param_list,
                        iterations_list,
                        path_to_data_folder=os.getcwd()):

        self.formulations_list = formulations_list
        self.no_of_robots_list = no_of_robots_list
        self.no_of_depots_list = no_of_depots_list
        self.no_of_tasks_list = no_of_tasks_list
        self.fuel_param_list = fuel_param_list
        self.Tmax_param_list = Tmax_param_list
        self.iterations_list = iterations_list
                       
        self.solution_runtimes = {}
        for f in self.formulations_list:
            self.solution_runtimes['F'+str(f)] = {}
            for r in self.no_of_robots_list:
                self.solution_runtimes['F'+str(f)]['R'+str(r)] = {}
                for d in self.no_of_depots_list:
                    self.solution_runtimes['F'+str(f)]['R'+str(r)]['D'+str(d)] = {}
                    for t in self.no_of_tasks_list:
                        self.solution_runtimes['F'+str(f)]['R'+str(r)]['D'+str(d)]['T'+str(t)] = {}
                        for fuel in self.fuel_param_list:
                            self.solution_runtimes['F'+str(f)]['R'+str(r)]['D'+str(d)]['T'+str(t)]['F'+str(fuel)] = {}
                            for tmax in self.Tmax_param_list:
                                self.solution_runtimes['F'+str(f)]['R'+str(r)]['D'+str(d)]['T'+str(t)]['F'+str(fuel)]['Tmax'+str(tmax)] = {}
                                for i in self.iterations_list:
                                    this_instance_string = 'F' + str(f) + \
                                        'R' + str(r) + 'D' + str(d) + \
                                        'T' + str(t) + 'F' + str(fuel) + \
                                        'Tmax' + str(tmax) + 'Iter' + str(i)
                                    this_sol = Solution_Reader(this_instance_string)
                                    self.solution_runtimes['F'+str(f)]['R'+str(r)]['D'+str(d)]['T'+str(t)]['F'+str(fuel)]['Tmax'+str(tmax)]['Iter'+str(i)] = this_sol.runtime


    def write_to_csv(self):
        self.resultsFile = os.path.normpath(os.getcwd()+'/aggregatedData.csv')
        with open(self.resultsFile, 'w+') as results_file:
            result_writer = csv.writer(results_file, delimiter=',')
            # Write row1
            row1 = [' ',' ']
            row2 = [' ',' ']
            row3 = [' ',' ']
            for formulation in self.formulations_list:
                row1 = row1 + ['F'+str(formulation) for i in range (len(self.no_of_depots_list)*len(self.no_of_tasks_list))]
                # Write row2
                for d in self.no_of_depots_list:
                    row2 = row2 + ['D'+str(d) for i in range (len(self.no_of_tasks_list))]
                    # Write row3
                    for t in self.no_of_tasks_list:
                        row3 = row3 + ['T'+str(t)]
            result_writer.writerow(row1)
            result_writer.writerow(row2)
            result_writer.writerow(row3)


def main():
    formulations_list = [1,2,3,4]
    no_of_robots_list = [2]
    no_of_depots_list =[2,3]
    no_of_tasks_list = [5,10]
    fuel_param_list = [50, 75, 150]
    Tmax_param_list = [150,300,600]
    iterations_list = [i for i in range(10)]

    agg = SolutionRuntimeDataAggregator(
                        formulations_list,
                        no_of_robots_list,
                        no_of_depots_list,
                        no_of_tasks_list,
                        fuel_param_list,
                        Tmax_param_list,
                        iterations_list)

    agg.write_to_csv()

if __name__ == "__main__":
    main()
