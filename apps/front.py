import dash_bootstrap_components as dbc
from dash import dcc, html
from app import app
import pathlib
import pandas as pd
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../datasets').resolve()

df1 = pd.read_csv(DATA_PATH.joinpath('stock_price.csv'))
df1['Date'] = pd.to_datetime(df1['Date'])
df_stock = df1.pivot(index=['Ticker', 'Date'],
                    columns='variable',
                    values='Value')
df_stock.fillna(method='ffill', inplace=True)
df_2d = df_stock.groupby(['Ticker'],as_index=False).tail(2)
df_2d['Growth Price'] = df_2d.groupby(['Ticker'])['Close'].diff()
df2 = df_2d.groupby(['Ticker'],as_index=False).nth(-1)
df2.reset_index(inplace=True)
df2 = df2.sort_values(by='Close', ascending=False)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([
                    html.Div([
                        html.H3('Stocks Dashboard', className='display-3')
                    ])
                ], xs=10, sm=10, lg=10, xl=10),
                dbc.Col([html.Hr()], width={'size':10}),
                html.Br(),
            ], justify='center'
        ), 
        dbc.Row(
            [
                dbc.Col(
                    [
                    dbc.Col(
                        html.Div(
                            html.H5('Last Stocks Price', className='display-6')
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            dash_table.DataTable(
                                id='datatable-interactivity4',
                                    columns=[
                                            {"name": 'Ticker', "id": 'Ticker', "hideable": False},
                                            {"name": 'Close', "id": 'Close', "hideable": False, 'type':'numeric', 'format': {'specifier': ',.0f', 'locale':{'group': ','}}},
                                            {'name': 'Growth Price', 'id':'Growth Price', 'type':'numeric'}
                                        ],
                                        data = df2.to_dict('records'),
                                        filter_action= 'native',
                                        sort_action='native',
                                        sort_mode='single',
                                        selected_columns=[],
                                        selected_rows=[],
                                        page_action="native",
                                        page_current= 0,
                                        page_size= 10,
                                        style_as_list_view=True,
                                        style_cell= {'textAlign':'right'},
                                        style_table={
                                            'overflowY': 'scroll'
                                        },
                                        style_data={
                                            'whiteSpace': 'normal',
                                            'height' : 'auto',
                                            'fontSize' : '16px',
                                            'font-family' : 'sans-serif',
                                            'padding': '5px',
                                            'backgroundColor': 'transparent'
                                        },
                                        style_header={
                                            'color': 'light-gray',
                                            'fontWeight': 'bold',
                                            'fontSize' : '14px',
                                            'whiteSpace': 'normal',
                                            'height' : 'auto',
                                            'font-family' : 'sans-serif'
                                        },
                                        style_data_conditional= ([
                                            #Growth Price
                                            {
                                                'if': {
                                                    'filter_query': '{Growth Price} > 0',
                                                    'column_id' : 'Growth Price'
                                                },
                                                'color': 'green'
                                            },
                                            {
                                                'if': {
                                                    'filter_query': '{Growth Price} < 0',
                                                    'column_id': 'Growth Price'
                                                },
                                                'color': 'red'
                                            },
                                        ])
                                    ),
                        )
                    )
                ],className= 'box', xs=10, sm=10, md=10, lg=10, xl=10,),
            ], justify='center'
        ),
        dbc.Row([
                dbc.Col(
                    [
                        dbc.Col(
                            html.Div(
                                html.H5('Stock Price', className='display-6')
                            )
                        ),
                        dbc.Col(
                            dbc.Row([
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='dd_ticker_front',
                                        options=[{'label':i, 'value':i} for i in df_stock.index.get_level_values('Ticker').unique()],
                                        value='ADRO',
                                        className='dbc'
                                    ), xs=10, sm=10, md=8, lg=8, xl=8),
                                dbc.Col(
                                    html.Div(
                                        [
                                            dbc.RadioItems(
                                                id="dd_long",
                                                className="btn-group",
                                                inputClassName="btn-check",
                                                labelClassName="btn btn-outline-primary",
                                                labelCheckedClassName="active",
                                                options=[
                                                    {"label": "1W", "value": 1},
                                                    {"label": "1M", "value": 2},
                                                    {"label": "1Y", "value": 3},
                                                ],
                                                value=1,
                                            ),
                                        ],
                                        className="radio-group",
                                    ), xs=10, sm=10, md=3, lg=3, xl=3),
                            ], justify='center')
                        ),
                        dbc.Col(
                            html.Div(
                                dcc.Graph(
                                    id='line_chart_price'
                                )
                            )
                        )
                    ], className= 'box', xs=10, sm=10, md=10, lg=10, xl=10,
                )
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
    Output(component_id='line_chart_price', component_property='figure'),
    Input(component_id='dd_ticker_front', component_property='value'),
    Input(component_id='dd_long', component_property='value')
)

def update_chart(ticker, long):
    df = df_stock.copy(deep=True)
    df.reset_index(inplace=True)
    if long == 1:
        df2 = df.set_index('Date').last('1W')
        start_date = df2.index.get_level_values('Date').min()
        end_date = df2.index.get_level_values('Date').max()
    elif long == 2:
        df2 = df.set_index('Date').last('1M')
        start_date = df2.index.get_level_values('Date').min()
        end_date = df2.index.get_level_values('Date').max()
    elif long == 3:
        df2 = df.set_index('Date').last('1Y')
        start_date = df2.index.get_level_values('Date').min()
        end_date = df2.index.get_level_values('Date').max()
    df = df[((df.Ticker == ticker) & (df.Date >= pd.to_datetime(start_date)) & (df.Date <= pd.to_datetime(end_date)))]
    fig = px.line(df, x='Date', y='Close')
    fig.update_layout(
        #title = 'Valuation Index Chart',
        yaxis_title = 'Close',
        xaxis_title = 'Date',
        #yaxis=dict(range=[lower,upper]),
        plot_bgcolor='#EDEFEB',
        paper_bgcolor='#EDEFEB'
    )
    return fig