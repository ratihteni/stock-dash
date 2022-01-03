import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from numpy import fromregex
# Connect to main app.py file
from app import app


from app import server

from apps import stock_price, stock_relative, front


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "4rem 1rem 2rem",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
SIDEBAR_STYLE = {
    "overflow": "scroll",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "padding": "4rem 2rem",
    "background-color": "#404040",
    "color": "white",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "padding-top": "3rem",
}

app.layout = html.Div([
    dcc.Location(id="url"),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.Div(
                    [
                        html.H2(html.A(href='/', children='Stocks Dashboard', style={'text-decoration': 'none', 'color': 'white'}), className="display-4"),
                        html.P(
                            "A simple stocks dashboard by Ratih Teni K.", className="lead", style={'text-align':'center'}
                        ),
                        html.Hr(),
                        dbc.Nav(
                            [
                                dbc.NavLink([html.I(className="fa fa-bar-chart-o mr-2", style={'margin-right': '10px'}), "Stock Price"], href="/stock-price", active="exact"),
                                dbc.NavLink([html.I(className="fa fa-line-chart mr-2", style={'margin-right': '10px'}), "Stock Relative"], href="/stock-relative", active="exact"),
                            ],
                            vertical=True,
                            pills=True,
                        ),
                    ],
                    id="sidebar",
                )
            ], justify='center', style=SIDEBAR_STYLE, className='full')
        ], xs=12, sm=12, md=5, lg=5, xl=3),
        dbc.Col([
            html.Div(id="page-content", style=CONTENT_STYLE)
        ], xs=12, sm=12, md=7, lg=7, xl=9)
    ])
])



@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return front.layout
    elif pathname == "/stock-price":
        return stock_price.layout
    elif pathname == "/stock-relative":
        return stock_relative.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(port=8888)