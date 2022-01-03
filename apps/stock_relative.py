from dash import dcc, html
from pandas.core.base import DataError
from app import app
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import date
from dash.dependencies import Input, Output
import pandas as pd
import pathlib
import numpy as np
import dash_bootstrap_components as dbc

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

def func(row):
    row['Value'] = row['Value'] / row['Value'].iloc[0] * 100
    return row

#px_stocks
df_stock = pd.read_csv(DATA_PATH.joinpath('stock_relative.csv'))
df_stock['Date'] = pd.to_datetime(df_stock['Date'])

layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col([
                    html.Div([
                        html.H3('Stock Relative', className='display-3')
                    ])
                ], xs=10, sm=10, lg=10, xl=10),
                dbc.Col([html.Hr()], width={'size':10}),
                html.Br(),
            ], justify='center'
        ), 
        dbc.Row(
            [
                dbc.Col([
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                html.P('Ticker'),
                                dcc.Dropdown(
                                    id='ticker_stock_relative',
                                    options=[{'label':i, 'value':i} for i in df_stock.Ticker.unique()],
                                    value = ['TLKM', 'WIKA'],
                                    multi=True
                                )
                            ], xs=10, sm=10, md=10, lg=5, xl=5),
                            dbc.Col([
                                html.P('Date'),
                                dcc.DatePickerRange(
                                    id='date_stock_relative',
                                    start_date = date(2021, 1, 1),
                                    end_date = date(2021, 12, 31)
                                )
                            ], xs=10, sm=10, md=10, lg=4, xl=4)
                        ], justify='center'),
                    ]),
                    html.Div(children=[
                        dcc.Graph(
                            id='stock_relative_graph'
                    )], className='box')
                ], xs=10, sm=10, md=10, lg=10, xl=10)
            ], justify='center'
        ),
        dbc.Row(
            [
                dbc.Col([
                    html.Div([
                        html.P('Created by Ratih Teni K.', style={'text-align':'center'})
                    ])],  xs=10, sm=10, md=10, lg=10, xl=10,
                )
            ], justify='center'
        )
    ]
)

@app.callback(
    Output(component_id='date_stock_relative', component_property='start_date'),
    Output(component_id='date_stock_relative', component_property='end_date'),
    Input(component_id='ticker_stock_relative', component_property='value'),
)

def update_date(ticker_stock_relative):
    df = df_stock.copy(deep=True)
    if ticker_stock_relative is None:
        ticker_stock_relative = ['TLKM', 'WIKA']
    df = df[((df['Ticker'].isin(ticker_stock_relative)) & (df['variable']=='Close'))]
    start_date = df.Date.min()
    end_date = df.Date.max()
    return start_date, end_date

@app.callback(
    Output(component_id='stock_relative_graph', component_property='figure'),
    Input(component_id='ticker_stock_relative', component_property='value'),
    Input(component_id='date_stock_relative', component_property='start_date'),
    Input(component_id='date_stock_relative', component_property='end_date'),
)

def update_chart(ticker, start, end):
    df = df_stock.copy(deep=True)
    df = df[((df['Ticker'].isin(ticker)))]
    df = df[((df['Ticker'].isin(ticker)) & (df['variable'] == 'Close') & (df['Date'] >= pd.to_datetime(start)) & (df['Date'] <= pd.to_datetime(end)))].sort_values('Date')
    df = df.groupby(['Ticker'], as_index=False).apply(func).fillna(method='ffill')
    q1 = np.percentile(df['Value'], 25, interpolation = 'midpoint')
    q3 = np.percentile(df['Value'], 75, interpolation = 'midpoint')
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr
    fig = px.line(df, x='Date', y='Value', color='Ticker')
    fig.update_layout(
        title = 'Stock Relative',
        title_x=0.5,
        yaxis_title = 'Value',
        xaxis_title = 'Date',
        #yaxis=dict(range=[lower,upper]),
        plot_bgcolor='#EDEFEB',
        paper_bgcolor='#EDEFEB'
    )
    return fig