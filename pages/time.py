from dash import html, dcc, Output, Input, MATCH, State
import dash_bootstrap_components as dbc
from datetime import datetime


# LAYOUT ############################################
def time_page():
    current_date = datetime.now().strftime("%Y - %m - %d")  # 获取当前日期

    input_groups = []
    history_date = ["2020-06-04", "2024-06-04", "2023-03-15"]
    default_date = "2024-01-01"
    for i in range(len(history_date)):
        input_groups.append(
            dbc.InputGroup(
                [
                    dbc.InputGroupText(f"Date {i+1}"),
                    dbc.Input(placeholder="Date", id={'type': 'date-input', 'index': i+1},
                              type="date", value=history_date[i]),
                    dbc.InputGroupText(id={'type': 'date-diff-output', 'index': i+1},
                                       style={"marginLeft": "10px"})  # 用于显示天数差异的文本
                ],
                className="mb-3",
            )
        )

    return html.Div([
        html.H4(f"Today : {current_date}"),  # 在页面上显示当前日期
        html.Hr(className="my-2"),
        dcc.Store(id='input-store', data={'default-date': default_date}),
        html.Div(id='input-container', children=input_groups),
        dbc.Button("New Date", id='add-button', n_clicks=0, className="mt-3"),
    ])


# CALLBACK ##########################################
def register_callbacks_time(app):
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
                    dbc.InputGroupText(id={'type': 'date-diff-output', 'index': new_index},
                                       style={"marginLeft": "10px"})
                ],
                className="mb-3",
            )
            existing_inputs.append(new_input_group)
        return existing_inputs


# OTHERS ############################################
def time_diff(input_date):
    try:
        if input_date:
            input_date = datetime.strptime(input_date, "%Y-%m-%d")
            input_date = input_date.replace(hour=0, minute=0, second=0, microsecond=0)
            current_date = datetime.now()
            if current_date < input_date:
                current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
            return (input_date - current_date).days
    except ValueError as e:
        print(f"ValueError: {e} -->{input_date}")
        return None
    return None
