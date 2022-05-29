# # # # # # # # # # # # # # # # # # # # # === Import Libraries === # # # # # # # # # # # # # # # # # # # # # 

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

# # # # # # # # # # # # # # # # # # # # # === Read Data AS CSV === # # # # # # # # # # # # # # # # # # # # # 

data = pd.read_csv("statistics_data.csv")

# # # # # # # # # # # # # # # # # # # # # === Initialize Dash === # # # # # # # # # # # # # # # # # # # # # 

app = dash.Dash()

# # # # # # # # # # # # # # # # # # # # # === Initialize Dash Bootstrap Components === # # # # # # # # # # # # # # # # # # # # # 

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# # # # # # # # # # # # # # # # # # # # # === List OF Companies === # # # # # # # # # # # # # # # # # # # # # 

list_companies = []
with open('companies.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        list_companies.append(line)

# # # # # # # # # # # # # # # # # # # # # === Variable OF Each Company === # # # # # # # # # # # # # # # # # # # # # 

Main_ORG = search('OCP')['Main_ORG']
avril = search('OCP')['avril']
mai = search('OCP')['mai']
orgs = search('OCP')['orgs']
texts = search('OCP')['texts']

# # # # # # # # # # # # # # # # # # # # # === TABLE OF POST FOR EACH COMPANY === # # # # # # # # # # # # # # # # # # # # # 

    # List of impresions
impressions = []
for text in list(dict.fromkeys(texts)):
    impressions.append(data[data['text']==text]['sentiments'].tolist()[0])
    
    # Table of posts
df = pd.DataFrame(
    {
        "id": np.arange(1, len(list(dict.fromkeys(texts)))+1),
        "post": list(dict.fromkeys(texts)),
        "impression": impressions
    }
)

table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

# # # # # # # # # # # # # # # # # # # # # === Components === # # # # # # # # # # # # # # # # # # # # # 

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
    ),
    # add blank space between search bar and 2nd row to ensure visibility
    html.Div(
    style={
        "height":10  
    }),
    #grid layout (2 columns)
    dbc.Row(
    [
        #first column contains informations and staistics
        dbc.Col([
            #this row contains 3 cards describing (company name ,posts number & impressions)
            dbc.Row(
                [
                    dbc.Col(dbc.Card(
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
                    dbc.Col(dbc.Card(
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
                    dbc.Col(dbc.Card(
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
            # add blank space between search bar and 2nd row to ensure visibility
            html.Div(
            style={
                "height":10  
            }),
            # table of posts
            dbc.Row(
               html.Div([table])
            )
        ]),
        #second column(consists of 2 rows) contains 2 plots 
        dbc.Col([
            #first row contains a line chart (number of posts per month)
            dbc.Row(
               html.Div([dcc.Graph(id = 'bar_plot')])
            ),
             #second row contains a bubble chart (number of posts per month)
            dbc.Row(html.Div(["bubble chart"]))
            ]
        )
    ],
    className="g-0",
    )
])


# # # # # # # # # # # # # # # # # # # # # === CAll BACK === # # # # # # # # # # # # # # # # # # # # # 

# @app.callback(Output(component_id='bar_plot', component_property= 'figure'),
#               [Input(component_id='dropdown', component_property= 'value')])
# def graph_update(dropdown_value):
#     fig = go.Figure([go.Scatter(x = data['month'], y = avril['number_of_posts'],\
#                      line = dict(color = 'firebrick', width = 4))
#                      ])
    
#     fig.update_layout(title = 'Number Of Post In Each Month',
#                       xaxis_title = 'Dates',
#                       yaxis_title = 'Number OF Post'
#                       )
#     return fig
    

# # # # # # # # # # # # # # # # # # # # # === MAIN === # # # # # # # # # # # # # # # # # # # # # 

if __name__ == '__main__': 
    app.run_server()