import datetime
import enum
from typing import Annotated

from sqlalchemy import ForeignKey, text, select
from sqlalchemy.orm import mapped_column, Mapped, relationship, Session

from database.database_init import Base



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
    id: Mapped[int]
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
        user_material = session.execute(query).scalars().first()
        if user_material:
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
