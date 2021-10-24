import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_leaflet as dl

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
    url = "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"
    attribution = "<a href=https://www.google.com/maps/@24,-101.4,3274426m/data=!3m1!1e3/>Google Maps</a>"

    fig = dl.Map([dl.TileLayer(url=url, maxZoom=20, attribution=attribution), 
                 dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}})],
                 id="map", style={'width': '100%', 'height': '480px', 'margin': "auto", "display": "block"},
                 zoom=13.5, center=(19.32,-99.186)
                 )

    layout = html.Div([fig,html.Div(id="text")])

    return layout


@server.app_dash.callback(Output("text", "children"), [Input("map", "location_lat_lon_acc")])
def update_location(location):
    if location:
        lat,lon = location[0], location[1]
        #print(lat,lon)
        #return 
    else:
     pass