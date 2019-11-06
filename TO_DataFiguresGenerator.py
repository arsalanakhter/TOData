import pandas as pd
import plotly.offline as py
import plotly.graph_objects as go
import plotly.io as pio


class DataFiguresGenerator:

    def __init__(self):
        pass

    def average_times_plot(self):
        row_fields = [' ', ' .1', ' .2', 'F1.3', 'F2.3', 'F3.3', 'F4.3']
        col_fields = ['Avg']
        df = pd.read_csv('aggregatedDataMinAvgMax.csv', usecols=row_fields, index_col=False)
        print(df[df[' .2'].str.contains(col_fields[0])]['F2.3'][0:3].tolist())
        print(df[df[' .2'].str.contains(col_fields[0])]['F2.3'][3:6].tolist())
        print(df[df[' .2'].str.contains(col_fields[0])]['F2.3'][6:9].tolist())
        fig = self.draw_figure()

        # Create Traces
        F1Tmax150 = self.F1_trace()
        zdata = df[df[' .2'].str.contains(col_fields[0])]['F1.3'][0:3].tolist()
        F1Tmax150.update(x=[50, 75, 150], y=[150, 150, 150], z = zdata)
        fig.add_trace(F1Tmax150)

        F2Tmax150 = self.F2_trace()
        zdata = df[df[' .2'].str.contains(col_fields[0])]['F2.3'][0:3].tolist()
        F2Tmax150.update(x=[50, 75, 150], y=[150, 150, 150], z = zdata)
        fig.add_trace(F2Tmax150)

        F3Tmax150 = self.F3_trace()
        zdata = df[df[' .2'].str.contains(col_fields[0])]['F3.3'][0:3].tolist()
        F3Tmax150.update(x=[50, 75, 150], y=[150, 150, 150], z = zdata)
        fig.add_trace(F3Tmax150)

        F4Tmax150 = self.F4_trace()
        zdata = df[df[' .2'].str.contains(col_fields[0])]['F4.3'][0:3].tolist()
        F4Tmax150.update(x=[50, 75, 150], y=[150, 150, 150], z = zdata)
        fig.add_trace(F4Tmax150)


        #Tmax 300
        F1Tmax150 = self.F1_trace()
        zdata = df[df[' .2'].str.contains(col_fields[0])]['F1.3'][3:6].tolist()
        F1Tmax150.update(x=[50, 75, 150], y=[300, 300, 300], z = zdata)
        fig.add_trace(F1Tmax150)

        F2Tmax150 = self.F2_trace()
        zdata = df[df[' .2'].str.contains(col_fields[0])]['F2.3'][3:6].tolist()
        F2Tmax150.update(x=[50, 75, 150], y=[300, 300, 300], z = zdata)
        fig.add_trace(F2Tmax150)

        F3Tmax150 = self.F3_trace()
        zdata = df[df[' .2'].str.contains(col_fields[0])]['F3.3'][3:6].tolist()
        F3Tmax150.update(x=[50, 75, 150], y=[300, 300, 300], z = zdata)
        fig.add_trace(F3Tmax150)

        F4Tmax150 = self.F4_trace()
        zdata = df[df[' .2'].str.contains(col_fields[0])]['F4.3'][3:6].tolist()
        F4Tmax150.update(x=[50, 75, 150], y=[300, 300, 300], z = zdata)
        fig.add_trace(F4Tmax150)


        #Tmax 600
        F1Tmax150 = self.F1_trace()
        zdata = df[df[' .2'].str.contains(col_fields[0])]['F1.3'][6:9].tolist()
        F1Tmax150.update(x=[50, 75, 150], y=[600, 600, 600], z = zdata)
        fig.add_trace(F1Tmax150)

        F2Tmax150 = self.F2_trace()
        zdata = df[df[' .2'].str.contains(col_fields[0])]['F2.3'][6:9].tolist()
        F2Tmax150.update(x=[50, 75, 150], y=[600, 600, 600], z = zdata)
        fig.add_trace(F2Tmax150)

        F3Tmax150 = self.F3_trace()
        zdata = df[df[' .2'].str.contains(col_fields[0])]['F3.3'][6:9].tolist()
        F3Tmax150.update(x=[50, 75, 150], y=[600, 600, 600], z = zdata)
        fig.add_trace(F3Tmax150)

        F4Tmax150 = self.F4_trace()
        zdata = df[df[' .2'].str.contains(col_fields[0])]['F4.3'][6:9].tolist()
        F4Tmax150.update(x=[50, 75, 150], y=[600, 600, 600], z = zdata)
        fig.add_trace(F4Tmax150)

        

        
        #pio.write_image(fig, 'pic_23.png', width = 1280, height = 1024)
        py.plot(fig, include_mathjax='cdn')
        #fig.write_image("figures/fig1.svg")




    def individual_trace(self):
        # Basic trace to be used to create other traces/lines
        trace = go.Scatter3d(
            text=[],
            hovertext=[],
            x=[],
            y=[],
            z=[],
            mode='markers+lines',
            textposition='bottom right',
            # hoverinfo='text',
            line=dict(
                color='darkblue',
                width=2
            ),
            name='',
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
        return trace

    def F1_trace(self):
        new_trace = self.individual_trace()
        new_trace.name = 'F1'
        new_trace.marker.color = 'red'
        new_trace.line.color = 'darkred'
        return new_trace

    def F2_trace(self):
        new_trace = self.individual_trace()
        new_trace.name = 'F2'
        new_trace.marker.color = 'blue'
        new_trace.line.color = 'darkblue'
        return new_trace

    def F3_trace(self):
        new_trace = self.individual_trace()
        new_trace.name = 'F3'
        new_trace.marker.color = 'green'
        new_trace.line.color = 'darkgreen'
        return new_trace

    def F4_trace(self):
        new_trace = self.individual_trace()
        new_trace.name = 'F4'
        new_trace.marker.color = 'violet'
        new_trace.line.color = 'darkviolet'
        return new_trace

    def draw_figure(self):
        data=[]
        layout = go.Layout(
            title='Average Times',
            width=800,
            height=700,
            autosize=False,
            scene=dict(
                xaxis_title=r"$\tau$",
                yaxis_title=r"$T_{max}$",
                zaxis_title=r"Computation Time",
                camera=dict(
                    up=dict(
                        x=0,
                        y=0,
                        z=1
                    ),
                    eye=dict(
                        x=0,
                        y=1.0707,
                        z=1,
                    )
                ),
                aspectratio = dict( x=1, y=1, z=0.7 ),
                aspectmode = 'manual'
            ),
            showlegend=True
        )
        fig = go.Figure(data=data, layout=layout)
        return fig





def main():
    fig_generator = DataFiguresGenerator()
    fig_generator.average_times_plot()

if __name__ == "__main__":
    main()
