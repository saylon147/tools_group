import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input

from callbacks import register_callbacks

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True  # 忽略回调异常

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        # html.H2("TOOL LIST", className="display-4"),
        # html.Hr(),
        # html.P(
        #     "description", className="lead"
        # ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Time Difference", href="/time-diff", active="exact"),
                dbc.NavLink("Currency Exchange", href="/currency-ex", active="exact"),
                dbc.NavLink("Image Process", href="/image-process", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# 注册回调函数
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
