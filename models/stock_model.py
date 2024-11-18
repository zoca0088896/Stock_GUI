import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# engine = create_engine("sqlite:///stocks.db", echo=True)


class Base(DeclarativeBase):
    pass


class Stock(Base):
    __tablename__ = "stocks"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    selected: Mapped[int] = mapped_column(default=0)


class StockModel:
    def __init__(self, url):
        self.url = url
        self.engine = create_engine(self.url, echo=True)

    def get_df(self):
        return pd.read_sql_table("stocks", self.engine)

