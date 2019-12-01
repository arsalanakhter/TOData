import os
import csv
from TO_SolutionReader import Solution_Reader


class FormulationsSolutionComparator:
    # A class to compare the solutions coming from different formulations
    # Ideally, all the solutions should be same. If not, at least the 
    # objective function value should be same
    # The class writes a file only containing any differences in the solutions.

    def __init__(self, formulations_list,
                        no_of_robots_list,
                        no_of_depots_list,
                        no_of_tasks_list,
                        delta_param_list,
                        Tmax_param_list,
                        iterations_list,
                        path_to_data_folder=os.getcwd()):

        self.formulations_list = formulations_list
        self.no_of_robots_list = no_of_robots_list
        self.no_of_depots_list = no_of_depots_list
        self.no_of_tasks_list = no_of_tasks_list
        self.delta_param_list = delta_param_list
        self.Tmax_param_list = Tmax_param_list
        self.iterations_list = iterations_list
        
        with open('comparison.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["Instance", "F1", "F2", "F3", "F4"])
        csvFile.close()    

        for r in self.no_of_robots_list:
            for d in self.no_of_depots_list:
                for t in self.no_of_tasks_list:
                    for delta in self.delta_param_list:
                        for tmax in self.Tmax_param_list:
                            for i in self.iterations_list:
                                problem_string = 'R{}D{}T{}Delta{}Tmax{}Iter{}'.format(r, d, t, delta, tmax, i)
                                self.compare_single_problem(problem_string)

    def compare_single_problem(self, problem_string):
        # Compares all the formulations for a single problem
        # and writes the results in a file 
        # The results should show only the problem instances that have
        # different objective values and, if so, what are those, and
        # what are the resulting arcs.       
        obj_val_list = []
        row = [problem_string]
        for f in self.formulations_list:
            instance_string = 'F'+str(f)+problem_string
            sol = Solution_Reader(instance_string)
            obj_val_list.append(sol.objective_val)
            print('{}: {}'.format('F'+str(f)+problem_string, obj_val_list[f-1:]==obj_val_list[:-1]))
            if obj_val_list[f-1:]==obj_val_list[:-1]:
                row.append("True")
            else:
                row.append(obj_val_list[f-1])
        with open('comparison.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()



def main():
    formulations_list = [1,2,3,4]
    no_of_robots_list = [3]
    no_of_depots_list =[2,3]
    no_of_tasks_list = [5,10]
    delta_param_list = [50, 75, 150]
    Tmax_param_list = [150,300,600]
    iterations_list = [i for i in range(10)]

    comparator = FormulationsSolutionComparator(
                        formulations_list,
                        no_of_robots_list,
                        no_of_depots_list,
                        no_of_tasks_list,
                        delta_param_list,
                        Tmax_param_list,
                        iterations_list)

if __name__ == "__main__":
    main()
