# Video

import plotly.offline as py
import plotly.graph_objs as go
import os
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
import numpy as np
import  random as rnd
from TO_InstanceReader import InstanceReader
from TO_SolutionReader import Solution_Reader
from InstancePlotter import Instance_Plotter
from SolutionPlotter import SolutionPlotter


class SolutionAnimation:

    def __init__(self, instance_string):
        self.instance_string = instance_string
        self.instance = InstanceReader(instance_string)
        self.sol = Solution_Reader(instance_string)
        self.instance_plotter_obj = Instance_Plotter(instance_string)
        self.solution_plotter_obj = SolutionPlotter(instance_string)

        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
        self.ax.grid(True, lw=0.5)
        plt.title(instance_string)
        self.line, = self.ax.plot([], [], 'k*', markersize=8)
        self.edge, = self.ax.plot([], [])
        self.edge_trace = {k: {'x': [], 'y': [], 'c': 'w'} for k in self.instance.K}
        self.expanded_trace = {k: {'x': [], 'y': []} for k in self.instance.K}
        self.node_list = {k: [] for k in self.instance.K}
        self.ann_list = []
        self.fuel_box = []
        self.plot_base()


    ''' Animation using plotly '''
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

        max_frames = max([len(self.sol.nodesInOrder[k]) for k in self.instance.K])
        xx = {'F'+str(c): [] for c in range(max_frames)}
        yy = {'F'+str(c): [] for c in range(max_frames)}
        for c in range(max_frames):
            for k in self.instance.K:
                if(c < len(self.sol.nodesInOrder[k])):
                    tempx, tempy = self.instance.N_loc.get(self.sol.nodesInOrder[k][c])
                    xx['F' + str(c)].append(tempx)
                    yy['F' + str(c)].append(tempy)
                else:
                    xx['F' + str(c)].append(self.instance.N_loc.get(self.sol.nodesInOrder[k][-1]))
                    yy['F' + str(c)].append(self.instance.N_loc.get(self.sol.nodesInOrder[k][-1]))


        frames = [dict(data=[start_trace, task_trace,
                             dict(text=[str(k) for k in self.instance.K],
                                  x=xx['F'+str(c)],
                                  y=yy['F'+str(c)],
                                  mode='markers+text',
                                  textposition='top center',
                                  name='Robots<br>',
                                  marker=dict(size=10,
                                              color='black'
                                              )
                                  )
                             ]
                       ) for c in range(max_frames)
                  ]

        # TODO: fix error in generalizing for edge_trace
        for f in frames:
            for k in ['K2']:     # self.instance.K:
                f['data'].append(edge_trace[k])
                f['data'].append(node_info_trace[k])

        fig = go.Figure(data=data, layout=layout, frames=frames)
        return fig


    def play_and_save(self):
        # plotly animation
        fig = self.drawArena(self.instance_string)
        py.plot(fig)



    ''' Animation using matplotlib '''
    def plot_base(self):
        disp_text = []
        startTrace = {'x': [], 'y': []}

        for s in self.instance.D_loc:
            x, y = self.instance.D_loc.get(s)
            disp_text.append(s)
            startTrace['x'].append(x)
            startTrace['y'].append(y)
        self.ax.plot(startTrace['x'], startTrace['y'], 'bo', markersize=8)
        for i, txt in enumerate(disp_text):
            self.ax.annotate(txt, (startTrace['x'][i] + 1, startTrace['y'][i] + 0.6))

        disp_text = []
        taskTrace = {'x': [], 'y': []}
        for t in self.instance.T_loc:
            x, y = self.instance.T_loc.get(t)
            disp_text.append(t)
            taskTrace['x'] += tuple([x])
            taskTrace['y'] += tuple([y])
        self.ax.plot(taskTrace['x'], taskTrace['y'], 'go')
        for i, txt in enumerate(disp_text):
            self.ax.annotate(txt, (taskTrace['x'][i] + 1, taskTrace['y'][i]))

        colors = ['r', 'y', 'm', 'c']
        N_loc = {**self.instance.T_loc, **self.instance.D_loc, **self.instance.S_loc, **self.instance.E_loc}
        for k in self.instance.K:
            for arc in self.sol.arcsInOrder[k]:
                x0, y0 = N_loc.get(arc[0])
                x1, y1 = N_loc.get(arc[1])
                self.edge_trace[k]['x'] += tuple([x0, x1])
                self.edge_trace[k]['y'] += tuple([y0, y1])

                expand_10 = list(zip(np.linspace(x0, x1, 6), np.linspace(y0, y1, 6)))
                for i in range(len(expand_10)):
                    self.expanded_trace[k]['x'].append(expand_10[i][0])
                    self.expanded_trace[k]['y'].append(expand_10[i][1])
                    self.node_list[k].append(arc[0])

            self.edge_trace[k]['c'] = colors[rnd.randint(0, len(colors) - 1)]
            self.ax.plot(self.edge_trace[k]['x'], self.edge_trace[k]['y'], '--', lw=0.8, color=self.edge_trace[k]['c'])

    # animation function, called sequentially
    def animate(self, i):
        for ann in self.ann_list:
            ann.remove()
        self.ann_list[:] = []

        xx = []
        yy = []
        for j, k in enumerate(self.instance.K):
            if i < len(self.expanded_trace[k]['x']):
                xx.append(self.expanded_trace[k]['x'][i])
                yy.append(self.expanded_trace[k]['y'][i])
            else:
                xx.append(self.expanded_trace[k]['x'][-1])
                yy.append(self.expanded_trace[k]['y'][-1])
        self.line.set_data(xx, yy)

        # TODO: automate annotations
        txt0 = self.ax.annotate(self.instance.K[0], (xx[0] - 2, yy[0] + 2))
        txt1 = self.ax.annotate(self.instance.K[1], (xx[1] - 2, yy[1] + 2))
        txt2 = self.ax.annotate(self.instance.K[2], (xx[2] - 2, yy[2] + 2))
        self.ann_list.append(txt0)
        self.ann_list.append(txt1)
        self.ann_list.append(txt2)

        # print remaining fuel
        disp_text = "Remaining Fuel: \n"
        for k in self.instance.K:
            if i < len(self.node_list[k]) and self.node_list[k][i] in self.instance.T:
                fuel = np.round(self.sol.remainingFuel[self.node_list[k][i]], 2)
                # print(fuel)
            else:
                fuel = self.instance.L
            disp_text += k + ": " + str(fuel) + "  "
        at = AnchoredText(disp_text, prop=dict(size=8), frameon=True, loc=4)
        at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
        self.ax.add_artist(at)
        self.fuel_box.append(at)

        return self.line, self.edge, at,


def main():
    instance_prefix = 'R3D3T7F150Tmax600Iter4'

    video = SolutionAnimation(instance_prefix)

    # For plotly
    # video.play_and_save()

    # Matplotlib
    max_trace = max([len(video.expanded_trace[k]['x']) for k in video.instance.K])
    anim = animation.FuncAnimation(video.fig, video.animate, frames=max_trace, interval=1000, blit=True)
    anim.save('minmax.mp4', fps=1)#, extra_args=['-vcodec', 'libx264'])

    plt.show()


if __name__ == "__main__":
    main()
