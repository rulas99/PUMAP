from flask import Flask, render_template
from server import app, app_dash
import dash_html_components as html
import dash_core_components as dcc
import dash_apps
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/PUMAPS_Comida.html')
def comida():
    return render_template('PUMAPS_Comida.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/PUMAPS_Deportes.html')
def deportes():
    return render_template('PUMAPS_Deportes.html')

@app.route('/PUMAPS_FI.html')
def fi():
    return render_template('PUMAPS_FI.html')

@app.route('/PUMAPS_Salud.html')
def salud():
    return render_template('PUMAPS_Salud.html')

@app.route('/PUMAPS_Transporte.html')
def transporte():
    return render_template('PUMAPS_Transporte.html')

@app.route('/PUMAPS_Turisticos.html')
def turisticos():
    return render_template('PUMAPS_Turisticos.html')


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
    app.secret_key = 'i61yFyvwheKB5v7XHn9zzOZurmDwPNJ_NS07YXpJH66Lk7fS8XNpRChBg_EuDN7R1_vmOvhXstpE5V23txGzjg'
    app.run(port=3333, use_reloader=True, threaded=True)