#import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc
#import dash_core_components as dcc
from dash import dcc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign
from dash.dependencies import Input, Output, State
from dash import callback_context

import server
from flask import session

from dash_apps.auxiliar_functions.here_api import hereRequestRoutes
from dash_apps.auxiliar_functions.mongo import getDataFromMongo
from dash_apps.auxiliar_functions.routes import get_hibryd_route, nodes, edges, G, poly_distance
from dash_apps.auxiliar_functions.html_parser import html_to_dash

from pandas import DataFrame

df = DataFrame(getDataFromMongo('geometries','food'))

opcI = [{"label":i, "value":i} for i in df.Servicio] + [{"label":"Todos", "value":"todo"}]

startText = getDataFromMongo('tabular','descriptions',query={'ID':3})[0]['HTML']

def create_layout():

    url = "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"
    attribution = "<a href=https://www.google.com/maps/@24,-101.4,3274426m/data=!3m1!1e3/>Google Maps</a>"

    mapa = dl.Map([dl.TileLayer(url=url, maxZoom=20, attribution=attribution),          
                 dl.LayerGroup(id="routes-f", children=[]),
                 dl.LayerGroup(id="points-f", children=[]),
                 dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True},'position':"bottomleft","drawCircle":False,
                                           'markerStyle':{'fillColor':'#38C8AE'}}),
                 dl.MeasureControl(position="bottomleft", primaryLengthUnit="meters", secondaryLengthUnit='kilometers', 
                                   primaryAreaUnit="sqmeters",secondaryAreaUnit="hectares",
                                   activeColor="#214097", completedColor="#972158")],
                 id="map-f", style={'width': '100%', 'height': '550px', 'margin': "auto", "display": "block"},
                 zoom=13.5, center=(19.32,-99.186), zoomControl=False
                 )

    origen = dcc.Dropdown(
            id="dropdown-f",
            options=opcI,
            placeholder='Seleccione un sitio de interés',
            value='todo'
            )

    destino = dcc.Dropdown(
            id="dropdown-ori-f",
            options=[
                {"label": 'Ubicación actual', "value": 'ubi'}
            ],
            placeholder='Seleccione un punto de origen',
            value='ubi'
            )

    layout = html.Div([
                        dbc.Row([dbc.Col(html.Div([html.H6('Lugares para comer'),origen],
                                         style={'padding': '1px 1px 15px 1px', 'text-align': 'center',
                                                'background': None, 'margin': '2px 2px 2px 2px',
                                                'position': 'relative', 'zIndex': 999}),sm=3),

                                dbc.Col(html.Div([html.A(dbc.Button('Ver!', id='ver-f', color='secondary', className='mr-1',
                                        size='md', style={'width': '130px','height': '40px','backgroundColor': '#31C4A5','border-color': '#2BD3BE'}, n_clicks=0))],
                                        style={'padding': '23px 1px 15px 1px', 'text-align': 'center',
                                               'margin': '2px 2px 2px 2px'}), sm=2),

                                dbc.Col(html.Div([html.H6('Ruta desde:'),destino],
                                        style={'padding': '1px 1px 15px 1px', 'text-align': 'center',
                                               'background': None, 'margin': '2px 2px 2px 2px'}),sm=2), 

                                dbc.Col(html.Div([html.A(dbc.Button('Calcular!', id='calcula-f', color='secondary', className='mr-1',
                                size='md', style={'width': '130px','height': '40px','backgroundColor': '#31C4A5','border-color': '#2BD3BE'}, n_clicks=0))],
                                style={'padding': '23px 1px 15px 1px', 'text-align': 'center',
                                       'margin': '2px 2px 2px 2px'}), sm=2),

                                dbc.Col(html.Div(id='distime-f',
                                        style={'padding': '30px 1px 15px 1px', 'text-align': 'left',
                                               'background': None, 'margin': '2px 2px 2px 2px'}),sm=3)

                                ], justify='center'),

                        dbc.Row([dbc.Col([html.Div([mapa], id="graph-map-f",
                                                  style={'padding': '3px 3px 3px 3px', 'text-align': 'center','background': None, 
                                                         'margin': '2px 2px 2px 2px','border':'1px gray solid',
                                                         'border-radius' : '7px'})],sm=10),

                                dbc.Col([html.Div(children=html_to_dash(startText)
                                    ,id="Info-f",style={'padding': '3px 5px 3px 3px', 'text-align': 'left','background': None, 
                                                          'margin': '2px 10px 2px 10px','border':'1px gray solid', 'height': '558px',
                                                          'border-radius' : '7px',"overflow-y": "scroll" })],sm=2)

                                ], justify='center'),
                        html.Div(html.Span('',id='coords-f',style={'font-size':'8pt','color': '#989898'}),
                            style={'padding': '0px 10px 3px 3px','text-align': 'left','background': None})])

    return layout

@server.app_dash.callback(Output("coords-f", "children"), 
                          Input("map-f", "location_lat_lon_acc"),)
def update_location(location):
    if location:
        ubi = location[0], location[1]
        session['ubi'] = ubi
        
        return f'lat: {ubi[0]}, lon: {ubi[1]}'

    else:
     pass


@server.app_dash.callback(Output("points-f","children"),
                          Output("Info-f","children"),
                          Input("ver-f","n_clicks"),
                          State("dropdown-f","value"), 
                          prevent_initial_call=True
                          )
def view_point(btn, point):
    icon = {
            "iconUrl": '/static/assets/target.png',
            "iconSize": [38, 38],  # size of the icon
            #"popupAnchor": [-3, -76]  # point from which the popup should open relative to the iconAnchor
           }
    
    child = children=html_to_dash(startText)

    ls = []
    if point != 'todo':
        datF = df[df.Servicio==point].copy()
        child = [html.H4('Detalles:')]
        child += [html.H6(f'{i}: {datF[i].iloc[0]}') for i in datF.iloc[:,1:-3].columns]
        if datF['LINK'].iloc[0]!='Sin link':
            child += [html.A(html.H6('Mayor información', style={'color': '#1C71F4'}),
                               href=datF['LINK'].iloc[0], target="_blank")]
    else:
        datF = df.copy()

    for row in datF.itertuples():
        ls.append(dict(name=row.Servicio, lat=row.Y, lon=row.X))

    markers =[dl.Marker(position=[c['lat'], c['lon']], icon=icon, children=dl.Popup(c['name']), autoPan=True) for c in ls]

    del datF, ls

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'ver-f' in changed_id:
        return markers, child 
    else:
        return None,None


@server.app_dash.callback(Output("routes-f", "children"), 
                          Output("distime-f", "children"),
                          Input("calcula-f", "n_clicks"),
                          State("dropdown-f", "value"),
                          State("dropdown-ori-f", "value"))
def get_route(btn, destino, origen):

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    if ('calcula-f' in changed_id) and destino!='todo':
        datF = df[df.Servicio==destino].copy()
        lat = datF.Y.iloc[0]
        lon = datF.X.iloc[0]

        poly = get_hibryd_route(session['ubi'],[lat,lon])
        dist, t = poly_distance(poly)

        #iconUrl = "/static/assets/paws.png"
        #marker = dict(rotate=True, markerOptions=dict(icon=dict(iconUrl=iconUrl, iconSize=[50,50])))

        patterns = [dict(repeat=20,dash=dict(pixelSize=10, pathOptions=dict(color='#29D18F', weight=3, opacity=0.9))),
                    dict(offset='5%', repeat='5%', )] #
        rotated_markers = dl.PolylineDecorator(positions=poly, patterns=patterns)

        return rotated_markers, html.P(f'Aprox. {dist} metros en {t} min.',style={'font-size':'16px'})

    else:
     pass

