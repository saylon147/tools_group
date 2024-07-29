from dash import html
import dash_bootstrap_components as dbc


def home_page():
    return dbc.Row([
        dbc.Col(
            html.Div(
                [
                    html.H2("Change the background", className="display-3"),
                    html.Hr(className="my-2"),
                    html.P(
                        "Swap the background-color utility and add a `.text-*` color "
                        "utility to mix up the look."
                    ),
                    dbc.Button("Example Button", color="light", outline=True),
                ],
                className="h-100 p-5 text-white bg-primary rounded-3",
            ),
            md=6,
        ),
    ])
