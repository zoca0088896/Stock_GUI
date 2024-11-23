import pandas as pd
from models.stock_model import model_manger
from fugle_marketdata import RestClient
from dotenv import load_dotenv
import os

load_dotenv()


class FugleManger:

    def __init__(self):
        self.model_manger = model_manger
        self.__end_point = os.getenv("FUGLE_API_ENDPOINT")
        self.client = RestClient(api_key=os.getenv("FUGLE_API_SECRET"))
        self.stock = self.client.stock
        self.selected_df = self.model_manger.get_selected_df()
        self.__organize_df()

    def __organize_df(self):
        def organize_helper(row):
            res = self.stock.intraday.quote(symbol=row["stock_id"])
            print(res)
            try:
                percentage_range = round((res["openPrice"] - res["previousClose"]) / res["previousClose"] * 100, 2)
                return (res["closePrice"], res["previousClose"], res["openPrice"],
                        percentage_range, res["change"], res["changePercent"])
            except KeyError:
                # 沒開盤
                return res["previousClose"], res["previousClose"], res["previousClose"], 0, 0, 0
        self.selected_df[["currentPrice", "previous_close", "open_price", "open_change_range", "change", "change_percent"]] \
            = self.selected_df.apply(organize_helper, axis=1, result_type="expand")

    def group_a(self, percentage: float, upper_bound: float, lower_bound: float):
        df_a = self.selected_df[(self.selected_df["open_change_range"] <= upper_bound)
                                & (self.selected_df["open_change_range"] >= lower_bound)]
        return df_a[df_a["change_percent"] >= percentage]

    def group_b(self, percentage: float, upper_bound: float, lower_bound: float):
        df_b = self.selected_df[(self.selected_df["open_change_range"] <= upper_bound)
                                & (self.selected_df["open_change_range"] >= lower_bound)]
        return df_b[df_b["change_percent"] <= -percentage]

    def group_c(self, percentage: float, upper_bound: float, lower_bound: float):
        df_c = self.selected_df[(self.selected_df["open_change_range"] <= upper_bound)
                                & (self.selected_df["open_change_range"] >= lower_bound)]
        return df_c[(df_c["change_percent"] <= percentage)
                    & (df_c["change_percent"] >= -percentage)]

    # 定期刷新用
    def refresh_single(self, stock_id: str):
        res = self.stock.intraday.quote(symbol=stock_id)
        try:
            return res["closePrice"], res["change"], res["changePercent"]
        except KeyError:
            # 沒開盤
            return res["previousClose"], 0, 0

    def get_candle(self, stock_id: str, timeframe: str):
        res = self.stock.intraday.candles(symbol=stock_id, timeframe=timeframe)
        data = res["data"]
        fig_data = pd.DataFrame(data=data)
        return fig_data

    def refresh_df(self) -> None:
        sql_df = self.model_manger.get_selected_df()
        # 先檢查長度
        if len(sql_df["stock_id"]) == len(self.selected_df["stock_id"]):
            # 長度相等時要檢查內容
            result = sql_df["stock_id"].compare(self.selected_df["stock_id"])
            if len(result) == 0:
                return None
        # 確定不同，則重構選擇股票池
        else:
            self.selected_df = self.model_manger.get_selected_df()
            self.__organize_df()
            return None
