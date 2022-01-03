import dash
import dash_bootstrap_components as dbc

# meta_tags are required for the app layout to be mobile responsive
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
fa_css = ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI, dbc_css, fa_css], suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'}]
                )
server = app.server