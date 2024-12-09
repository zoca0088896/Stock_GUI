import pandas as pd
from sqlalchemy import create_engine, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine("sqlite:///stocks.db", echo=True)


class Base(DeclarativeBase):
    pass


class Stock(Base):
    __tablename__ = "stocks"

    代號: Mapped[str] = mapped_column(primary_key=True, comment="代號")
    名稱: Mapped[str] = mapped_column(comment="名稱")
    市場: Mapped[str] = mapped_column(comment="市場")
    觀察中: Mapped[int] = mapped_column(default=0, comment="觀察中")
    當日前15分最高價: Mapped[float] = mapped_column(default=0.00, comment="當日前15分最高價")


Base.metadata.create_all(engine, checkfirst=True)


listed_company_path = "./models/上市股票.csv"
otc_company_path = "./models/上櫃股票.csv"

# 轉換成df並存入db


def create_db(path, method):
    df1 = pd.read_csv(path)

    df_listed = df1[["代號", "名稱", "市場"]].copy()
    df_listed["觀察中"] = 0
    df_listed["當日前15分最高價"] = 0.00
    df_listed.set_index("代號", inplace=True)
    print(df_listed.head())
    df_listed.to_sql("stocks", engine, if_exists=method)


create_db(listed_company_path, "replace")
create_db(otc_company_path, "append")
