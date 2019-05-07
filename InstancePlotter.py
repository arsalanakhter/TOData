# Plot the Instance
# Should take the name of the Instance string, and plot

import plotly.offline as py
import plotly.graph_objs as go
from TO_InstanceReader import InstanceReader
import os


class Instance_Plotter(InstanceReader):

    def __init__(self, instance_string, path_to_data_folder=os.getcwd()):
        InstanceReader.__init__(self, instance_string, path_to_data_folder)
        self.readData()

    def taskNodesTrace(self, remainingFuel=0):
        taskTrace = go.Scatter(
            text=[],
            hovertext=[],
            x=[],
            y=[],
            mode='markers+text',
            textposition='bottom right',
            # hoverinfo='text',
            name='<br>Task Locations<br>',
            marker=dict(
                size=6,
                color='blue',
                line=dict(
                    # color='rgba(217, 217, 217, 0.14)',
                    width=0.5
                ),
                opacity=0.8
            )
        )

        for t in self.T_loc:
            x, y = self.T_loc.get(t)
            # disp_text = 'NodeID: ' + t + '<br>Reward: ' + \
            #    str(self.R[t]) + '<br>f_left: ' + \
            #    "{0:.2f}".format(remainingFuel[t])
            disp_text = 'NodeID: ' + t
            taskTrace['x'] += tuple([x])
            taskTrace['y'] += tuple([y])
            taskTrace['text'] += tuple([t])
            taskTrace['hovertext'] += tuple([disp_text])
        return taskTrace

    def startNodesTrace(self, S_loc):
        startTrace = go.Scatter(
            text=[],
            hovertext=[],
            x=[],
            y=[],
            mode='markers+text',
            textposition='top center',
            # hoverinfo='text',
            name='Refueling Locations<br>',
            marker=dict(
                size=12,
                color='green',
                line=dict(
                    # color='rgba(217, 217, 217, 0.14)',
                    width=0.5
                ),
                opacity=0.8
            )
        )

        for s in S_loc:
            x, y = S_loc.get(s)
            # + '<br>f_left: ' + "{0:.2f}".format(f_left)
            disp_text = 'NodeID: ' + s
            startTrace['x'] += tuple([x])
            startTrace['y'] += tuple([y])
            startTrace['text'] += tuple([s])
            startTrace['hovertext'] += tuple([disp_text])
        return startTrace

    def drawArena(self, modelName='', remainingFuel=0):
        task_trace = self.taskNodesTrace(remainingFuel)
        start_trace = self.startNodesTrace(self.D_loc)
        # end_trace = endNodesTrace(E_loc)
        data = [task_trace, start_trace]

        layout = go.Layout(
            title='{}: {} robot(s), {} task(s), {} depot(s). f={:.1f}, Tmax={}'
            .format(modelName, len(self.K), len(self.T), len(self.D), self.L, self.T_max,),
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

    def create_plot_and_show(self):
        fig = self.drawArena(self.instance_string)
        py.plot(fig)


def main():
    # instance_prefix = 'R3D2T3F150Tmax600Iter'
    instance_prefix = 'R3D3T7F50Tmax600Iter'
    no_of_instances = 1
    for i in range(no_of_instances):
        instance_name = instance_prefix + str(i)
        plot = Instance_Plotter(instance_name)
        plot.create_plot_and_show()


if __name__ == "__main__":
    main()
