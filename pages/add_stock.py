from nicegui import ui
import requests


@ui.refreshable
def add_stock():
    ui.label("新增股票")
    ui.button("返回主頁", on_click=lambda: ui.navigate.to("/"))
