from dash import html, Output, Input, State, MATCH
import dash_bootstrap_components as dbc


from pages.home import home_page
from pages.time import time_page, register_callbacks_time
from pages.image import image_page, register_callbacks_image
from pages.currency import currency_page


def register_callbacks(app):
    @app.callback(Output("page-content", "children"),
                  [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/":
            return home_page()
        elif pathname == "/time-diff":
            return time_page()
        elif pathname == "/currency-ex":
            return currency_page()
        elif pathname == "/image-process":
            return image_page()
        # If the user tries to reach a different page, return a 404 message
        return html.Div(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ],
            className="p-3 bg-light rounded-3",
        )

    register_callbacks_time(app)
    register_callbacks_image(app)
