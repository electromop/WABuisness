from sqlalchemy import select
from sqlalchemy.orm import selectinload


from database.database_init import engine, Base, session_factory
from database.models import User, Material, UserRole


class SyncORM:

    @staticmethod
    def create_table():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    @staticmethod
    def check_key(key: str):
        query = select(User).where(User.key_word == key)
        with session_factory() as session:
            res = session.execute(query)
            result = res.scalars().first()
            return result

    @staticmethod
    def find_material(key: str):
        query = select(Material).where(Material.key_word == key)
        with session_factory() as session:
            res = session.execute(query)
            result = res.scalars().first()
            return result

    @staticmethod
    def read_material(key: str, phone: str):
        query = select(User).options(selectinload(User.materials)).where(User.phone_number == phone)
        with session_factory() as session:
            user_db = session.execute(query)
            user = user_db.scalars().first()
            material_db = session.execute(select(Material).where(Material.key_word == key))
            material = material_db.scalars().first()
            if material:
                user.add_material(session, material)
            return

    @staticmethod
    def get_all_users() -> list[User]:
        query = select(User).where(User.role != UserRole.admin)
        with session_factory() as session:
            users = session.execute(query).scalars().all()
            return users

    @staticmethod
    def update_chat(chat_id, phone_number):
        query = select(User).where(User.phone_number == phone_number)
        with session_factory() as session:
            user_db = session.execute(query)
            user = user_db.scalars().first()
            user.chatId = chat_id
            session.commit()
