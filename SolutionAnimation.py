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

    def make_frame(self, node):
        # for k in self.instance.K:
        #     for node in self.sol.nodesInOrder[k]:
        x, y = self.instance.T_loc.get(node)

        return x

    def drawArena(self, modelName='', remainingFuel=0):
        task_trace = self.instance_plotter_obj.taskNodesTrace(remainingFuel)
        start_trace = self.instance_plotter_obj.startNodesTrace(self.instance.D_loc)
        # end_trace = endNodesTrace(E_loc)
        data = [task_trace, start_trace]

        edge_trace = {k:[] for k in self.instance.K}
        node_info_trace = {k:[] for k in self.instance.K}
        for k in self.sol.arcsInOrder:
            edge_trace[k], node_info_trace[k] = self.solution_plotter_obj.edgeTrace(self.instance.D_loc,
                                                                              self.sol.arcsInOrder[k])
            edge_trace[k].name = str(k)
            data.append(edge_trace[k])
            data.append(node_info_trace[k])

        layout = go.Layout(
            title='{}: {} robot(s), {} task(s), {} depot(s). f={:.1f}, Tmax={}'
                .format(modelName, len(self.instance.K), len(self.instance.T), len(self.instance.D), self.instance.L,
                        self.instance.T_max, ),
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
            showlegend=True,
            updatemenus=[{'type': 'buttons',
                          'buttons': [{'label': 'Play',
                                       'method': 'animate',
                                       'args': [None]}]}]
        )

        xx = [50, 60, 70, 80]
        yy = [50, 60, 70, 80]
        # for node in self.sol.nodesInOrder['K0']

        frames = [dict(data=[start_trace, task_trace,
                             dict(text='Animate',
                                  x=[xx[c]],
                                  y=[yy[c]],
                                  mode='markers+text',
                                  textposition='top center',
                                  name='Animated<br>',
                                  marker=dict(size=10,
                                              color='yellow'
                                              )
                                  )
                             ]
                       ) for c in range(4)
                  ]

        for f in frames:
            # for k in self.instance.K:
            f['data'].append(edge_trace['K0'])
            f['data'].append(node_info_trace['K0'])
            f['data'].append(edge_trace['K1'])
            f['data'].append(node_info_trace['K1'])
            # f['data'].append(edge_trace['K2'])
            # f['data'].append(node_info_trace['K2'])

        fig = go.Figure(data=data, layout=layout, frames=frames)
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
