from nicegui import ui
from api.utils import FugleManger
import matplotlib.pyplot as plt
import plotly.graph_objects as go


@ui.refreshable
def show_group(group_type, upper_bound, lower_bound):
    group_manger = FugleManger()
    match group_type:
        case "a":
            ui.table.from_pandas(group_manger.group_a(1))
            ui.label("a")
        case "b":
            df_b = group_manger.group_b(1)
            with ui.row().classes("w-full"):
                group_card(group_manger, df_b)
            ui.label("b")
        case _:
            df_c = group_manger.group_c(1)
            with ui.row().classes("w-full"):
                group_card(group_manger, df_c)
    ui.button("返回前一頁", on_click=ui.navigate.back).classes("fixed right-4 top-4")


@ui.refreshable
def group_card(group_manger, group_df):
    def show_row(row):
        with ui.grid(rows="1fr 3fr", columns="1fr 2fr").classes("bg-black gap-0 p-1 text-white "
                                                                "basis-5/12 grow shrink-0"):
            with ui.card().classes("no-shadow p-1 bg-black row-start-1 row-end-2 col-span-1"):
                ui.label(f"{row['stock_id']}").classes("text-2xl")
                ui.label(f"{row['name']}").classes("text-3xl")
                ui.separator().classes("bg-grey")
            with ui.card().classes("no-shadow bg-black row-start-2 row-end-3 col-span-1"):
                ui.label(f"{row['目前股價']}").classes("text-4xl")
                with ui.row():
                    ui.label(f"{row['漲跌']}").classes("text-2xl")
                    ui.label(f"({row['目前漲跌百分比']})%").classes("text-2xl")
            fig_data = group_manger.get_candle(row['stock_id'])
            fig = go.Figure(data=go.Candlestick(x=fig_data["date"],
                                                open=fig_data["open"],
                                                high=fig_data["high"],
                                                low=fig_data["low"],
                                                close=fig_data["close"]))
            fig.update_layout(xaxis_rangeslider_visible=False)
            ui.plotly(fig).classes("row-start-1 row-end-3 col-start-2")

    group_df.apply(lambda row: show_row(row), axis=1)
