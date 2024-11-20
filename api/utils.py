import pandas as pd
from models.stock_model import model_manger
from fugle_marketdata import RestClient
from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()


class FugleManger:
    def __init__(self):
        self.model_manger = model_manger
        self.__end_point = os.getenv("FUGLE_API_ENDPOINT")
        self.client = RestClient(api_key=os.getenv("FUGLE_API_SECRET"))
        self.stock = self.client.stock
        self.selected_df = self.model_manger.get_selected_df()
        self.__organize_df()
        # self.__test()

    def __organize_df(self):
        def organize_helper(row):
            res = self.stock.intraday.quote(symbol=row["stock_id"])
            # print(res)
            # time.sleep(1)
            try:
                percentage_range = round((res["openPrice"] - res["previousClose"]) / res["previousClose"] * 100, 2)
                # percentage_current = round((res["closePrice"] - res["previousClose"]) / res["previousClose"] * 100, 2)
                return (res["closePrice"], res["previousClose"], res["openPrice"],
                        percentage_range, res["change"], res["changePercent"])
            except KeyError:
                # 沒開盤
                return res["previousClose"], res["previousClose"], res["previousClose"], 0, 0, 0

        self.selected_df[["目前股價", "昨日收盤", "開盤", "開盤漲跌百分比", "漲跌", "目前漲跌百分比"]] = self.selected_df.apply(organize_helper,
                                                                                            axis=1,
                                                                                            result_type="expand")

    def update_df(self):
        def update_helper(row):
            res = self.stock.intraday.quote(symbol=row["stock_id"])
            percentage = round((res["closePrice"] - res["previousClose"]) / res["previousClose"] * 100, 2)
            return res["closePrice"], percentage
        self.selected_df[["目前股價", "目前漲跌百分比"]] = self.selected_df.apply(update_helper,
                                                                              axis=1,
                                                                              result_type="expand")

    def group_a(self, percentage: float):
        return self.selected_df[self.selected_df["目前漲跌百分比"] >= percentage]

    def group_b(self, percentage: float):
        return self.selected_df[self.selected_df["目前漲跌百分比"] <= -percentage]

    def group_c(self, percentage: float):
        return self.selected_df[(self.selected_df["目前漲跌百分比"] <= percentage) &
                                (self.selected_df["目前漲跌百分比"] >= -percentage)]

    def get_candle(self, stock_id: str):
        res = self.stock.intraday.candles(symbol=stock_id, timeframe="5")
        data = res["data"]
        fig_data = pd.DataFrame(data=data)
        # print(fig_data)
        return fig_data

    def refresh_df(self):
        sql_df = self.model_manger.get_selected_df()
        # compare stock index
        df_compare = self.selected_df["stock_id"]

    def __test(self):
        for i in ["2213", "0050", "1210", "0056", "3060", "00940", "00878", "1215", "1216", "1225", "1101", "1102", "1103", "1104"]:
            res = self.stock.intraday.quote(symbol=i)
            print(res)

# 快照quotes：
# res = requests.get("https://api.fugle.tw/snapshot/v1.0/quotes/TSE?apiToken=23ac0d4b28e2077a46206fdc24b29c44")
# for stock in res.json()["data"]:
#     print(stock["name"])
# print(len(res.json()["data"]))
