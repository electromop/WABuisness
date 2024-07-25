import datetime
import enum
from typing import Annotated

from sqlalchemy import ForeignKey, text, select, and_
from sqlalchemy.orm import mapped_column, Mapped, relationship, Session

from database.database_init import Base

intpk = Annotated[int, mapped_column(autoincrement=True, primary_key=True)]


class UserRole(enum.Enum):
    admin = "ADMIN"
    user = "USER"


class User(Base):
    __tablename__ = "users"
    id: Mapped[intpk]
    name: Mapped[str]
    key_word: Mapped[str]
    role: Mapped[UserRole]
    phone_number: Mapped[str]
    chat_id: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[datetime.datetime] = mapped_column(default=text("TIMEZONE('utc', now())"))
    region: Mapped[str]
    #team: Mapped[list["User"]] = relationship(back_populates="parent")
    #parent: Mapped["User"] = relationship(remote_side=[.id], back_populates="team")
    #parent_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    materials: Mapped[list["Material"]] = relationship(back_populates="users", secondary="user_materials")

    def add_material(self, session: Session, material: 'Material'):
        query = select(UserMaterials).where(and_(User.id == self.id, Material.id == material.id))
        user_material = session.execute(query).scalars().first()
        if user_material:
            user_material.count += 1
        else:
            user_material = UserMaterials(user_id=self.id, material_id=material.id, count=1)
            session.add(user_material)
        session.commit()


class UserMaterials(Base):
    __tablename__ = "user_materials"
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    material_id = mapped_column(ForeignKey("materials.id", ondelete="CASCADE"), primary_key=True)
    count: Mapped[int]


class Material(Base):
    __tablename__ = "materials"
    id: Mapped[intpk]
    name: Mapped[str]
    key_word: Mapped[str]
    users: Mapped[list[User]] = relationship(back_populates="materials", secondary="user_materials")
