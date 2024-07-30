import os
from PIL import Image

from dash import html, dcc, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify


INPUT_FOLDER = "\\input_data"


# LAYOUT ############################################
def image_page():
    return html.Div([
        dmc.Title(f"GIF 帧输出", order=1),
        html.Br(),
        dcc.Upload(
            id='input-file',
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
        dmc.TextInput(label="输入文件", id='input-file-path', style={'width': '100%'}, required=True, disabled=True),
        html.Br(),
        dmc.Flex([
            dmc.TextInput(label='输出目录', id='output-folder', required=True, style={'width': '90%'}),
            dmc.Button('导出', id='output-button',
                       leftSection=DashIconify(icon="fa6-solid:file-export"),
                       color='lime',
                       style={'width': '10%'})
        ],
            align={"base": "flex-end"},
            direction={"base": "row"},
            gap={"base": "lg"},
            justify={"base": "flex-start"},
        ),

        html.Br(),
        html.Br(),
        dmc.Title(f"合并GIF", order=1),
        html.Br(),
        dmc.TextInput(label='输入目录', id='input-pics-folder', required=True, style={'width': '100%'}),
        html.Br(),
        dmc.NumberInput(label='帧间隔时间(毫秒)', id='frame-time-gap', value=100, w=200,
                        min=100, max=1000, step=50),
        html.Br(),
        dmc.Flex([
            dmc.TextInput(label='输出到', id='output-gif-path', required=True, style={'width': '90%'}),
            dmc.Button('合并', id='output-gif-button',
                       leftSection=DashIconify(icon="ic:baseline-hive"),
                       color='violet',
                       style={'width': '10%'})
        ],
            align={"base": "flex-end"},
            direction={"base": "row"},
            gap={"base": "lg"},
            justify={"base": "flex-start"},
        ),
    ])


# CALLBACK ##########################################
def register_callbacks_image(app):
    @app.callback(
        Output('input-file-path', 'value'),
        Input('input-file', 'contents'),
        State('input-file', 'filename')
    )
    def update_output(contents, filename):
        if contents is not None:
            file_path = os.path.join(os.getcwd() + INPUT_FOLDER, filename[0])
            return f"{file_path}"
        return "未选择文件"

    @app.callback(
        Input('output-button', 'n_clicks'),
        State('input-file-path', 'value'),
        State('output-folder', 'value'),
        prevent_init_call=True
    )
    def do_export(n_clicks, input_file_path, output_folder):
        if n_clicks:
            if input_file_path != "" and output_folder != "":
                extract_gif_frames(input_file_path, output_folder)
            else:
                print("Alert")

    @app.callback(
        Input('output-gif-button', 'n_clicks'),
        State('input-pics-folder', 'value'),
        State('output-gif-path', 'value'),
        State('frame-time-gap', 'value'),
        prevent_init_call=True
    )
    def do_merge(n_clicks, input_folder, output_file_path, time_gap):
        if n_clicks:
            if input_folder != "" and output_file_path != "":
                create_gif_from_frames(input_folder, output_file_path, time_gap)
            else:
                print("Alert")


# OTHERS ############################################
def extract_gif_frames(gif_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(gif_path))[0]

    with Image.open(gif_path) as gif:
        frame_count = gif.n_frames
        for frm in range(frame_count):
            gif.seek(frm)
            frame_image = gif.copy()
            frame_image.save(os.path.join(output_folder, f'{base_name}_F_{frm+1:03d}.png'))

    print(f"Successfully extracted {frame_count} frames to '{output_folder}'.")


def create_gif_from_frames(frames_folder, output_gif_path, duration=100):
    # 获取所有帧文件的路径，并排序
    frames = [os.path.join(frames_folder, f) for f in sorted(os.listdir(frames_folder)) if f.endswith('.png')]

    # 打开所有帧图像
    images = [Image.open(frame) for frame in frames]

    # 将第一帧图像保存为GIF，并附加剩余帧图像
    if images:
        images[0].save(output_gif_path, save_all=True, append_images=images[1:], duration=duration, loop=0)
        print(f"Successfully created GIF '{output_gif_path}' with {len(images)} frames.")
    else:
        print("No PNG frames found in the specified folder.")
