from nicegui import ui, background_tasks
from setting.user import UserSetting
from setting.dark_mode import DarkMode


@ui.refreshable
def main_menu() -> None:

    # 建立user物件，包含設定值和更改設定值的方法
    user = UserSetting()

    # 各分類的功能
    with (ui.grid(columns="1fr repeat(3, 30%) 1fr").classes(
            "w-full absolute bottom-1/2 right-1/2 translate-x-1/2 translate-y-1/2 text-xl")):
        # 各分組進入頁面
        with ui.card().classes("col-start-2"):
            ui.label("分組股票查看").classes(
                "text-xl bg-blue w-full text-center text-slate-50")
            ui.label(
                f"A組策略：\n\t+{user.upper_bound_a} % ~ {user.lower_bound_a} % 區間開盤，目前上漲{user.group_strategy_a} % 以上股票"
            )
            ui.label(
                f"B組策略：\n\t+{user.upper_bound_b}% ~ {user.lower_bound_b}%區間開盤，目前下跌{user.group_strategy_b}%以上股票"
            )
            ui.label(
                f"C組策略：\n\t+{user.upper_bound_c}% ~ {user.lower_bound_c}%區間開盤，突破開盤後15分鐘內最高值{user.group_strategy_c}%以上的股票"
            )
            ui.label("選擇分組，進入自選股分組頁面：")
            with ui.row():
                ui.button("A", on_click=lambda: ui.navigate.to(
                    f"/group/a/{user.upper_bound_a}/{user.lower_bound_a}/{user.group_strategy_a}")).classes("bg-red text-black text-lg")
                ui.button("B", on_click=lambda: ui.navigate.to(
                    f"/group/b/{user.upper_bound_b}/{user.lower_bound_b}/{user.group_strategy_b}")).classes("bg-green text-black text-lg")
                ui.button("C", on_click=lambda: ui.navigate.to(
                    f"/group/c/{user.upper_bound_c}/{user.lower_bound_c}/{user.group_strategy_c}")).classes("bg-yellow text-black text-lg")
        # 修改各分組策略
        with ui.card().classes("col-start-3"):
            ui.label("修改A組策略").classes(
                "text-xl bg-blue w-full text-center text-slate-50")
            group_setting(user.upper_bound_a, user.lower_bound_a,
                          user.group_strategy_a, user.set_new_bound_a, "a")
            ui.label("修改B組策略").classes(
                "text-xl bg-blue w-full text-center text-slate-50")
            group_setting(user.upper_bound_b, user.lower_bound_b,
                          user.group_strategy_b, user.set_new_bound_b, "b")
            ui.label("修改C組策略").classes(
                "text-xl bg-blue w-full text-center text-slate-50")
            group_setting(user.upper_bound_c, user.lower_bound_c,
                          user.group_strategy_c,  user.set_new_bound_c, "c")
        # 新增自選股
        with ui.card().classes("col-start-4"):
            ui.label("新增自選股").classes(
                "text-xl bg-blue w-full text-center text-slate-50")
            ui.label("將指定股票加入/移除觀察清單")
            ui.button("前往新增", on_click=lambda: ui.navigate.to("/add"))

    # dark mode
    dark_mode = DarkMode()
    dark_mode.show_switch()

# 各組策略修改card row


def group_setting(upper_bound, lower_bound, group_strategy, set_new_bound, group) -> None:
    with ui.row():
        new_upper_info = ui.label().classes("text-sm")
        new_lower_info = ui.label().classes("text-sm")
        new_group_strategy = ui.label().classes("text-sm")
    with ui.row():
        upper_num = ui.number(label="開盤漲幅上限", value=upper_bound, step=0.1, min=0, format="%.1f",
                              on_change=lambda e: new_upper_info.set_text(f"漲幅上限修改至: +{e.value}%"))

        lower_num = ui.number(label="開盤跌幅下限", value=lower_bound, step=0.1, max=0, format="%.1f",
                              on_change=lambda e: new_lower_info.set_text(f"跌幅下限修改至: {e.value}%"))
        if group in ["a", "b"]:
            strategy_num = ui.number(label="當前漲跌", value=group_strategy, step=0.1, min=0, format="%.1f",
                                     on_change=lambda e: new_group_strategy.set_text(f"新的漲跌修改至: {e.value}%"))
        else:
            strategy_num = ui.number(label="突破上限百分比", value=group_strategy, step=0.1, min=0, format="%.1f",
                                     on_change=lambda e: new_group_strategy.set_text(f"新的突破值修改至: {e.value}%"))
    with ui.row():
        ui.button("回復預設範圍", on_click=lambda: set_new_bound(1.0, -2.0, 1.0)
                  ).classes("text-lg")
        ui.button(text="確認修改",
                  on_click=lambda: set_new_bound(
                      upper_num.value, lower_num.value, strategy_num.value)
                  ).classes("text-lg")
