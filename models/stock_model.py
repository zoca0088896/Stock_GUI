import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Stock(Base):
    __tablename__ = "stocks"

    代號: Mapped[str] = mapped_column(primary_key=True, comment="代號")
    名稱: Mapped[str] = mapped_column(comment="名稱")
    市場: Mapped[str] = mapped_column(comment="市場")
    觀察中: Mapped[int] = mapped_column(default=0, comment="觀察中")
    當日前15分最高價: Mapped[float] = mapped_column(default=0, comment="當日前15分最高價")


class StockModel:
    def __init__(self, url) -> None:
        self.url = url
        self.engine = create_engine(self.url, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def get_df(self) -> pd.DataFrame:
        return pd.read_sql_table("stocks", self.engine)

    def get_selected_df(self) -> pd.DataFrame:
        df = pd.read_sql_table("stocks", self.engine)
        return df[df["觀察中"] == 1].copy()

    def update_selected(self, keys: list) -> None:
        with self.Session() as session:
            session.query(Stock).where(Stock.代號.in_(
                keys)).update({Stock.觀察中: 1})
            session.commit()

    def update_selected_by_id(self, stock_id) -> None:
        with self.Session() as session:
            session.query(Stock).where(Stock.代號 ==
                                       stock_id).update({Stock.觀察中: 1})
            session.commit()

    def update_unselected(self, stock_id) -> None:
        with self.Session() as session:
            session.query(Stock).where(Stock.代號 ==
                                       stock_id).update({Stock.觀察中: 0})
            session.commit()

    def update_15min_high(self, stock_id, price) -> None:
        with self.Session() as session:
            session.query(Stock).where(Stock.代號 ==
                                       stock_id).update({Stock.當日前15分最高價: price})
            session.commit()

    def add_stock(self, stock_id, stock_name, stock_type, stock_selected=0) -> None:
        with self.Session() as session:
            new_stock = Stock(代號=stock_id,
                              名稱=stock_name,
                              市場=stock_type,
                              觀察中=stock_selected,
                              當日前15分最高價=0)
            session.add(new_stock)
            session.commit()


# remember url is depended on which import module
model_manger = StockModel("sqlite:///models/stocks.db")
