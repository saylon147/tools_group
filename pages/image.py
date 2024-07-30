import os

from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc


# LAYOUT ############################################
def image_page():
    return html.Div([
        html.H4("Image Process"),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                '拖动文件到这里，或者 ',
                html.A('点击上传')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=True
        ),
        html.P(id='output-data-upload')
    ])


# CALLBACK ##########################################
def register_callbacks_image(app):
    @app.callback(
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
    )
    def update_output(contents, filename):
        if contents is not None:
            file_path = os.path.join(os.getcwd(), filename[0])
            return f"文件: {file_path}"
        return "未选择文件"
