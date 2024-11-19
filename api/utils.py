from models.stock_model import StockModel, Stock
from fugle_marketdata import RestClient
from dotenv import load_dotenv
import os

# 建立資料庫物件並獲取已選擇的df
model_manger = StockModel("sqlite:///models/stocks.db")
df = model_manger.get_df()
df = df[df["selected"] == 1]
print(df.head())
