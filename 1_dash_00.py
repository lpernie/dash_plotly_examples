# Code based on 'Learn how to create interactive plots and intelligent dashboards with Plotly, Python,
# and the Dash library!' From JOSE PORTILLA. https://github.com/Pierian-Data/Plotly-Dashboards-with-Dash
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash
import dash_core_components as dcc  # Describes the individual graph (it can be also a button or a table)
import dash_html_components as html  # Describes the layout of the page
from dash.dependencies import Input, Output, State  # For callback interactivity (will be used by the decorators)
import dash_auth
# import requests  # To perform web-scraping
import base64  # In order to import an image

# ---------------------------------------------------- Input Data ----------------------------------------------------
# HEX color dictionary (for your convenience)
colors = {'background': '#a39d9d', 'text': '3C56A2'}
border_color = 'black'
# A Markdown text to be used later
markdown_text = """
### My Text
* *This text will be italic*. 
* _This will also be italic_.  
    * [Dash User Guide](https://dash.plotly.com/dash-core-components/markdown). 
    * [Mark-down guide](https://www.markdownguide.org/basic-syntax/)
"""
# Get a df for inserting the plot later on
df = pd.read_csv('data/gapminderDataFiveYear.csv')
year_options = []  # The Dropdown menu will show all possible years. You select a year, it returns it as a float.
for year in df['year'].unique():
    year_options.append({'label': str(year), 'value': year})
# Get another df for another plot (a plot with 2 inputs)
df2 = pd.read_csv('data/mpg.csv')
df2['year'] = np.random.randint(-4, 5, len(df2)) * 0.1 + df2[
    'model_year']  # Year is alway a multiple of 10. This fix it.
features = df2.columns
# Get another df for another plot (multiple inputs/outputs)
df3 = pd.read_csv('data/wheels.csv')
# Scatter plot data for Selection Data
np.random.seed(10)
x1 = np.linspace(0.1, 5, 50)
x2 = np.linspace(5.1, 10, 50)
y = np.random.randint(0, 50, 50)
dfx1 = pd.DataFrame({'x': x1, 'y': y})
dfx2 = pd.DataFrame({'x': x1, 'y': y})
dfx3 = pd.DataFrame({'x': x2, 'y': y})
dfx = pd.concat([dfx1, dfx2, dfx3])


# Encode an image to add into the dashboard
def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())  # Read and image and encode it into a binary file.
    return 'data:image/png;base64,{}'.format(encoded.decode())  # This string is how html file can add an image.


# -----------------------------------    Start a Dash application    --------------------------------------------
# NOTE: You can print on the stdout the help menu for each method of dash
# print(help(html.Div))
# print(help(html.H1))
app = dash.Dash()
# Let's protect this dashboard
# HTTP Authorization: free protocol to protect a dashboard. You store username-password in the code, but you have to
#                     take care yourself of securely distribute those username-password to the users.
# Plotly OAuth: authentication is mantained by Plotly, but you have to pay a subscription
USERNAME_PWD = [['user1', '123'], ['user2', '456']]
auth = dash_auth.BasicAuth(app, USERNAME_PWD)

# Here you define the layout of your dashboard. You start with a Div: a container of spaces to use.
app.layout = html.Div(children=[
    # ---- Interval: this part refresh automatically the page ----
    html.H1(id='live-text-update'),
    dcc.Interval(id='interval-component',
                 interval=10000,  # 10k milliseconds = 10 seconds
                 n_intervals=0),  # You start counting the refreshes from zero
    # ---- H1 ----- It will appear as text.
    html.H1(
        children='My First Dashboard',  # Text you are displaying
        style={  # The sytyle how you dispaly it
            'textAlign': 'center',
            'color': colors['text'],
            'backgroundColor': 'red',
            'border': '3px ' + border_color + ' solid'  # Cannot use hex color
        }
    ),
    # ---- DROPDOWN ----
    html.Label(children='Cities', style={'color': colors['text']}),
    dcc.Dropdown(options=[{'label': 'New York City', 'value': 'NYC'},
                          {'label': 'San Francisco', 'value': 'SF'}],
                 value='SF'),  # Default value if label ios not specified.
    # ---- SLIDER ----
    html.Label('Slider', style={'color': colors['text']}),
    dcc.Slider(min=-10, max=10, step=1, value=0,
               marks={i: i for i in range(-10, 10)}),
    # ---- RADIO ITEMS ----
    html.P(  # This gives a new paragraph, so that this item is not overlapped to the previous one.
        html.Label('Radio Items', style={'color': colors['text']})
    ),
    dcc.RadioItems(options=[{'label': 'New York City', 'value': 'NYC'},
                            {'label': 'San Francisco', 'value': 'SF'}],
                   style={'color': colors['text']},
                   value='SF'),
    # ---- CALLBACK EXAMPLE: 1 INPUT + DIV ----
    html.Div(children=[  # You created a Div that has and Input on the first line, and a Div on the second line.
        dcc.Input(id='text-input', value='<insert value>', type='text'),  # Input Object, where you can write.
        html.Button(id='submit-button',  # This time the Input will affect the Output only after submitting the input
                    n_clicks=0,  # Variable that keep track on the number of clicks, not needed now
                    children='Submit here',
                    style={'fontSize': 24}),
        html.Div(children='', id='my-div')  # This is an empy Div where you will write the output of 'update_div'.
    ]),
    # ---- DIV ----
    html.Div(
        children=['DIV - 0 (Text)',
                  html.Div(children=['DIV - 1 (Div)'], style={'textAlign': 'center'})],
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    # ---- MARKDOWN
    dcc.Markdown(children=markdown_text),
    # ---- PLOT ----
    dcc.Graph(
        id='example-graph',  # Unique ID to refers to this plot.
        figure={  # Figure object, so that you can build the plot.
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
                'title': 'My Plot'
            }
        }
    ),
    # ---- INTERACTIVE PLOT ----
    dcc.Graph(id='graph'),  # You let it blank, since the decorator will fill its output.
    dcc.Dropdown(id='year-picker', options=year_options, value=df['year'].max()),  # Default year is the max year.
    # ---- INTERACTIVE PLOT with 2 inputs ----
    html.Div([dcc.Dropdown(id='xaxis',  # You place the Dropdown in a Div to custimize its individual style
                           options=[{'label': i, 'value': i} for i in features],
                           value='displacement')],
             style={'width': '48%', 'display': 'inline-block'}),
    html.Div([dcc.Dropdown(id='yaxis',
                           options=[{'label': i, 'value': i} for i in features],
                           value='mpg')],
             style={'width': '48%', 'display': 'inline-block'}),
    dcc.Graph(id='feature-graphic'),
    # ---- Multiple INPUTs/OUTPUTs ----
    html.Div([
        dcc.RadioItems(id='wheels',  # Input: you can select how many wheels
                       options=[{'lable': i, 'value': i} for i in df3['wheels'].unique()],
                       value=1),
        html.Div(id='wheels-output'),  # Output: text box where you read the number of wheels selected
        html.Hr(),
        dcc.RadioItems(id='colors',  # Input: you can select a color
                       options=[{'lable': i, 'value': i} for i in df3['color'].unique()],
                       value='blue'),
        html.Div(id='colors-output'),  # Output: text box where you read the color selected
        html.Img(id='display-img', src='children', height=300),  # The Image you will display
    ]),
    # ---- Hover Over Data ----
    html.Div([
        # Every Plot has a hoverData method that contain the info where the mouse is located.
        html.Div(dcc.Graph(id='wheel-plot', figure={'data': [go.Scatter(x=df3['color'],
                                                                        y=df3['wheels'],
                                                                        dy=1,  # Grid-line structure
                                                                        mode='markers',
                                                                        marker={'size': 15})],
                                                    'layout': go.Layout(title='Test',
                                                                        xaxis={'title': 'Color'},
                                                                        yaxis={'title': 'Wheels', 'nticks': 3},
                                                                        hovermode='closest')},
                           style={'width': '30%', 'float': 'left'})),  # The graph will use 30% of the space
        # This is an image that will change depedning on the data point selected by the mount on the prev graph.
        html.Div([html.Img(id='hover-data', src='children', height=300)],
                 style={'paddingTop': 35})
    ]),
    # ---- Selection DATA (select and see operation on selected data) ----
    html.Div([
        html.Div([dcc.Graph(id='plot',
                            figure={'data': [go.Scatter(x=dfx['x'],
                                                        y=dfx['y'],
                                                        mode='markers'
                                                        )],
                                    'layout': go.Layout(title='Scatter Plot', hovermode='closest')}
                            )
                  ], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            html.H1(id='density', style={'paddingTop': 25})
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'display': 'block'}),
    html.Div([
        html.Div(
            dcc.Graph(id='mpg-scatter',
                      figure={'data': [go.Scatter(x=df2['year'] + 1900,
                                                  y=df2['mpg'],
                                                  text=df2['name'],
                                                  hoverinfo='text + x + y',  # What to display on overData
                                                  mode='markers')],
                              'layout': go.Layout(title='MPG Data',
                                                  xaxis={'title': 'Model Year'},
                                                  yaxis={'title': 'MPG'},
                                                  hovermode='closest')}
                      ), style={'width': '50%', 'display': 'inline-block'}
        ),
        html.Div(
            dcc.Graph(id='mpg-line',
                      figure={'data': [go.Scatter(x=[0, 1],
                                                  y=[0, 1],
                                                  mode='lines')],
                              'layout': go.Layout(title='acceleration',
                                                  margin={'l': 0})  # Left marging=0, so this plot is next the prev one
                              }), style={'width': '20%', 'height': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Markdown(id='mpg-stats')], style={'width': '20%', 'height': '50%', 'display': 'inline-block'})
    ])
], style={'backgroundColor': colors['background']})  # Style of the initial container you crated at the beginning


# ---------------------------------------------------- Callbaks ----------------------------------------------------
@app.callback(Output('live-text-update', 'children'), [Input('interval-component', 'n_intervals')])
def update_layout(n):
    return f'Crash free for {n} refreshes.'


# Callback for filling the children of the Div with id='my-div', with the output of update_div when a Button is pressed
@app.callback(Output(component_id='my-div', component_property='children'),
              # The input is the Submit button (when you have a State in the callback). Otherwise is simply the Input.
              [Input(component_id='submit-button', component_property='n_clicks')],
              # If you have a State, you give him the Input text you want displayed once Submit is pressed.
              [State(component_id='text-input', component_property='value')])
def update_div(n_clicks, input_value):  # n_clicks is first because Input came before State
    return f'You entered: {input_value} and clicked {n_clicks} times.'  # It is not mandatory to use n_clicks.


# Callback to update the graph based on the year selected in the Dropdown menu
@app.callback(Output('graph', 'figure'),  # The Output is the Figure field of the graph.
              [Input('year-picker', 'value')])  # Input is the numeric value of the year you selected in the Dropdown
def update_figure(selected_year):
    filtered_df = df[df['year'] == selected_year]
    traces = []
    for continent_name in df['continent'].unique():
        df_by_continent = filtered_df[filtered_df['continent'] == continent_name]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            mode='markers',
            marker={'size': 15, 'opacity': 0.7},
            name=continent_name
        ))
    return {'data': traces, 'layout': go.Layout(title='My Plot',
                                                xaxis={'title': 'GDP per Capita', 'type': 'log'},
                                                yaxis={'title': 'Life Expectancy'})}


# Callback to update the graph using 2 Inputs
@app.callback(Output('feature-graphic', 'figure'), [Input('xaxis', 'value'), Input('yaxis', 'value')])
def update_graph(xaxis_name, yaxis_name):
    traces = [go.Scatter(
        x=df2[xaxis_name],
        y=df2[yaxis_name],
        text=df2['name'],
        mode='markers',
        marker={'size': 15, 'opacity': 0.5, 'line': {'width': 0.5, 'color': 'white'}},
        name=xaxis_name + ' vs ' + yaxis_name
    )]
    return {'data': traces, 'layout': go.Layout(title='My Plot2',
                                                xaxis={'title': xaxis_name},
                                                yaxis={'title': yaxis_name},
                                                hovermode='closest')}


# Callback to update the multi-input and multi-output plots
@app.callback(Output('wheels-output', 'children'), [Input('wheels', 'value')])
def callback_a(wheel_value):
    return f'You chose {wheel_value}'


@app.callback(Output('colors-output', 'children'), [Input('colors', 'value')])
def callback_b(color_value):
    return f'You chose {color_value}'


@app.callback(Output('display-img', 'src'), [Input('wheels', 'value'), Input('colors', 'value')])
def callback_img(wheel, color):
    path = 'data/Images/'
    return encode_image(path + df3[(df3['wheels'] == wheel) & (df3['color'] == color)]['image'].values[0])


# Here if the mouse is on a data point of the plot, you will display a different image.
@app.callback(Output('hover-data', 'src'),  # Output is the Pre for text display
              [Input('wheel-plot', 'clickData')])  # Input is clickData: info when the mouse clicks on a data point
#              [Input('wheel-plot', 'hoverData')])  # Input is the hoverData: info when the mouse is on a data point
def callback_image(hoverData):
    if hoverData is not None:
        wheel = hoverData['points'][0]['y']  # HoverData isthe info about the data point you are selecting
        color = hoverData['points'][0]['x']
        path = 'data/Images/'
        return encode_image(path + df3[(df3['wheels'] == wheel) & (df3['color'] == color)]['image'].values[0])


@app.callback(Output('density', 'children'),  # In the H1 with id=density you are populating the text
              [Input('plot', 'selectedData')])  # The function input are the selected data with Lasso or Box selection
def find_sensity(selectedData):
    if selectedData is not None:
        pts = len(selectedData['points'])
        rng_or_lp = list(selectedData.keys())
        rng_or_lp.remove('points')
        max_x = max(selectedData[rng_or_lp[0]]['x'])
        min_x = min(selectedData[rng_or_lp[0]]['x'])
        max_y = max(selectedData[rng_or_lp[0]]['y'])
        min_y = min(selectedData[rng_or_lp[0]]['y'])
        area = (max_x - min_x) * (max_y - min_y)
        d = pts / area
        return f'Density is {d:.2f}'


@app.callback(Output('mpg-line', 'figure'),
              [Input('mpg-scatter', 'hoverData')])
def callback_graph(hover_data):
    v_index = hover_data['points'][0]['pointIndex']
    figure = {'data': [go.Scatter(x=[0, 1],
                                  y=[0, 60 / df2.iloc[v_index]['acceleration']],  # Miles per minutes
                                  mode='lines',
                                  line={'width': 2 * df2.iloc[v_index]['cylinders']})],
              'layout': go.Layout(title=df2.iloc[v_index]['name'],
                                  xaxis={'visible': False},
                                  yaxis={'visible': False,
                                         'range': [0, 60 / df2['acceleration'].min()]},
                                  margin={'l': 0},
                                  height=300)}
    return figure


# Same
@app.callback(Output('mpg-stats', 'children'),
              [Input('mpg-scatter', 'hoverData')])
def callback_stats(hover_data):
    v_index = hover_data['points'][0]['pointIndex']
    stats = '''
    {} cylinders
    {} cc displacement
    From 0 to 60 mph in {} seconds
    '''.format(df2.iloc[v_index]['cylinders'], df2.iloc[v_index]['displacement'], df2.iloc[v_index]['acceleration'])
    return stats


if __name__ == '__main__':
    app.run_server()  # It generates the local host that contain the dashboard
