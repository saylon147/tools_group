import json
import os
import uuid
import re

import certifi
import requests
import dash_mantine_components as dmc
from dash import html, Output, Input, State, ALL, no_update, callback_context, clientside_callback
from dash_iconify import DashIconify


def start_download(url, save_path, new_filename):
    url = url.strip()
    save_path = save_path.strip()
    new_filename = new_filename.strip()
    # print(url, save_path, new_filename)

    # 确保保存路径存在
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 构建完整的保存路径，包括文件名
    file_path = os.path.join(save_path, f"{new_filename}.mp3")

    # 发送请求，获取MP3文件内容
    response = requests.get(url, stream=True, verify=certifi.where())
    if response.status_code == 200:
        with open(file_path, 'wb') as mp3_file:
            # 将文件分块写入，避免占用大量内存
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    mp3_file.write(chunk)
        print(f"MP3 file downloaded and saved as: {file_path}")
    else:
        print(f"Failed to download the MP3 file. Status code: {response.status_code}")


def add_download_entry(entry_id, rename):
    return dmc.Group([
        dmc.TextInput("", placeholder="url", style={"flex": "1"}, id={"type": "url-input", "index": entry_id}),
        dmc.TextInput(rename, placeholder="rename", w=200, id={"type": "name-input", "index": entry_id}),
        dmc.Button("Start", id={"type": "start-button", "index": entry_id}),
        dmc.Button("Finish", color="lime", id={"type": "finish-button", "index": entry_id}),
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
         Input({"type": "start-button", "index": ALL}, "n_clicks"),
         Input({"type": "finish-button", "index": ALL}, "n_clicks")],
        prevent_init_call=True,
    )
    def add_new_download_entry(children, output_path, rename, urls, names, button_ids,
                               add_clicks, start_clicks, finish_clicks):
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
        elif "finish-button" in triggered_id:
            triggered_id_dict = json.loads(triggered_id)
            entry_to_remove = triggered_id_dict["index"]
            # 从 children 列表中移除相应的条目
            children = [
                child for child in children
                if not any(
                    comp['props']['id'].get('type') == 'finish-button' and
                    comp['props']['id'].get('index') == entry_to_remove
                    for comp in child['props']['children']
                )
            ]
            return children, no_update
