from nicegui import ui


@ui.refreshable
def main_menu():
    # open and close strategy range state
    upper_bound, set_upper = ui.state(1)
    lower_bound, set_lower = ui.state(-2)

    def set_new_bound(new_upper, new_lower):
        set_upper(new_upper)
        set_lower(new_lower)

    with (ui.grid(columns="1fr repeat(3, 30%) 1fr").classes(
            "w-full absolute bottom-1/2 right-1/2 translate-x-1/2 translate-y-1/2 text-xl")):
        with ui.card().classes("col-start-2"):
            ui.label("分組股票查看").classes("text-xl bg-blue w-full text-center text-slate-50")
            ui.label(f"當前開盤漲跌區間：+{upper_bound}% ~ {lower_bound}%")
            ui.label(f"A組策略：當前區間目前上漲1%以上股票")
            ui.label(f"B組策略：當前區間目前下跌1%以上股票")
            ui.label(f"C組策略：當前區間目前不屬於A、B兩組股票")
            ui.label("選擇分組，進入自選股分組頁面：")
            with ui.row():
                ui.button("A", on_click=lambda: ui.navigate.to(f"/group/a/{upper_bound}/{lower_bound}")).classes("bg-red text-black text-lg")
                ui.button("B", on_click=lambda: ui.navigate.to(f"/group/b/{upper_bound}/{lower_bound}")).classes("bg-green text-black text-lg")
                ui.button("C", on_click=lambda: ui.navigate.to(f"/group/c/{upper_bound}/{lower_bound}")).classes("bg-yellow text-black text-lg")
        with ui.card().classes("col-start-3"):
            ui.label("修改開盤策略").classes("text-xl bg-blue w-full text-center text-slate-50")
            upper_num = ui.number(label="漲幅上限", value=1, step=0.1, min=0, format="%.1f",
                                  on_change=lambda e: new_upper_info.set_text(f"漲幅上限修改至: +{e.value}%"))
            new_upper_info = ui.label()
            lower_num = ui.number(label="跌幅下限", value=-2, step=0.1, max=0, format="%.1f",
                                  on_change=lambda e: new_lower_info.set_text(f"跌幅下限修改至: {e.value}%"))
            new_lower_info = ui.label()
            with ui.row():
                ui.button("回復預設範圍", on_click=lambda: set_new_bound(1, 2)
                          ).classes("text-lg")
                ui.button(text="確認修改",
                          on_click=lambda: set_new_bound(upper_num.value, lower_num.value)
                          ).classes("text-lg")

        with ui.card().classes("col-start-4"):
            ui.label("新增自選股").classes("text-xl bg-blue w-full text-center text-slate-50")
            ui.label("將指定股票加入/移除觀察清單")
            ui.button("前往新增", on_click=lambda: ui.navigate.to("/add"))
