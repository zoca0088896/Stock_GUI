from nicegui import ui
from apis.utils import FugleManger
import plotly.graph_objects as go

# prevent call api when this module be imported
first_call = True
group_manger = None


@ui.refreshable
def show_group(group_type, upper_bound, lower_bound):
    # when first rendering, call api and create manger
    global first_call, group_manger
    if first_call:
        group_manger = FugleManger()
        first_call = False

    k_timeframe, set_k_timeframe = ui.state("5")

    match group_type:
        case "a":
            # check if selected stocks had changed
            group_manger.refresh_df()
            df_a = group_manger.group_a(percentage=1, upper_bound=upper_bound, lower_bound=lower_bound)
            with ui.row().classes("w-full"):
                group_card(df_a, "text-red", k_timeframe)
        case "b":
            group_manger.refresh_df()
            df_b = group_manger.group_b(percentage=1, upper_bound=upper_bound, lower_bound=lower_bound)
            with ui.row().classes("w-full"):
                group_card(df_b, "text-green", k_timeframe)
        case "c":
            group_manger.refresh_df()
            df_c = group_manger.group_c(percentage=1, upper_bound=upper_bound, lower_bound=lower_bound)
            with ui.row().classes("w-full"):
                group_card(df_c, "text-yellow", k_timeframe)
    ui.button("返回前一頁", on_click=ui.navigate.back).classes("fixed right-4 top-4")
    k_line_container = {"1": "1分k", "3": "3分k", "5": "5分k", "10": "10分k"}
    ui.select(options=k_line_container, on_change=lambda e: set_k_timeframe(e.value), value="5")
    ui.button("1分k", on_click=lambda: set_k_timeframe("1"))
    ui.button("3分k", on_click=lambda: set_k_timeframe("3"))
    ui.button("5分k", on_click=lambda: set_k_timeframe("5"))
    ui.button("10分k", on_click=lambda: set_k_timeframe("10"))


@ui.refreshable
def group_card(group_df, color, k_timeframe):
    def show_row(row):
        with ui.grid(rows="1fr 3fr", columns="1fr 2fr").classes(f"bg-black gap-0 p-1 {color} "
                                                                "basis-5/12 grow shrink-0"):
            with ui.card().classes("no-shadow p-1 bg-black row-start-1 row-end-2 col-span-1"):
                ui.label(f"{row['stock_id']}").classes("text-2xl")
                ui.label(f"{row['name']}").classes("text-3xl")
                ui.separator().classes("bg-grey")
            with ui.card().classes("no-shadow bg-black row-start-2 row-end-3 col-span-1"):
                close_price, change, change_percent = group_manger.refresh_single(row["stock_id"])
                ui.label(f"{close_price}").classes("text-4xl")
                with ui.row():
                    ui.label(f"{change}").classes("text-2xl")
                    ui.label(f"({change_percent})%").classes("text-2xl")

            # 以5分k請求資料
            fig_data = group_manger.get_candle(row['stock_id'], k_timeframe)
            fig = go.Figure(data=go.Candlestick(x=fig_data["date"],
                                                open=fig_data["open"],
                                                high=fig_data["high"],
                                                low=fig_data["low"],
                                                close=fig_data["close"]))
            fig.update_layout(xaxis_rangeslider_visible=False)
            ui.plotly(fig).classes("row-start-1 row-end-3 col-start-2")

    group_df.apply(lambda row: show_row(row), axis=1)
