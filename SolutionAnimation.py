# Video

import plotly.offline as py
import plotly.graph_objs as go
import os
from TO_InstanceReader import InstanceReader
from TO_SolutionReader import Solution_Reader
from InstancePlotter import Instance_Plotter
from SolutionPlotter import SolutionPlotter


class SolutionAnimation:

    def __init__(self, instance_string, path_to_data_folder=os.getcwd()):
        self.instance_string = instance_string
        self.instance = InstanceReader(instance_string)
        self.sol = Solution_Reader(instance_string)
        self.instance_plotter_obj = Instance_Plotter(instance_string)
        self.solution_plotter_obj = SolutionPlotter(instance_string)

    def drawArena(self, modelName='', remainingFuel=0):
        task_trace = self.instance_plotter_obj.taskNodesTrace(remainingFuel)
        start_trace = self.instance_plotter_obj.startNodesTrace(self.instance.D_loc)
        # end_trace = endNodesTrace(E_loc)
        data = [task_trace, start_trace]

        for k in self.sol.arcsInOrder:
            edge_trace, node_info_trace = self.solution_plotter_obj.edgeTrace(self.instance.D_loc, self.sol.arcsInOrder[k])
            edge_trace.name = str(k)
            data.append(edge_trace)
            data.append(node_info_trace)

        layout = go.Layout(
            title='{}: {} robot(s), {} task(s), {} depot(s). f={:.1f}, Tmax={}'
                .format(modelName, len(self.instance.K), len(self.instance.T), len(self.instance.D), self.instance.L, self.instance.T_max, ),
            hovermode='closest',
            xaxis=dict(
                title='X-Coord',
                range=[0, 100]
                # ticklen= 5,
                # zeroline= False,
                # gridwidth= 2,
            ),
            yaxis=dict(
                title='Y-Coord'
                # ticklen= 5,
                # gridwidth= 2,
            ),
            showlegend=True

        )
        fig = go.Figure(data=data, layout=layout)
        return fig


    def play_and_save(self):
        # plotly animation
        fig = self.drawArena(self.instance_string)
        py.plot(fig)




def main():
    instance_prefix = 'R3D3T7F150Tmax600Iter0'

    video = SolutionAnimation(instance_prefix)
    video.play_and_save()



if __name__ == "__main__":
    main()


