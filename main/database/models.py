import datetime
import enum
from typing import Annotated

from sqlalchemy import ForeignKey, text, select
from sqlalchemy.orm import mapped_column, Mapped, relationship, Session

from database.database_init import Base

from sqlalchemy import Column, Integer, String, Text, Enum


intpk = Annotated[int, mapped_column(autoincrement=True, primary_key=True)]


class UserRole(enum.Enum):
    admin = "ADMIN"
    user = "USER"


class UserMaterials(Base):
    __tablename__ = "user_materials"
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    count: Mapped[int]
    user_phone: Mapped[str]
    material_name: Mapped[str]
    date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())


class User(Base):
    __tablename__ = "users"
    id: Mapped[intpk] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    key_word_id: Mapped[int] = mapped_column(ForeignKey("keywords.id", ondelete="CASCADE"))
    key_word: Mapped["Keyword"] = relationship(back_populates="users")
    role: Mapped[UserRole] = mapped_column(default=UserRole.user)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    chat_id: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    region: Mapped[str] = mapped_column(nullable=True)
    #materials: Mapped[list["Material"]] = relationship(back_populates="users", secondary="user_materials")

    def add_material(self, session: Session, material_name: str):
        query = select(UserMaterials).where(
            (UserMaterials.user_id == self.id) & (UserMaterials.material_name == material_name))
        if user_material := session.execute(query).scalars().first():
            user_material.count += 1
        else:
            user_material = UserMaterials(user_id=self.id, count=1,
                                          user_phone=self.phone_number, material_name=material_name)
            session.add(user_material)
        session.commit()


class Keyword(Base):
    __tablename__ = "keywords"
    id: Mapped[intpk]
    key_word: Mapped[str]
    users: Mapped[list["User"]] = relationship(back_populates="key_word")


class Mailing(Base):
    __tablename__ = 'mailings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)  # Заголовок рассылки
    content = Column(Text, nullable=False)  # Текст рассылки

    mailing_type = Column(Enum('keyword', 'region', 'all_users', name='mailing_type_enum'), nullable=False)

    keyword = Column(String(255), nullable=True)
    region = Column(String(255), nullable=True)



# class Material(Base):
#     __tablename__ = "materials"
#     id: Mapped[intpk]
#     name: Mapped[str]
#     key_word: Mapped[str]
#     users: Mapped[list[User]] = relationship(back_populates="materials", secondary="user_materials")


# class Question(Base):
#     __tablename__ = "questions"
#     id: Mapped[intpk]
#     phone_number: Mapped[str]
#     question: Mapped[str]
