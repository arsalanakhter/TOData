# The class takes in a string for an instance, and generates folder paths and
# instance and solution filenames
import regex as re
import os


class PathGenerator:

    def __init__(self, instance_string, path_to_working_dir=os.getcwd()):
        self.instance_string = instance_string
        self.path_to_working_dir = path_to_working_dir
        temp = [int(s) for s in re.findall(
            '\d+', instance_string)]  # extract numbers
        self.noOfRobots = temp[0]
        self.noOfDepots = temp[1]
        self.noOfTasks = temp[2]
        self.L = temp[3]
        self.T_max = temp[4]
        self.iteration = temp[5]
        self.compute_data_filepath()
        self.compute_sol_filepath()

    def compute_data_filepath(self):
        instance_data_folder_path_suffix = \
            '/data' + \
            '/R' + str(self.noOfRobots) + \
            '/D' + str(self.noOfDepots) + \
            '/T' + str(self.noOfTasks) + \
            '/F' + str(self.L) + \
            '/Tmax' + str(self.T_max)
        self.instance_data_folder_path = \
            os.path.normpath(self.path_to_working_dir +
                             instance_data_folder_path_suffix)
        instance_data_filename_prefix = \
            '\\R' + str(self.noOfRobots) + \
            'D' + str(self.noOfDepots) + \
            'T' + str(self.noOfTasks) + \
            'F' + str(self.L) + \
            'Tmax' + str(self.T_max) + \
            'Iter' + str(self.iteration)
        self.instance_data_file = os.path.normpath(
            self.instance_data_folder_path + instance_data_filename_prefix + '.json')

    def compute_sol_filepath(self):
        instance_sol_folder_path_suffix = \
            '/sol' + \
            '/R' + str(self.noOfRobots) + \
            '/D' + str(self.noOfDepots) + \
            '/T' + str(self.noOfTasks) + \
            '/F' + str(self.L) + \
            '/Tmax' + str(self.T_max)
        self.instance_sol_folder_path = os.path.normpath(
            self.path_to_working_dir + instance_sol_folder_path_suffix)
        instance_sol_filename_prefix = \
            '\\R' + str(self.noOfRobots) + \
            'D' + str(self.noOfDepots) + \
            'T' + str(self.noOfTasks) + \
            'F' + str(self.L) + \
            'Tmax' + str(self.T_max) + \
            'Iter' + str(self.iteration)
        self.instance_sol_file = os.path.normpath(
            self.instance_sol_folder_path + instance_sol_filename_prefix + '.sol')
