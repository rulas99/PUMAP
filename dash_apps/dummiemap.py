import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import server
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from flask import session

def create_layout():
    layout = dcc.Loading(
        html.Div([
        dcc.Dropdown(
            id="dropdown-map_update",
            options=[
                {"label": 'Metro', "value": 'todos'},
                {"label": 'Metrobus', "value": 'amenazas'},
                {"label": 'Pumabus', "value": 'lesiones'}
            ],
            value='todos',
            ),
        html.Br(),
        html.Div(id="graph-map")
        ]),
        type='circle', fullscreen=True,
        loading_state={'is_loading': True},
        style={'backgroundColor': '#FFFFFF00'})
    return layout


@server.app_dash.callback(
    Output("graph-map", "children"), 
    [Input("dropdown-map_update", "value")])
def update_bar_chart(value):
    mapbox_center_lon=-99.1817107
    mapbox_center_lat=19.3268706

  
    fig = go.Figure(go.Scattermapbox(
        lat=[],
        lon=[],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
        text=['Montreal'],
    ))
    fig.update_layout(mapbox_zoom=13,
                        mapbox_style="open-street-map",
                        mapbox_center_lon=mapbox_center_lon,
                        mapbox_center_lat=mapbox_center_lat)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})            
    layout = html.Div([dcc.Graph(figure=fig, 
                                    config={'displayModeBar': False})])

    return layout









