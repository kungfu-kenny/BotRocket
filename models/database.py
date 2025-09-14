from typing import Optional, List
from sqlalchemy import ForeignKey
from sqlalchemy import (
    Float,
    String,
    Boolean,
    Integer,
)
# from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from contextlib import contextmanager
from config import DATABASE_URL


class Base(DeclarativeBase):
    pass


class UserAdmins(Base):
    __tablename__ = "user_admins"
    id_user: Mapped[int] = mapped_column(Integer(), ForeignKey('user_accounts.id'), primary_key=True)
    id_admin: Mapped[int] = mapped_column(Integer(), ForeignKey('user_accounts.id'), primary_key=True)
    user: Mapped[List["User"]] = relationship(
        foreign_keys=[id_user])
    admin: Mapped[List["User"]] = relationship(
        foreign_keys=[id_admin])


class UserPayment(Base):
    __tablename__ = "user_payments"
    id_payment: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(Integer(), ForeignKey('user_accounts.id'))
    payment_date: Mapped[str] = mapped_column(String(30))
    user_payed: Mapped[List["User"]] = relationship(
        foreign_keys=[id_user]
    )


class UserShopList(Base):
    __tablename__ = "user_shop_lists"
    id_user: Mapped[int] = mapped_column(Integer(), ForeignKey('user_accounts.id'), primary_key=True)
    id_shop_list: Mapped[int] = mapped_column(Integer(), ForeignKey('shop_list.id'), primary_key=True)
    shop_list_date: Mapped[str] = mapped_column(String(30))
    user: Mapped[List["User"]] = relationship(
        foreign_keys=[id_user],
    )
    shop: Mapped[List["ShopList"]] = relationship(
        foreign_keys=[id_shop_list],
    )


class User(Base):
    __tablename__ = "user_accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]
    surname: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)
    join_date_start: Mapped[Optional[str]]
    join_date_end: Mapped[Optional[str]]
    relation_user_list:Mapped[List["UserShopList"]] = relationship(
        back_populates="user",
        foreign_keys=[UserShopList.id_user],
    )
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, surname={self.surname!r}, username={self.username!r}, admin={self.is_admin!r})"


# TODO continue work from here
class AdminSettings(Base):
    __tablename__ = 'admin_settings'
    id: Mapped[int] = mapped_column(Integer(), ForeignKey('user_accounts.id'), primary_key=True)
    show_responsible: Mapped[bool] = mapped_column(Boolean(), default=True)
    show_day_minus:Mapped[bool] = mapped_column(Boolean(), default=True)
    show_overdue:Mapped[bool] = mapped_column(Boolean(), default=True)
    show_inactive:Mapped[bool] = mapped_column(Boolean(), default=True)
    show_new_users:Mapped[bool] = mapped_column(Boolean(), default=True)
    show_unattached: Mapped[bool] = mapped_column(Boolean(), default=True)
    id_admin: Mapped[List["User"]] = relationship(
        foreign_keys=[id],
    )

#TODO work after here
# class UserPass(Base):
#     __tablename__ = 'user_season_pass'


class ShopList(Base):
    __tablename__ = 'shop_list'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(300))
    price: Mapped[int] = mapped_column(Float())
    usershop_list: Mapped[List["UserShopList"]] = relationship(
        back_populates="shop",
        foreign_keys=[UserShopList.id_shop_list],
    )


def engine_develop():
    engine = create_engine(
        DATABASE_URL,
        echo=True,
    )
    Base.metadata.create_all(engine)


@contextmanager
def db_session(db_url:str=DATABASE_URL):
    try:
        engine = create_engine(db_url, echo=True)
        connection = engine.connect()
        db_session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=True,
                bind=engine,
            )
        )
        yield db_session
    finally:
        db_session.close()
        connection.close()
