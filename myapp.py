# import libraries
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
import dash_bootstrap_components as dbc
from search_fct import search
from dash import html

# read data
data = pd.read_csv("statistics_data.csv")

# initialize dash
app = dash.Dash()

#initialize dash-bootstrap components
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])



# list of companies
list_companies = []
with open('companies.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        list_companies.append(line)

# test search
# print(search('OCP'))

#variables (example of OCP)
Main_ORG = search('OCP')['Main_ORG']
avril = search('OCP')['avril']
mai = search('OCP')['mai']
orgs = search('OCP')['orgs']



#component
app.layout = html.Div(children=[
    dbc.Row(
        html.Div([
            html.H1(id = 'H1', children = "Companies E-Reputation", style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40 , 'fontFamily':'Arial','fontWeight':'bold'}),

        dcc.Dropdown( id = 'dropdown',
        options = list_companies,
        value = '--select company--')
        ]
        )
    )
,
# add blank space between search bar and 2nd row to ensure visibility
html.Div(
  style={
      "height":10  
  }
),
#grid layout (2 columns)
dbc.Row(
    [
        #first column contains informations and staistics
        dbc.Col([
            #this row contains 3 cards describing (company name ,posts number & impressions)
            dbc.Row(
                [
                    dbc.Col(  dbc.Card(
            dbc.CardBody(
                [
                    html.H5("COMPANY NAME", className="card-title"),
                    html.P(
                        "This card has some text content.",
                        className="card-text",
                    ),
                ]
            )
        )),
                    dbc.Col(
                          dbc.Card(
            dbc.CardBody(
                [
                    html.H5("NUMBER OF POSTS", className="card-title"),
                    html.P(
                        "This card has some text content.",
                        className="card-text",
                    ),
                ]
            )
        )
                    ),
                    dbc.Col(  dbc.Card(
            dbc.CardBody(
                [
                    html.H5("IMPRESSIONS", className="card-title"),
                    html.P(
                        "This card has some text content.",
                        className="card-text",
                    ),
                ]
            )
        ))
                ]
            ),
            dbc.Row()
        ]),
        #second column(consists of 2 rows) contains 2 plots 
        dbc.Col([
            #first row contains a line chart (number of posts per month)
            dbc.Row(
               html.Div([
            dcc.Graph(id = 'bar_plot')]
        )
            ),
             #second row contains a bubble chart (number of posts per month)
            dbc.Row(
                html.Div(["bubble chart"])
            )
            ]
        )
    ],
    className="g-0",
)
    ])



    
@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])
def graph_update(dropdown_value):
    fig = go.Figure([go.Scatter(x = data['month'], y = avril['number_of_posts'],\
                     line = dict(color = 'firebrick', width = 4))
                     ])
    
    fig.update_layout(title = 'Number Of Post In Each Month',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Number OF Post'
                      )
    return fig
    
# fig = px.bar(data, x="month", y="MAIN_ORG", color="sentiments", barmode="group")

# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),

#     html.Div(children='''
#         Dash: A web application framework for your data.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])

if __name__ == '__main__': 
    app.run_server()