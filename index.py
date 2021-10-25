from flask import Flask, render_template
from server import app, app_dash
import dash_html_components as html
import dash_core_components as dcc
import dash_apps
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

@app.route('/')
def index():
    return render_template('profile.html')

@app.route('/profile.html')
def home():
    return render_template('profile.html')

@app.route('/index.html')
def transporte():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/table.html')
def table():
    return render_template('table.html')


app_dash.layout = html.Div(children=[html.Div([dcc.Location(id='url', refresh=True),
                                          html.Div(id='page-content')])])

@app_dash.callback(Output('page-content', 'children'),
                   [Input('url', 'pathname')])
def display_page(pathname):
    children_pages = dash_apps.children_pages
    root = '/'.join(pathname.split('/')[:3]) + '/'
    print(pathname)
    if root not in children_pages:
        raise PreventUpdate('Do nothing')
    else:
        layout = children_pages[root].create_layout()
        return layout

if __name__ == "__main__":
    app.run(port=8080, use_reloader=True, threaded=True)