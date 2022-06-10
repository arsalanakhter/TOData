# from TO_InstanceGenerator import Instance_Generator
from TO_InstanceReader import InstanceReader

from TO_SolverMinMax import SolverMinMax
from TO_Solver import Solver
from F1TOBasicTaskFlowBasedSubtourNodeBasedFuel import F1Solver
from F2TOBasicTaskFlowBasedSubtourArcBasedFuel import F2Solver
from F3TOBasicTimeFlowBasedSubtourNodeBasedFuel import F3Solver
from F4TOBasicTimeFlowBasedSubtourArcBasedFuel import F4Solver
from F5TOMaxMinTaskFlowBasedSubtourNodeBasedFuel import F5Solver
from F6TOMaxMinTaskFlowBasedSubtourArcBasedFuel import F6Solver
from F7TOMaxMinTimeFlowBasedSubtourNodeBasedFuel import F7Solver
from F8TOMaxMinTimeFlowBasedSubtourArcBasedFuel import F8Solver

from TO_SolutionReader import Solution_Reader
from TO_SolutionInformationExtractor import SolutionInformationExtractor
import os
import sys
# import ptvsd


class Job:
    def __init__(self, instance_string, solver_string, path_to_working_dir=os.getcwd()):
        self.instance = InstanceReader(instance_string)
        self.instance_data = self.instance.readData()
        # Now solve the instance, and write the solution to disk
        solver_selected = self.solver_select(solver_string)
        solver = solver_selected(self.instance_data)
        model = solver.solve()
        solver.write_lp_and_sol_to_disk()

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



def main():
    # Attach a debugger from here (vscode) for a call from bash
    # print("Waiting for debugger attach")
    # ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
    # ptvsd.wait_for_attach()
    # breakpoint()
    # Get the string name from sys.argv[1]
    instance_string = sys.argv[1]
    solver_string = sys.argv[2]
    print("instance and solver string from within python : {} {}".format(instance_string, solver_string))
    # Call the job, since we assume that data has already been generated, and
    # this job is to just solve the instance
    curr_job = Job(instance_string, solver_string)


if __name__ == "__main__":
    main()
