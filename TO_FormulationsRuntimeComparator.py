import os
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as py
import plotly.io as pio
import csv
from TO_SolutionReader import Solution_Reader


class FormulationsRuntimeComparator:
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

    def compare_all_problems(self):
        os.remove('Runtimes.csv')
        with open('Runtimes.csv', 'a') as the_file:
            the_file.write('instance,F1,F2,F3,F4\n')
            # the_file.write('instance,F5,F6,F7,F8\n')
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
        runtimes_list = []
        row = [problem_string]
        for f in self.formulations_list:
            instance_string = 'F'+str(f)+problem_string
            sol = Solution_Reader(instance_string)
            runtimes_list.append(sol.runtime)
        with open('Runtimes.csv', 'a') as the_file:
            the_file.write('{},{},{},{},{}\n'.format(problem_string, runtimes_list[0], 
                                                runtimes_list[1], runtimes_list[2], runtimes_list[3]))

    def compute_best_formulation_stats(self):
        # Compute which formulation works better for the following scenarios
        # 1. Increasing number of robots
        # 2. Increasing number of tasks
        # 3. Increasing number of depots
        # 4. Increasing delta
        # 5. Increasing Tmax
        df_with_instances = pd.read_csv('Runtimes.csv', index_col=False)
        df = df_with_instances[['F1','F2','F3','F4']]
        # df = df_with_instances[['F5','F6','F7','F8']]
        print(df)
        df_min_vals = df.min(axis=1)
        df_min_F1 = (df_min_vals == df.F1).astype(int)
        df_min_F2 = (df_min_vals == df.F2).astype(int)
        df_min_F3 = (df_min_vals == df.F3).astype(int)
        df_min_F4 = (df_min_vals == df.F4).astype(int)

        # df_min_F5 = (df_min_vals == df.F5).astype(int)
        # df_min_F6 = (df_min_vals == df.F6).astype(int)
        # df_min_F7 = (df_min_vals == df.F7).astype(int)
        # df_min_F8 = (df_min_vals == df.F8).astype(int)
        df_all_mins = pd.concat([df_with_instances.instance, df_min_F1, df_min_F2, df_min_F3, df_min_F4], axis=1)
        # df_all_mins = pd.concat([df_with_instances.instance, df_min_F5, df_min_F6, df_min_F7, df_min_F8], axis=1)
        df_all_mins.columns = ['instance','F1','F2','F3','F4']
        # df_all_mins.columns = ['instance','F5','F6','F7','F8']

        # Create a dictionary to hold min times
        self.min_times = {}
        #for f in self.formulations_list:
        #    self.min_times['F'+str(f)] = {}
        for r in self.no_of_robots_list:
            self.min_times['R = '+str(r)] = []
        for d in self.no_of_depots_list:
            self.min_times['D = '+str(d)] = []
        for t in self.no_of_tasks_list:
            self.min_times['T = '+str(t)] = []
        for delta in self.delta_param_list:
            self.min_times['𝜏 = '+str(delta)] = []
        for tmax in self.Tmax_param_list:
            self.min_times['𝓣<sub>max</sub> = '+str(tmax)] = []

        # Now, compute how many times each formulation worked best for R
        self.R_formulations_data = {} 
        for i in self.no_of_robots_list:
            df_R =  df_all_mins[df_all_mins.instance.str.contains('R'+str(i))]
            # Pick the row entries where each formulation has the minimum value
            for j in self.formulations_list:
                curr_col_with_times = df[df_with_instances.instance.str.contains('R'+str(i))]['F'+str(j)]
                self.min_times['R = '+str(i)].append(round(df['F'+str(j)].iloc[curr_col_with_times[df_R['F'+str(j)] == 1].idxmax()]))
            df_R_sum = df_R.sum().tolist()
            self.R_formulations_data['R = '+str(i)] = df_R_sum[1:]

        # Now, compute how many times each formulation worked best for D
        self.D_formulations_data = {} 
        for i in self.no_of_depots_list:
            df_D =  df_all_mins[df_all_mins.instance.str.contains('D'+str(i))]
            # Pick the row entries where each formulation has the minimum value
            for j in self.formulations_list:
                curr_col_with_times = df[df_with_instances.instance.str.contains('D'+str(i))]['F'+str(j)]
                self.min_times['D = '+str(i)].append(round(df['F'+str(j)].iloc[curr_col_with_times[df_D['F'+str(j)] == 1].idxmax()]))
            df_D_sum = df_D.sum().tolist()
            self.D_formulations_data['D = '+str(i)] = df_D_sum[1:]

        # Now, compute how many times each formulation worked best for T
        self.T_formulations_data = {} 
        for i in self.no_of_tasks_list:
            df_T =  df_all_mins[df_all_mins.instance.str.contains('T'+str(i))]
            # Pick the row entries where each formulation has the minimum value
            for j in self.formulations_list:
                curr_col_with_times = df[df_with_instances.instance.str.contains('T'+str(i))]['F'+str(j)]
                self.min_times['T = '+str(i)].append(round(df['F'+str(j)].iloc[curr_col_with_times[df_T['F'+str(j)] == 1].idxmax()]))
            df_T_sum = df_T.sum().tolist()
            self.T_formulations_data['T = '+str(i)] = df_T_sum[1:]

        # Now, compute how many times each formulation worked best for Delta
        self.Delta_formulations_data = {} 
        for i in self.delta_param_list:
            df_Delta =  df_all_mins[df_all_mins.instance.str.contains('Delta'+str(i))]
            # Pick the row entries where each formulation has the minimum value
            for j in self.formulations_list:
                curr_col_with_times = df[df_with_instances.instance.str.contains('Delta'+str(i))]['F'+str(j)]
                self.min_times['𝜏 = '+str(i)].append(round(df['F'+str(j)].iloc[curr_col_with_times[df_Delta['F'+str(j)] == 1].idxmax()]))
            df_Delta_sum = df_Delta.sum().tolist()
            self.Delta_formulations_data['𝜏 = '+str(i)] = df_Delta_sum[1:]


        # Now, compute how many times each formulation worked best for Tmax
        self.Tmax_formulations_data = {} 
        for i in self.Tmax_param_list:
            df_Tmax =  df_all_mins[df_all_mins.instance.str.contains('Tmax'+str(i))]
            # Pick the row entries where each formulation has the minimum value
            for j in self.formulations_list:
                curr_col_with_times = df[df_with_instances.instance.str.contains('Tmax'+str(i))]['F'+str(j)]
                self.min_times['𝓣<sub>max</sub> = '+str(i)].append(round(df['F'+str(j)].iloc[curr_col_with_times[df_Tmax['F'+str(j)] == 1].idxmax()]))

            df_Tmax_sum = df_Tmax.sum().tolist()
            self.Tmax_formulations_data["𝓣<sub>max</sub> = "+str(i)] = df_Tmax_sum[1:]


    def plot_best_formulation_stats(self):
        data_to_be_plotted = [self.R_formulations_data, self.D_formulations_data, self.T_formulations_data,
                                self.Delta_formulations_data, self.Tmax_formulations_data]
        count = 0
        # count = 5
        for data_obj in data_to_be_plotted:
            fig = go.Figure(data=[
                go.Bar(name=k, 
                        x=[r'$\mathcal{F}1$', r'$\mathcal{F}2$', r'$\mathcal{F}3$', r'$\mathcal{F}4$'],
                        # x=[r'$\mathcal{F}5$', r'$\mathcal{F}6$', r'$\mathcal{F}7$', r'$\mathcal{F}8$'],
                        y=v
                        #textfont=dict(size=20),
                        #text=self.min_times[k],
                        #textposition='outside',
                        #textangle=270,
                        #texttemplate='%{text:.0f} (s)'
                )
                for k,v in data_obj.items()]
                )
            fig.update_layout(font=dict(size=18),xaxis_title="Formulations", yaxis_title="Number of instances with best runtime")
            fig.update_yaxes(range=[0, 800])
            py.plot(fig, include_mathjax='cdn')
            fig = pio.full_figure_for_development(fig, warn=False)
            pio.write_image(fig, 'figs/fig'+str(count)+'.pdf', format='pdf')
            count += 1



def main():
    formulations_list = [1,2,3,4]
    # formulations_list = [5,6,7,8]
    no_of_robots_list = [2,3,4]
    no_of_depots_list =[1,2,3]
    no_of_tasks_list = [5, 10]
    delta_param_list = [50, 75, 100, 125, 150]
    Tmax_param_list = [50,75,150,300,600]
    iterations_list = [i for i in range(10)]

    comparator = FormulationsRuntimeComparator(
                        formulations_list,
                        no_of_robots_list,
                        no_of_depots_list,
                        no_of_tasks_list,
                        delta_param_list,
                        Tmax_param_list,
                        iterations_list)
    comparator.compare_all_problems()
    comparator.compute_best_formulation_stats()
    comparator.plot_best_formulation_stats()

if __name__ == "__main__":
    main()
