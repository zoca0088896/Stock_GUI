from nicegui import ui
from apis.utils import FugleManger
import plotly.graph_objects as go

first_call = True
group_manger = None


@ui.refreshable
def show_group(group_type, upper_bound, lower_bound):
    global first_call, group_manger
    if first_call:
        group_manger = FugleManger()
        first_call = False
    match group_type:
        case "a":
            group_manger.refresh_df()
            df_a = group_manger.group_a(percentage=1, upper_bound=upper_bound, lower_bound=lower_bound)
            with ui.row().classes("w-full"):
                group_card(df_a, "text-red")
        case "b":
            group_manger.refresh_df()
            df_b = group_manger.group_b(percentage=1, upper_bound=upper_bound, lower_bound=lower_bound)
            with ui.row().classes("w-full"):
                group_card(df_b, "text-green")
        case "c":
            group_manger.refresh_df()
            df_c = group_manger.group_c(percentage=1, upper_bound=upper_bound, lower_bound=lower_bound)
            with ui.row().classes("w-full"):
                group_card(df_c, "text-yellow")
    ui.button("返回前一頁", on_click=ui.navigate.back).classes("fixed right-4 top-4")


@ui.refreshable
def group_card(group_df, color):
    def show_row(row):
        with ui.grid(rows="1fr 3fr", columns="1fr 2fr").classes(f"bg-black gap-0 p-1 {color} "
                                                                "basis-5/12 grow shrink-0"):
            with ui.card().classes("no-shadow p-1 bg-black row-start-1 row-end-2 col-span-1"):
                ui.label(f"{row['stock_id']}").classes("text-2xl")
                ui.label(f"{row['name']}").classes("text-3xl")
                ui.separator().classes("bg-grey")
            with ui.card().classes("no-shadow bg-black row-start-2 row-end-3 col-span-1"):
                colse_price, change, chage_percent = group_manger.refresh_single(row["stock_id"])
                ui.label(f"{colse_price}").classes("text-4xl")
                with ui.row():
                    ui.label(f"{change}").classes("text-2xl")
                    ui.label(f"({chage_percent})%").classes("text-2xl")
            fig_data = group_manger.get_candle(row['stock_id'])
            fig = go.Figure(data=go.Candlestick(x=fig_data["date"],
                                                open=fig_data["open"],
                                                high=fig_data["high"],
                                                low=fig_data["low"],
                                                close=fig_data["close"]))
            fig.update_layout(xaxis_rangeslider_visible=False)
            ui.plotly(fig).classes("row-start-1 row-end-3 col-start-2")

    group_df.apply(lambda row: show_row(row), axis=1)
