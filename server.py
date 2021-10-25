from flask import Flask
import dash
import dash_bootstrap_components as dbc

app = Flask(__name__)

app_dash = dash.Dash(__name__, server=app,
            meta_tags=[{"name": "viewport", "content":
                        "width=device-width, initial-scale=1"}],
            url_base_pathname="/dash/",
            external_stylesheets=['https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
                                  dbc.themes.BOOTSTRAP],
            #prevent_initial_callbacks=True
            )
    
app_dash.config.suppress_callback_exceptions = True
app_dash.title = 'Proyecto'






