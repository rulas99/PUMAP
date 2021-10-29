import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_leaflet as dl
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import server
from flask import session

from dash_apps.auxiliar_functions.here_api import hereRequestRoutes

def create_layout():

    url = "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"
    attribution = "<a href=https://www.google.com/maps/@24,-101.4,3274426m/data=!3m1!1e3/>Google Maps</a>"

    mapa = dl.Map([dl.TileLayer(url=url, maxZoom=20, attribution=attribution),  
                 dl.LayerGroup(id="routes", children=[]),
                 dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}})],
                 id="map", style={'width': '100%', 'height': '560px', 'margin': "auto", "display": "block"},
                 zoom=13.5, center=(19.32,-99.186)
                 )

    origen = dcc.Dropdown(
            id="dropdown-map_update",
            options=[
                {"label": 'Metro', "value": 'todos'},
                {"label": 'Metrobus', "value": 'amenazas'},
                {"label": 'Pumabus', "value": 'lesiones'},
                {"title": 'origen'}
            ],
            value='todos',
            )

    destino = dcc.Dropdown(
            id="dropdown-map_update2",
            options=[
                {"label": 'Metro', "value": 'todos'},
                {"label": 'Metrobus', "value": 'amenazas'},
                {"label": 'Pumabus', "value": 'lesiones'},
                {"title": 'origen'}
            ],
            value='todos',
            )

    layout = html.Div([
                        dbc.Row([dbc.Col(html.Div([html.H6('Origen'),origen],
                                         style={'padding': '1px 1px 15px 1px', 'text-align': 'center',
                                                'background': None, 'margin': '2px 2px 2px 2px'}),sm=4),

                                dbc.Col(html.Div([html.H6('Destino'),destino],
                                        style={'padding': '1px 1px 15px 1px', 'text-align': 'center',
                                               'background': None, 'margin': '2px 2px 2px 2px'}),sm=4), 

                                dbc.Col(html.Div([html.A(dbc.Button('Calcular!', id='calcula', color='secondary', className='mr-1',
                                size='md', style={'width': '130px','height': '40px','backgroundColor': '#31C4A5','border-color': '#2BD3BE'}, n_clicks=0))],
                                style={'padding': '23px 1px 15px 1px', 'text-align': 'center',
                                       'margin': '2px 2px 2px 2px'}), sm=3)

                                ], no_gutters=True, justify='center'),

                        dbc.Row([dbc.Col([html.Div([mapa], id="graph-map",
                                                  style={'padding': '3px 3px 3px 3px', 'text-align': 'center','background': None, 
                                                         'margin': '2px 2px 2px 2px','border':'1px gray solid',
                                                         'border-radius' : '7px'})],sm=10),

                                dbc.Col([html.Div([html.H4('Detalles:')],id="Info",
                                                   style={'padding': '3px 5px 3px 3px', 'text-align': 'left','background': None, 
                                                          'margin': '2px 10px 2px 10px','border':'1px gray solid', 'height': '568px',
                                                          'border-radius' : '7px'})],sm=2)

                                ], no_gutters=True, justify='center')
                        ])

    return layout

@server.app_dash.callback(Output("routes", "children"), [Input("map", "location_lat_lon_acc")])
def update_location(location):
    if location:
        ubi = location[0], location[1]
        session['ubi'] = ubi
        
        poly = hereRequestRoutes(ubi,[19.32471,-99.18775])

        iconUrl = "/static/assets/paws.png"
        marker = dict(rotate=True, markerOptions=dict(icon=dict(iconUrl=iconUrl, iconSize=[50,50])))

        patterns = [dict(repeat=20,dash=dict(pixelSize=10, pathOptions=dict(color='#29D18F', weight=3, opacity=0.9))),
                    dict(offset='5%', repeat='5%', marker=marker)]
        rotated_markers = dl.PolylineDecorator(positions=poly, patterns=patterns)

        return rotated_markers

    else:
     pass