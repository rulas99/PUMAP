from flask import Flask
import dash

app = Flask(__name__)

app_dash = dash.Dash(__name__, server=app,
            meta_tags=[{"name": "viewport", "content":
                        "width=device-width, initial-scale=1"}],
            url_base_pathname="/dash/")
    
app_dash.config.suppress_callback_exceptions = True
app_dash.title = 'Proyecto'






