from nicegui import ui
from apis.utils import FugleManger
import plotly.graph_objects as go
import datetime as dt
from setting.dark_mode import DarkMode

# prevent call api when this module be imported
first_call = True
group_manger = None


@ui.refreshable
def show_group(group_type, upper_bound, lower_bound, strategy_num, notify_num) -> None:
    # when first rendering, call api and create manger
    global first_call, group_manger
    if first_call:
        group_manger = FugleManger()
        first_call = False
    # group card會刷新，所以要將state定義移動到parent內
    # 預設以5分k請求資料
    k_timeframe, set_k_timeframe = ui.state("5")
    try:
        match group_type:
            case "a":
                # check if selected stocks had changed
                group_manger.refresh_df()
                df_a = group_manger.group_a(
                    percentage=strategy_num, upper_bound=upper_bound, lower_bound=lower_bound)
                with ui.grid(rows=df_a.shape[0]+1, columns="1fr 1fr").classes("w-full bg-black gap-1 p-1"):
                    group_card(df_a, "text-red", k_timeframe,
                               set_k_timeframe, strategy_num, notify_num, group_type)
            case "b":
                group_manger.refresh_df()
                df_b = group_manger.group_b(
                    percentage=strategy_num, upper_bound=upper_bound, lower_bound=lower_bound)
                with ui.grid(rows=df_b.shape[0]+1, columns="1fr 1fr").classes("w-full bg-black gap-1 p-1"):
                    group_card(df_b, "text-green",
                               k_timeframe, set_k_timeframe, strategy_num, notify_num, group_type)
            case "c":
                group_manger.refresh_df()
                df_c = group_manger.group_c(
                    percentage=strategy_num, upper_bound=upper_bound, lower_bound=lower_bound)
                with ui.grid(rows=df_c.shape[0]+1, columns="1fr 1fr").classes("w-full bg-black gap-1 p-1"):
                    group_card(df_c, "text-yellow",
                               k_timeframe, set_k_timeframe, strategy_num, notify_num, group_type)

    except Exception as e:
        # 基本方案可能會發生API速率限制問題，所以用try catch來處理
        ui.notify(f"Error: 刷新速度過快，已超過API速率限制60/min，請稍後再試。{e}")
    ui.button("返回前一頁", on_click=ui.navigate.back).classes(
        "fixed right-4 top-4")

    # dark mode
    dark_mode = DarkMode()
    dark_mode.show_switch()


@ui.refreshable
def group_card(group_df, color, k_timeframe, set_k_timeframe, strategy_num, notify_num, group_type) -> None:

    # 時間，10點前才會警示ab，c則是9:15後到收盤
    now = dt.datetime.now()

    # 提醒鈴聲
    ding = ui.audio(
        'notify.mp3', controls=False)

    def alert_notify(message: str) -> None:
        ding.play()
        ui.notify(message, type="warning")

    # 分開渲染刷新單一股票
    def show_row(row):
        with ui.grid(rows="1fr 3fr", columns="1fr 2fr").classes(f"bg-black gap-0 p-1"
                                                                "basis-5/12 grow shrink-0 border-2 border-lime-400"):
            with ui.card().classes(f"no-shadow p-1 bg-black row-start-1 row-end-2 col-span-1 {color}"):
                ui.label(f"{row['stock_id']}").classes("text-2xl")
                ui.label(f"{row['name']}").classes("text-3xl")
                ui.separator().classes("bg-grey")
            with ui.card().classes(f"no-shadow bg-black row-start-2 row-end-3 col-span-1 {color}"):
                close_price, change, change_percent = group_manger.refresh_single(
                    row["stock_id"])
                ui.label(f"{close_price}").classes("text-4xl")
                with ui.row():
                    ui.label(f"{change}").classes("text-2xl")
                    ui.label(f"({change_percent})%").classes("text-2xl")
                k_line_container = {"1": "1分k",
                                    "3": "3分k", "5": "5分k", "10": "10分k"}
                ui.select(options=k_line_container, on_change=lambda e: set_k_timeframe(
                    e.value), value=k_timeframe).classes("text-white bg-white p-1")
                # user notify
                # 9~10點會通知a和b
                if dt.time(9, 0) < now.time() < dt.time(10, 0):
                    if change_percent >= strategy_num + notify_num:
                        # a group
                        alert_notify(
                            f"{row['name']}[{row['stock_id']}] 目前上升超過 {strategy_num + notify_num}%")
                    elif change_percent <= -(strategy_num + notify_num):
                        # b group
                        alert_notify(
                            f"{row['name']}[{row['stock_id']}] 目前下跌超過 {strategy_num + notify_num}%")
                # 9:15~13:30點會通知c
                if dt.time(9, 15) < now.time() < dt.time(13, 30):
                    if change_percent >= notify_num and group_type == "c":
                        # c group
                        alert_notify(
                            f"{row['name']}[{row['stock_id']}] 目前上升超過 {notify_num}%")
                    if change_percent <= -notify_num and group_type == "c":
                        # c group
                        alert_notify(
                            f"{row['name']}[{row['stock_id']}] 目前下跌超過 {notify_num}%")

            fig_data = group_manger.get_candle(row['stock_id'], k_timeframe)
            fig = go.Figure(data=go.Candlestick(x=fig_data["date"],
                                                open=fig_data["open"],
                                                high=fig_data["high"],
                                                low=fig_data["low"],
                                                close=fig_data["close"]))
            fig.update_layout(xaxis_rangeslider_visible=False)
            ui.plotly(fig).classes("row-start-1 row-end-3 col-start-2")

    group_df.apply(lambda row: show_row(row), axis=1)
