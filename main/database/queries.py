from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload


from database.database_init import engine, Base, session_factory
from database.models import User, UserRole, Keyword


class SyncORM:

    @staticmethod
    def create_table():
        #Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    @staticmethod
    def check_key(key: str):
        query = select(Keyword).where(Keyword.key_word == key)
        with session_factory() as session:
            res = session.execute(query)
            result = res.scalars().first()
            return result

    # @staticmethod
    # def find_material(key: str):
    #     query = select(Material).where(Material.key_word == key)
    #     with session_factory() as session:
    #         res = session.execute(query)
    #         result = res.scalars().first()
    #         return result

    @staticmethod
    def read_material(key: str, phone: str):
        query = select(User).options(selectinload(User.materials)).where(User.phone_number == phone)
        with session_factory() as session:
            user_db = session.execute(query)
            user = user_db.scalars().first()
            # material_db = session.execute(select(Material).where(or_(Material.name == key)))
            # material = material_db.scalars().first()
            # if material:
            user.add_material(session, key)
            return

    @staticmethod
    def get_all_users() -> list[User]:
        query = select(User).where(User.role != UserRole.admin)
        with session_factory() as session:
            users = session.execute(query).scalars().all()
            return users

    @staticmethod
    def update_chat(chat_id: str, id: int):
        query = select(User).where(User.id == id)
        with session_factory() as session:
            user_db = session.execute(query)
            user = user_db.scalars().first()
            user.chatId = chat_id
            session.commit()

    @staticmethod
    def update_phone(phone: str, id: int):
        query = select(User).where(User.id == id)
        with session_factory() as session:
            user_db = session.execute(query)
            user = user_db.scalars().first()
            user.phone_number = phone
            session.commit()

    @staticmethod
    def insert_user(key_word_id: int, phone_number: str, chat_id: str):
        query = select(User).where(User.phone_number == phone_number)
        new_user = User(key_word_id=key_word_id, role=UserRole.user, phone_number=phone_number, chat_id=chat_id)
        with session_factory() as session:
            user = session.execute(query).scalars().first()
            if user:
                return
            session.add(new_user)
            session.commit()

    # @staticmethod
    # def new_feedback(text: str, phone: str):
    #     new_feedback = Question(question=text, phone_number=phone)
    #     with session_factory() as session:
    #         session.add(new_feedback)
    #         session.commit()

    @staticmethod
    def find_user_by_phone(phone: str):
        query = select(User).options(selectinload(User.key_word)).where(User.phone_number == phone)
        with session_factory() as session:
            user = session.execute(query).scalars().first()
            return user

    @staticmethod
    def find_users_by_key(key: str):
        query_key = select(Keyword).where(Keyword.key_word == key)
        with session_factory() as session:
            key_word = session.execute(query_key).scalars().first()
            if not key_word:
                return []
            query = select(User).where((User.key_word_id == key_word.id) & (User.role != UserRole.admin))
            users = session.execute(query).scalars().all()
            return users

    @staticmethod
    def find_users_by_region(region: str):
        query = select(User).where((User.region == region) & (User.role != UserRole.admin))
        with session_factory() as session:
            users = session.execute(query).scalars().all()
            return users
        