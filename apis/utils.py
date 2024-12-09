import pandas as pd
from models.stock_model import model_manger
from fugle_marketdata import RestClient
from dotenv import load_dotenv
import os
import datetime as dt

load_dotenv()


class FugleManger:

    def __init__(self) -> None:
        self.model_manger = model_manger
        self.__end_point = os.getenv("FUGLE_API_ENDPOINT")
        self.client = RestClient(api_key=os.getenv("FUGLE_API_SECRET"))
        self.stock = self.client.stock
        self.selected_df = self.model_manger.get_selected_df()
        self.__organize_df()

    def __organize_df(self) -> None:
        def organize_helper(row):
            res = self.stock.intraday.quote(symbol=row["代號"])
            now = dt.datetime.now()
            try:
                # 前15分鐘的最高價格，順便計入資料庫
                if now.time() >= dt.time(9, 0) and now.time() <= dt.time(9, 15):
                    self.model_manger.update_15min_high(
                        row["代號"], res["highPrice"])
                    percentage_range = round(
                        (res["openPrice"] - res["previousClose"]) / res["previousClose"] * 100, 2)
                    return (res["closePrice"], res["previousClose"], res["openPrice"],
                            percentage_range, res["change"], res["changePercent"], res["highPrice"])
                else:
                    # 已經過前15分鐘，就用原本的資料庫資料
                    percentage_range = round(
                        (res["openPrice"] - res["previousClose"]) / res["previousClose"] * 100, 2)
                    return (res["closePrice"], res["previousClose"], res["openPrice"],
                            percentage_range, res["change"], res["changePercent"], row["當日前15分最高價"])
            except KeyError:
                # 沒開盤
                return res["previousClose"], res["previousClose"], res["previousClose"], 0, 0, 0, 0
            except Exception as e:
                # throw exception
                print(e)
                raise e
        self.selected_df[["currentPrice", "previous_close", "open_price", "open_change_range", "change",
                          "change_percent", "當日前15分最高價"]] = self.selected_df.apply(organize_helper, axis=1, result_type="expand")

        print(self.selected_df)
        print(self.selected_df.dtypes)

    def group_a(self, percentage: float, upper_bound: float, lower_bound: float) -> pd.DataFrame:
        df_a = self.selected_df[(self.selected_df["open_change_range"] <= upper_bound)
                                & (self.selected_df["open_change_range"] >= lower_bound)]
        return df_a[df_a["change_percent"] >= percentage]

    def group_b(self, percentage: float, upper_bound: float, lower_bound: float) -> pd.DataFrame:
        df_b = self.selected_df[(self.selected_df["open_change_range"] <= upper_bound)
                                & (self.selected_df["open_change_range"] >= lower_bound)]
        return df_b[df_b["change_percent"] <= -percentage]

    def group_c(self, percentage: float, upper_bound: float, lower_bound: float) -> pd.DataFrame:
        # 突破當日前15分鐘最高價指定百分比
        df_c = self.selected_df[(self.selected_df["open_change_range"] <= upper_bound)
                                & (self.selected_df["open_change_range"] >= lower_bound)]
        df_c = df_c[df_c["當日前15分最高價"] != 0]
        # 大於等於最高價以上指定的百分比
        df_c = df_c[df_c["currentPrice"] >= df_c["當日前15分最高價"] * (1 + percentage / 100)]
        print(df_c)
        return df_c

    # 定期刷新用
    def refresh_single(self, stock_id: str) -> tuple:
        res = self.stock.intraday.quote(symbol=stock_id)
        try:
            return res["closePrice"], res["change"], res["changePercent"]
        except KeyError:
            # 沒開盤
            return res["previousClose"], 0, 0

    def get_candle(self, stock_id: str, timeframe: str) -> pd.DataFrame:
        try:
            res = self.stock.intraday.candles(
                symbol=stock_id, timeframe=timeframe)
            data = res["data"]
            if data:
                fig_data = pd.DataFrame(data=data)
                return fig_data
            else:
                # fix no candle data issue
                return pd.DataFrame([{
                    "date": dt.datetime.today(),
                    "open": 0,
                    "high": 0,
                    "low": 0,
                    "close": 0,
                    "volume": 0,
                    "average": 0
                }])
        except Exception as e:
            # 刷新過快
            raise e

    def refresh_df(self) -> None:
        sql_df = self.model_manger.get_selected_df()
        # 先檢查長度
        if len(sql_df["代號"]) == len(self.selected_df["代號"]):
            # 長度相等時要檢查內容
            result = sql_df["代號"].compare(self.selected_df["代號"])
            if len(result) == 0:
                return None
        # 確定不同，則重構選擇股票池
        else:
            self.selected_df = self.model_manger.get_selected_df()
            self.__organize_df()
            return None
