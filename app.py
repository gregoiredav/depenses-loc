# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Le jeu des 1000 euros'),

    html.Div(children='''
        Comment votre commune répartit-elle 1000 euros de dépenses? 
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Saint Ouen'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Courbevoie'},
            ],
            'layout': {
                'title': 'Exemple d\'indicateur '
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)