import requests
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine("sqlite:///stocks.db", echo=True)


class Base(DeclarativeBase):
    pass


class Stock(Base):
    __tablename__ = "stocks"

    stock_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    selected: Mapped[int] = mapped_column(default=0)


Base.metadata.create_all(engine, checkfirst=True)


# 證交所清單連結
listed_company = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
otc_company = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4"

# 獲取清單html文檔
listed_company_text = requests.get(listed_company).text
otc_company_text = requests.get(otc_company).text


# 轉換成df並存入db
def create_db(html_text, method):
    df1 = pd.read_html(StringIO(html_text))[0]
    df1.columns = df1.iloc[0]
    df1 = df1.drop([0, 1], axis=0)[["有價證券代號及名稱", "市場別"]]

    df_listed = df1["有價證券代號及名稱"].str.split("　", expand=True).copy()
    df_listed["市場別"] = df1["市場別"]
    df_listed["selected"] = 0
    df_listed.columns = ["stock_id", "name", "type", "selected"]
    df_listed.dropna(inplace=True)
    df_listed.set_index("stock_id", inplace=True)
    df_listed.to_sql("stocks", engine, if_exists=method)


create_db(listed_company_text, "replace")
create_db(otc_company_text, "append")
