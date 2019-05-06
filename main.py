# from TO_InstanceGenerator import Instance_Generator
from TO_InstanceReader import InstanceReader
from TO_SolverMinMax import SolverMinMax
from TO_Solver import Solver
from TO_SolutionReader import Solution_Reader
from TO_SolutionInformationExtractor import SolutionInformationExtractor
import os
import sys
import ptvsd


class Job:
    def __init__(self, instance_string, path_to_working_dir=os.getcwd()):
        instance = InstanceReader(instance_string)
        instance_data = instance.readData()
        # Now solve the instance, and write the solution to disk
        # solver = SolverMinMax(instance_data)
        solver = Solver(instance_data)
        solver.solve()
        solver.write_lp_and_sol_to_disk()


def main():
    # Attach a debugger from here (vscode) for a call from bash
    # print("Waiting for debugger attach")
    # ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
    # ptvsd.wait_for_attach()
    # breakpoint()
    # Get the string name from sys.argv[1]
    instance_string = sys.argv[1]
    print("instance string from within python : {}".format(instance_string))
    # Call the job, since we assume that data has already been generated, and
    # this job is to just solve the instance
    curr_job = Job(instance_string)


if __name__ == "__main__":
    main()
