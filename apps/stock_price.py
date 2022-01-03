from dash import dcc, html
from app import app
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import date
from dash.dependencies import Input, Output
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

#PX_STOCKS
df1 = pd.read_csv(DATA_PATH.joinpath("stock_price.csv"))
df1['Date'] = pd.to_datetime(df1['Date'])
df_stock = df1.pivot(index=['Ticker', 'Date'],
                    columns='variable',
                    values='Value')
df_stock.fillna(method='ffill', inplace=True)

layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col([
                    html.Div([
                        html.H3('Stock Price', className='display-3')
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
                                    id='ticker_stock_price',
                                    options=[{'label': i, 'value':i} for i in df_stock.index.get_level_values(0).unique()],
                                    value='TLKM'
                                )], xs=10, sm=10, md=10, lg=4, xl=4
                            ),
                            dbc.Col([
                                html.Div([
                                    html.P('Date'),
                                    dcc.DatePickerRange(
                                        id='date_stock_price',
                                        start_date= date(2021, 1, 1),
                                        end_date= date(2021, 12, 31)
                                    )
                                ])
                                ], xs=10, sm=10, md=10, lg=4, xl=4,
                            ),
                        ], justify='center'),
                    ]),
                    dbc.Col([
                        html.Div(children=[
                            dcc.Graph(
                                id='stock_price_graph'
                            )
                        ], className= 'box')
                    ])
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
    Output(component_id='date_stock_price', component_property='start_date'),
    Output(component_id='date_stock_price', component_property='end_date'),
    Input(component_id='ticker_stock_price', component_property='value')
)

def update_date(dd_value):
    df = df_stock.copy(deep=True)
    if dd_value is None:
        dd_value = 'TLKM'
    df = df[((df.index.get_level_values(0) == dd_value))]
    start_date = df.index.get_level_values(1).min()
    end_date = df.index.get_level_values(1).max()
    return start_date, end_date

@app.callback(
    Output(component_id='stock_price_graph', component_property='figure'),
    Input(component_id='ticker_stock_price', component_property='value'),
    Input(component_id='date_stock_price', component_property='start_date'),
    Input(component_id='date_stock_price', component_property='end_date')
)

def update_chart(dd_value, start, end):
    df = df_stock.copy(deep=True)
    df = df[((df.index.get_level_values(0) == dd_value))]
    df = df[((df.index.get_level_values(1) >= pd.to_datetime(start)) & (df.index.get_level_values(1) <= pd.to_datetime(end)))]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=('Stock Price', 'Volume'),
               row_width=[0.2, 0.8])
    fig.add_trace(go.Candlestick(x=df.index.get_level_values(1), open=df["Open"], high=df["High"],
                low=df["Low"], close=df["Close"]),
                row=1, col=1)
    fig.add_trace(go.Bar(x=df.index.get_level_values(1), y=df['Volume'], showlegend=False), row=2, col=1)
    fig.update_layout(
        #title = 'Stock Price',
        yaxis_title = 'Stock Price IDR (Rp.)',
        xaxis_title = 'Date',
        xaxis_rangeslider_visible=False,
        showlegend = False,
        height=600,
        plot_bgcolor='#EDEFEB',
        paper_bgcolor='#EDEFEB'
    )
    return fig