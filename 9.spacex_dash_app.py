import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the data into a pandas DataFrame
spacex_launch_dash = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_launch_dash['Payload Mass (kg)'].max()
min_payload = spacex_launch_dash['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown for site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here"
    ),
    
    # Pie chart for success counts
    dcc.Graph(id='success-pie-chart'),
    
    html.Br(),
    html.P("Payload range (Kg):"),
    
    # Slider for payload range selection
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload, max=max_payload, step=1000,
        marks={min_payload: str(min_payload), max_payload: str(max_payload)},
        value=[min_payload, max_payload]
    ),
    
    # Scatter chart for payload vs. launch success correlation
    dcc.Graph(id='success-payload-scatter-chart')
])

# Callback for updating pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_launch_dash, names='class', title='Success Launches by Class')
    else:
        filtered_df = spacex_launch_dash[spacex_launch_dash['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', title=f'Success Launches by Class - {entered_site}')
    return fig

# Callback for updating scatter chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='payload-slider', component_property='value'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_scatter_chart(payload_range, entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_launch_dash[
            (spacex_launch_dash['Payload Mass (kg)'] >= payload_range[0]) &
            (spacex_launch_dash['Payload Mass (kg)'] <= payload_range[1])
        ]
    else:
        filtered_df = spacex_launch_dash[
            (spacex_launch_dash['Payload Mass (kg)'] >= payload_range[0]) &
            (spacex_launch_dash['Payload Mass (kg)'] <= payload_range[1]) &
            (spacex_launch_dash['Launch Site'] == entered_site)
        ]
    
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='class',
        title='Correlation between Payload and Launch Success',
        labels={'class': 'Launch Success'}
    )
    fig.update_layout(yaxis=dict(tickvals=[0, 1], ticktext=['Failed', 'Successful']))

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
