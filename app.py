# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

bilan_2018 = pd.read_csv('data_output/bilan_2018.csv', dtype=str, na_filter=False)

df_communes = bilan_2018[bilan_2018['commune'] != ''].sort_values(by='commune')
labels = df_communes['commune'].unique()
values = df_communes['code_commune'].unique()
communes = [dict(zip(('label', 'value'), (label, value))) for label, value in zip(labels, labels)]

app.layout = html.Div(children=[
    html.H1(children='Le jeu des 1000 euros'),

    html.Div(children='''
        Comment votre commune répartit-elle 1000 euros de dépenses? 
    '''),

    html.Label('Choisissez votre commune'),
    dcc.Dropdown(id='commune_dropdown', options=communes),

    html.Div(id='graphs')

])


@app.callback(
    Output(component_id='graphs', component_property='children'),
    [Input(component_id='commune_dropdown', component_property='value')]
)
def udpate_dep_par_fonction(commune):
    if not commune:
        return ''
    filtered_df = bilan_2018[bilan_2018['commune'] == commune].sort_values(by=['aggregat_fonction', 'aggregat_compte'])
    fig = px.pie(
        filtered_df,
        values='depense',
        names='aggregat_fonction',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    return [dcc.Graph(id='dep_par_fonction', figure=fig)]


if __name__ == '__main__':
    app.run_server(debug=True)