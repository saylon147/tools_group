import json
import uuid
import re

from dash import html, Output, Input, State, ALL, no_update, callback_context, clientside_callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def start_download(url, path, rename):
    print(url, path, rename)


def add_download_entry(entry_id, rename):
    return dmc.Group([
        dmc.TextInput("", placeholder="url", style={"flex": "1"}, id={"type": "url-input", "index": entry_id}),
        dmc.TextInput(rename, placeholder="rename", w=200, id={"type": "name-input", "index": entry_id}),
        dmc.Button("Start", id={"type": "start-button", "index": entry_id}),
    ],
    )


def generate_new_name(rename):
    match = re.search(r'(\d+)$', rename)
    if match:
        # 提取数字部分并加1
        number = match.group(0)
        # 数字加1，并用zfill来补充前导0，保持与原数字相同的长度
        new_number = str(int(number) + 1).zfill(len(number))
        # 更新rename的数字部分
        rename = rename[:match.start()] + new_number
    return rename


def download_page():
    return html.Div([
        dmc.Stack([
            dmc.Button("New Task", variant="filled", leftSection=DashIconify(icon="mingcute:download-line",
                                                                             width=20), id="new-download-btn", w=150),
            dmc.TextInput("", label="Download Path", id="download-path", required=True),
            dmc.TextInput("", label="Default Rename", id="rename-input", w=200),
            dmc.Stack([], id="download-entries-container")
        ]),
    ])


clientside_callback(
    """
    function(n_clicks_list) {
        if (!n_clicks_list) {
            return Array(n_clicks_list.length).fill(false);
        }

        return n_clicks_list.map(n => n > 0);
    }
    """,
    Output({"type": "start-button", "index": ALL}, "loading", allow_duplicate=True),
    Input({"type": "start-button", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)


def register_callback_download(app):
    @app.callback(
        [Output("download-entries-container", "children"),
         Output("rename-input", "value")],
        [State("download-entries-container", "children"),
         State("download-path", "value"),
         State("rename-input", "value"),
         State({"type": "url-input", "index": ALL}, "value"),
         State({"type": "name-input", "index": ALL}, "value"),
         State({"type": "start-button", "index": ALL}, "id")],
        [Input("new-download-btn", "n_clicks"),
         Input({"type": "start-button", "index": ALL}, "n_clicks")],
        prevent_init_call=True,
    )
    def add_new_download_entry(children, output_path, rename, urls, names, button_ids, add_clicks, start_clicks):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update

        # 检查触发的事件是添加新任务还是点击 "Start" 按钮
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'new-download-btn':
            # 添加新条目
            entry_id = str(uuid.uuid4())  # 生成唯一的 entry id
            rename = generate_new_name(rename)
            children.append(add_download_entry(entry_id, rename))
            return children, rename
        elif "start-button" in triggered_id:
            # 处理 Start 按钮逻辑
            # button_id = triggered_id
            # print(f"Button {button_id} clicked!")
            # 可添加具体处理逻辑，例如启动下载
            triggered_id_dict = json.loads(triggered_id)
            for idx, button_id in enumerate(button_ids):
                if button_id["index"] == triggered_id_dict["index"]:
                    url_input = urls[idx]
                    rename_input = names[idx]
                    start_download(url_input, output_path, rename_input)
                    return no_update, no_update
