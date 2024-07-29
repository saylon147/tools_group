from dash import html, Output, Input, State, MATCH
import dash_bootstrap_components as dbc

from pages.home import home_page
from pages.time import time_page, time_diff


def register_callbacks(app):
    @app.callback(Output("page-content", "children"),
                  [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/":
            return home_page()
        elif pathname == "/time-utilities":
            return time_page()
        elif pathname == "/page-2":
            return html.P("Oh cool, this is page 2!")
        # If the user tries to reach a different page, return a 404 message
        return html.Div(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ],
            className="p-3 bg-light rounded-3",
        )

    @app.callback(
        Output({'type': 'date-diff-output', 'index': MATCH}, 'children'),
        Input({'type': 'date-input', 'index': MATCH}, 'value'),
    )
    def update_date_difference(input_date):
        if input_date:
            if difference := time_diff(input_date):
                if difference > 0:
                    return f"{difference} 天之后"
                elif difference < 0:
                    return f"第 {-difference} 天"
                else:
                    return ""
        else:
            return "Select a Date"

    @app.callback(
        Output('input-container', 'children'),
        Input('add-button', 'n_clicks'),
        State('input-store', 'data'),
        State('input-container', 'children')
    )
    def add_date_input(n_clicks, stored_data, existing_inputs):
        if n_clicks > 0:
            new_index = len(existing_inputs) + 1
            new_input_group = dbc.InputGroup(
                [
                    dbc.InputGroupText(f"Date {new_index}"),
                    dbc.Input(placeholder="Date", id={'type': 'date-input', 'index': new_index}, type="date",
                              value=stored_data['default-date']),
                    dbc.InputGroupText(id={'type': 'date-diff-output', 'index': new_index}, style={"marginLeft": "10px"})
                ],
                className="mb-3",
            )
            existing_inputs.append(new_input_group)
        return existing_inputs
