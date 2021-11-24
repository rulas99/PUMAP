import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign
from dash.dependencies import Input, Output, State
from dash import callback_context

import server
from flask import session

from dash_apps.auxiliar_functions.here_api import hereRequestRoutes
from dash_apps.auxiliar_functions.mongo import getDataFromMongo
from dash_apps.auxiliar_functions.routes import get_hibryd_route, nodes, edges, G

from pandas import DataFrame

df = DataFrame(getDataFromMongo('geometries','interest'))

opcI = [{"label":i, "value":i} for i in df.sitio] + [{"label":"Todos", "value":"todo"}]

def create_layout():

    url = "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"
    attribution = "<a href=https://www.google.com/maps/@24,-101.4,3274426m/data=!3m1!1e3/>Google Maps</a>"

    mapa = dl.Map([dl.TileLayer(url=url, maxZoom=20, attribution=attribution),          
                 dl.LayerGroup(id="routes-id", children=[]),
                 dl.LayerGroup(id="points-id", children=[]),
                 dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True},'position':"bottomleft","drawCircle":False,
                                           'markerStyle':{'fillColor':'#38C8AE'}}),
                 dl.MeasureControl(position="bottomleft", primaryLengthUnit="meters", secondaryLengthUnit='kilometers', 
                                   primaryAreaUnit="sqmeters",secondaryAreaUnit="hectares",
                                   activeColor="#214097", completedColor="#972158")],
                 id="map-id", style={'width': '100%', 'height': '560px', 'margin': "auto", "display": "block"},
                 zoom=13.5, center=(19.32,-99.186), zoomControl=False
                 )

    origen = dcc.Dropdown(
            id="dropdown-int",
            options=opcI,
            placeholder='Seleccione un sitio de interés',
            value='todo'
            )

    destino = dcc.Dropdown(
            id="dropdown-ori",
            options=[
                {"label": 'Ubicación actual', "value": 'ubi'}
            ],
            placeholder='Seleccione un punto de origen',
            value='ubi'
            )

    layout = html.Div([
                        dbc.Row([dbc.Col(html.Div([html.H6('Sitio de interés'),origen],
                                         style={'padding': '1px 1px 15px 1px', 'text-align': 'center',
                                                'background': None, 'margin': '2px 2px 2px 2px',
                                                'position': 'relative', 'zIndex': 999}),sm=3),

                                dbc.Col(html.Div([html.A(dbc.Button('Ver en mapa!', id='ver-id', color='secondary', className='mr-1',
                                        size='md', style={'width': '130px','height': '40px','backgroundColor': '#31C4A5','border-color': '#2BD3BE'}, n_clicks=0))],
                                        style={'padding': '23px 1px 15px 1px', 'text-align': 'center',
                                               'margin': '2px 2px 2px 2px'}), sm=3),

                                dbc.Col(html.Div([html.H6('Ruta desde:'),destino],
                                        style={'padding': '1px 1px 15px 1px', 'text-align': 'center',
                                               'background': None, 'margin': '2px 2px 2px 2px'}),sm=3), 

                                dbc.Col(html.Div([html.A(dbc.Button('Calcular!', id='calcula-id', color='secondary', className='mr-1',
                                size='md', style={'width': '130px','height': '40px','backgroundColor': '#31C4A5','border-color': '#2BD3BE'}, n_clicks=0))],
                                style={'padding': '23px 1px 15px 1px', 'text-align': 'center',
                                       'margin': '2px 2px 2px 2px'}), sm=3)

                                ], no_gutters=True, justify='center'),

                        dbc.Row([dbc.Col([html.Div([mapa], id="graph-map-id",
                                                  style={'padding': '3px 3px 3px 3px', 'text-align': 'center','background': None, 
                                                         'margin': '2px 2px 2px 2px','border':'1px gray solid',
                                                         'border-radius' : '7px'})],sm=10),

                                dbc.Col([html.Div([html.H4('Detalles:'),html.H6('Los sitios de interes corresponden a lugares donde se pueden realizar actividades academicas y culturales de indole extracurricular blablablabla blabalbalb alabklalbalba lbalablaba blablaba lbalbal')]
                                    ,id="Info-id",style={'padding': '3px 5px 3px 3px', 'text-align': 'left','background': None, 
                                                          'margin': '2px 10px 2px 10px','border':'1px gray solid', 'height': '568px',
                                                          'border-radius' : '7px'})],sm=2)

                                ], no_gutters=True, justify='center'),
                        html.Div(html.Span('',id='coords-id',style={'font-size':'8pt','color': '#989898'}),
                            style={'padding': '0px 10px 3px 3px','text-align': 'left','background': None})])

    return layout

@server.app_dash.callback(Output("coords-id", "children"), 
                          Input("map-id", "location_lat_lon_acc"),)
def update_location(location):
    if location:
        ubi = location[0], location[1]
        session['ubi'] = ubi
        
        return f'lat: {ubi[0]}, lon: {ubi[1]}'

    else:
     pass


@server.app_dash.callback(Output("points-id","children"),
                          Output("Info-id","children"),
                          Input("ver-id","n_clicks"),
                          State("dropdown-int","value"), 
                          prevent_initial_call=True
                          )
def view_point(btn, point):
    icon = {
            "iconUrl": '/static/assets/target.png',
            "iconSize": [38, 38],  # size of the icon
            #"popupAnchor": [-3, -76]  # point from which the popup should open relative to the iconAnchor
           }
    
    child = [html.H4('Detalles:'),html.H6('Los sitios de interes corresponden a lugares donde se pueden realizar actividades academicas y culturales de indole extracurricular blablablabla blabalbalb alabklalbalba lbalablaba blablaba lbalbal')]

    ls = []
    if point != 'todo':
        datF = df[df.sitio==point].copy()
        child = [html.H4('Detalles:')]
        child += [html.H6(f'{i}: {datF[i].iloc[0]}') for i in datF.iloc[:,1:-3].columns]
        child += [html.A(html.H6('Mayor información', style={'color': '#1C71F4'}),
                           href=datF['link'].iloc[0], target="_blank")]
    else:
        datF = df.copy()

    for row in datF.itertuples():
        ls.append(dict(name=row.sitio, lat=row.lat, lon=row.lon))

    markers =[dl.Marker(position=[c['lat'], c['lon']], icon=icon, children=dl.Popup(c['name']) ) for c in ls]

    del datF, ls

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'ver-id' in changed_id:
        return markers, child 
    else:
        return None,None


@server.app_dash.callback(Output("routes-id", "children"), 
                          Input("calcula-id", "n_clicks"),
                          State("dropdown-int", "value"),
                          State("dropdown-ori", "value"))
def get_route(btn, destino, origen):

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    if ('calcula-id' in changed_id) and destino!='todo':
        datF = df[df.sitio==destino].copy()
        lat = datF.lat.iloc[0]
        lon = datF.lon.iloc[0]

        poly = get_hibryd_route(session['ubi'],[lat,lon])

        #iconUrl = "/static/assets/paws.png"
        #marker = dict(rotate=True, markerOptions=dict(icon=dict(iconUrl=iconUrl, iconSize=[50,50])))

        patterns = [dict(repeat=20,dash=dict(pixelSize=10, pathOptions=dict(color='#29D18F', weight=3, opacity=0.9))),
                    dict(offset='5%', repeat='5%', )] #
        rotated_markers = dl.PolylineDecorator(positions=poly, patterns=patterns)

        return rotated_markers

    else:
     pass
