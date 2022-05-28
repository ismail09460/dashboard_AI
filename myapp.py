from msilib.schema import tables
import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from ast import literal_eval
import numpy as np



app = dash.Dash()

data = pd.read_csv("statistics_data.csv")

#company function
def search(company):
    dct = {}
    dct['Main_ORG'] = company
    texts = []
    orgs = []
    regex = ".*"+company+".*"
    df_company = data[data.MAIN_ORG.str.match(regex)].reset_index(drop=True)
    #number of posts by company
    posts_number = df_company.shape[0]
    #get texts
    texts = df_company['text'].values.tolist()
    dct['texts'] = texts
    #orgs
    for i in range(len(df_company)):
        if df_company['ORGS'][i] != 'no organisation':
            orgs.extend(literal_eval(df_company['ORGS'][i]))
    dct['orgs'] = orgs
    #group by month
    df_company = df_company.groupby('month')
    #get group for avril
    df_avril = df_company.get_group('avril')
    #get group for mai
    df_mai = df_company.get_group('mai')
    
    #positive and negative rate
    #statistics for avril
    dct['avril'] = {}
    positive_rate_avril = np.round((len(df_avril.loc[df_avril['score'] == 1]) / len(df_avril['score']))*100 , 2)
    negative_rate_avril = np.round((len(df_avril.loc[df_avril['score'] == 0]) / len(df_avril['score']))*100 , 2)
    dct['avril']['positive_rate'] = positive_rate_avril
    dct['avril']['negative_rate'] = negative_rate_avril
    #number of posts by company by month
    dct['avril']['number_of_posts'] = df_avril.shape[0]
    
    #statistics for mai
    dct['mai'] = {}
    positive_rate_mai = np.round((len(df_mai.loc[df_mai['score'] == 1]) / len(df_mai['score']))*100 , 2)
    negative_rate_mai = np.round((len(df_mai.loc[df_mai['score'] == 0]) / len(df_mai['score']))*100 , 2)
    dct['mai']['positive_rate'] = positive_rate_mai
    dct['mai']['negative_rate'] = negative_rate_mai
    #number of posts by company by month
    dct['mai']['number_of_posts'] = df_mai.shape[0]
    
    return dct

#variables
Main_ORG = search('OCP')['Main_ORG']
avril = search('OCP')['avril']
mai = search('OCP')['mai']
orgs = search('OCP')['orgs']

app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = f'{Main_ORG}', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),

        dcc.Dropdown( id = 'dropdown',
        options = [
            {'label':'OCP', 'value':'OCP' },
            {'label': 'ORANGE', 'value':'ORANGE'},
            {'label': 'CMA CGM', 'value':'CMA CGM'},
            ],
        value = '--select company--'),
        dcc.Graph(id = 'bar_plot')

    ])

    
@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])
def graph_update(dropdown_value):
    print(dropdown_value)
    fig = go.Figure([go.Scatter(x = data['month'], y = avril['number_of_posts'],\
                     line = dict(color = 'firebrick', width = 4))
                     ])
    
    fig.update_layout(title = 'Number Of Post In Each Month',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Number OF Post'
                      )
    return fig
fig = px.bar(data, x="month", y="MAIN_ORG", color="sentiments", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__': 
    app.run_server()