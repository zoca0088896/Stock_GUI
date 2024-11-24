import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Stock(Base):
    __tablename__ = "stocks"

    stock_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    selected: Mapped[int] = mapped_column(default=0)


class StockModel:
    def __init__(self, url) -> None:
        self.url = url
        self.engine = create_engine(self.url, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def get_df(self) -> pd.DataFrame:
        return pd.read_sql_table("stocks", self.engine)

    def get_selected_df(self) -> pd.DataFrame:
        df = pd.read_sql_table("stocks", self.engine)
        return df[df["selected"] == 1].copy()

    def update_selected(self, keys: list) -> None:
        with self.Session() as session:
            session.query(Stock).where(Stock.stock_id.in_(
                keys)).update({Stock.selected: 1})
            session.commit()

    def update_unselected(self, stock_id) -> None:
        with self.Session() as session:
            session.query(Stock).where(Stock.stock_id ==
                                       stock_id).update({Stock.selected: 0})
            session.commit()

    def add_stock(self, stock_id, stock_name, stock_type, stock_selected=0) -> None:
        with self.Session() as session:
            new_stock = Stock(stock_id=stock_id,
                              name=stock_name,
                              type=stock_type,
                              selected=stock_selected)
            session.add(new_stock)
            session.commit()


# remember url is depended on which import module
model_manger = StockModel("sqlite:///models/stocks.db")
