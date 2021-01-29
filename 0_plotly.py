# Code based on 'Learn how to create interactive plots and intelligent dashboards with Plotly, Python,
# and the Dash library!' From JOSE PORTILLA.
import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly import tools

justlast = True
# SCATTER PLOT X and Y values  ----------------------------------------------------------------------------------
np.random.seed(42)
random_x = np.random.randint(1, 101, 100)  # 100 random integers from 1 to 100.
random_y = np.random.randint(1, 101, 100)

# Create the data to plot. It has to be inside a list.
data = [go.Scatter(x=random_x, y=random_y, mode='markers',
                   marker=dict(size=12,
                               color='rgb(51,204,153)',  # You can either specify the color, or use define it using rgb.
                               symbol='pentagon',
                               line=dict(width=2)
                               )
                   )]
# Create a layout to customize the plot
layout = go.Layout(title='Hello',
                   xaxis=dict(title='MY X AXIS'),
                   yaxis=dict(title='MY Y AXIS'),
                   hovermode='closest')  # mouse indicate the closest point
# Plot without a layout
if not justlast:
    pyo.plot(data, filename='images/scatter_00.html')
# Plot with a layout
if not justlast:
    fig = go.Figure(data=data, layout=layout)
    pyo.plot(fig, filename='images/scatter_01.html')  # You can plot [go.Scatter] or a go.Figure

# Line Chart Plot X and Y values -------------------------------------------------------------------------------
np.random.seed(56)
x_values = np.linspace(0, 1, 100)  # 100 values from 0 to 1 equally spaced
y_values = np.random.randn(100)

# Create the data to plot
trace0 = go.Scatter(x=x_values, y=y_values+5, mode='markers', name='mymarkers')
trace1 = go.Scatter(x=x_values, y=y_values, mode='lines', name='mylines')
trace2 = go.Scatter(x=x_values, y=y_values-5, mode='lines+markers', name='both')
data = [trace0, trace1, trace2]
# Create a layout
layout = go.Layout(title='Line Chart')
# Plot
if not justlast:
    fig = go.Figure(data=data, layout=layout)
    pyo.plot(fig, filename='images/line_00.html')

# Line Chart Plot from Pandas
df = pd.read_csv('data/nst-est2017-alldata.csv')
df2 = df[df['DIVISION'] == '1']
df2.set_index('NAME', inplace=True)  # implace=True means that you do not have to do df2 = df2.set_index('NAME')
list_of_pop_col = [col for col in df2.columns if col.startswith('POP')]
df2 = df2[list_of_pop_col]

data = [go.Scatter(x=df2.columns,  # X axis represents POP in each year, that is the column name (POP2018, POP2019..)
                   y=df2.loc[name],  # Y axis is a vector with the pop value for each year (for that index, i.e. plot)
                   mode='lines') for name in df2.index]  # Each curve is a different place (the index of df2)
if not justlast:
    pyo.plot(data, filename='images/line_01.html')

# Exercise Line Chart
df = pd.read_csv('data/2010YumaAZ.csv')
days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
data = [go.Scatter(x=df[df['DAY'] == day]['LST_TIME'],
                   y=df[df['DAY'] == day]['T_HR_AVG'],
                   mode='lines', name=day) for day in days]
layout = go.Layout(title='Line Chart', xaxis=dict(title='TIME'), yaxis=dict(title='TEMPERATURE'), hovermode='closest')
fig = go.Figure(data=data, layout=layout)
if not justlast:
    pyo.plot(fig, filename='images/line_02.html')

# BAR CHART  -------------------------------------------------------------------------------------------------
df = pd.read_csv('data/2018WinterOlympics.csv')
data = [go.Bar(
    x=df['NOC'],  # NOC stands for National Olympic Committee
    y=df['Total']
)]
layout = go.Layout(title='2018 Winter Olympic Medals by Country')
fig = go.Figure(data=data, layout=layout)
if not justlast:
    pyo.plot(fig, filename='images/line_00.html')

# More complex version
trace1 = go.Bar(
    x=df.sort_values(by='Gold', ascending=False)['NOC'],  # NOC stands for National Olympic Committee
    y=df.sort_values(by='Gold', ascending=False)['Gold'],
    name='Gold',
    marker=dict(color='#FFD700')  # set the marker color to gold
)
trace2 = go.Bar(
    x=df.sort_values(by='Gold', ascending=False)['NOC'],
    y=df.sort_values(by='Gold', ascending=False)['Silver'],
    name='Silver',
    marker=dict(color='#9EA0A1')  # set the marker color to silver
)
trace3 = go.Bar(
    x=df.sort_values(by='Gold', ascending=False)['NOC'],
    y=df.sort_values(by='Gold', ascending=False)['Bronze'],
    name='Bronze',
    marker=dict(color='#CD7F32')  # set the marker color to bronze
)
data = [trace1, trace2, trace3]
layout = go.Layout(title='2018 Winter Olympic Medals by Country',
                   barmode='stack')
fig = go.Figure(data=data, layout=layout)
if not justlast:
    pyo.plot(fig, filename='images/line_01.html')

# BUBBLE PLOTS  (a scatter plot where the marker size depends on a thisr variable)------------------------------------
df = pd.read_csv('data/mpg.csv')
data = [go.Scatter(x=df['horsepower'],
                   y=df['mpg'],
                   text=df['name'],  # Extra info that will appear when you pla e the mouse on a point.
                   mode='markers',
                   # Since the 'cylinders' variable ios small, you add a factor two to make it visible
                   marker=dict(size=2*df['cylinders'],
                               color=df['weight'],
                               showscale=True))]  # This is the part where you make the marker size variable
layout = go.Layout(title='Bubble Chart', hovermode='closest',
                   xaxis=dict(title='horsepower'),
                   yaxis=dict(title='mpg'))
fig = go.Figure(data=data, layout=layout)
if not justlast:
    pyo.plot(fig, filename='images/bubble_00.html')

# BOX PLOTS --------------------------------------------------------------------------------------------------------
df = pd.read_csv('data/abalone.csv')
a = np.random.choice(df['rings'], 30, replace=False)
b = np.random.choice(df['rings'], 100, replace=False)
data = [go.Box(y=a, name='A'),
        go.Box(y=b, name='B')]
layout = go.Layout(title='Comparison of two samples taken from the same population')
fig = go.Figure(data=data, layout=layout)
if not justlast:
    pyo.plot(fig, filename='images/box_00.html')

# HISTOGRAMS --------------------------------------------------------------------------------------------------------
df = pd.read_csv('data/mpg.csv')
data = [go.Histogram(x=df['mpg'],
                     xbins=dict(start=0, end=50, size=2))]
layout = go.Layout(title='histograms')
fig = go.Figure(data=data, layout=layout)
if not justlast:
    pyo.plot(fig, filename='images/box_00.html')

# DIST PLOTS --------------------------------------------------------------------------------------------------------
df = pd.read_csv('data/iris.csv')
trace0 = df[df['class'] == 'Iris-setosa']['petal_length']
trace1 = df[df['class'] == 'Iris-versicolor']['petal_length']
trace2 = df[df['class'] == 'Iris-virginica']['petal_length']
data = [trace0, trace1, trace2]
group_labels = ['Iris Setosa', 'Iris Versicolor', 'Iris Virginica']
fig = ff.create_distplot(data, group_labels, bin_size=[0.1, 0.2, 0.2])
if not justlast:
    pyo.plot(fig, filename='images/dist_00.html')

# HEAT MAP + SUBPLOTS------------------------------------------------------------------------------------------------
df = pd.read_csv('data/flights.csv')
trace1 = go.Heatmap(
    x=df['year'],
    y=df['month'],
    z=df['passengers'])
trace2 = go.Heatmap(
    x=df['year'],
    y=df['month'],
    z=df['passengers'])
fig = tools.make_subplots(rows=1,
                          cols=2,
                          subplot_titles=['v1', 'v2'],
                          shared_yaxes=True)  # Shate the same y-axis
fig.append_trace(trace1, 1, 1)  # append the plot numnber 1 in the subplot on raw=1 and col=1
fig.append_trace(trace2, 1, 2)
fig['layout'].update(title='HEAT MAP')
pyo.plot(fig, filename='images/heat_00.html')
