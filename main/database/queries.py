from sqlalchemy import and_, select, or_
from sqlalchemy.orm import selectinload


from database.database_init import engine, Base, session_factory
from database.models import User, UserMaterials, UserRole, Keyword, Mailing


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
        query = select(User).where(User.phone_number == phone)
        with session_factory() as session:
            user_db = session.execute(query)
            user = user_db.scalars().first()
            
            user.add_material(session, key)
            return

    @staticmethod
    def get_all_users() -> list[User]:
        query = select(User)
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
            return session.execute(query).scalars().first()

    @staticmethod
    def find_users_by_key(key: str):
        query_key = select(Keyword).where(Keyword.key_word == key)
        with session_factory() as session:
            key_word = session.execute(query_key).scalars().first()
            if not key_word:
                return []
            query = select(User).where(User.key_word_id == key_word.id)
            return session.execute(query).scalars().all()

    @staticmethod
    def find_users_by_region(region: str):
        query = select(User).where((User.region == region))
        with session_factory() as session:
            return session.execute(query).scalars().all()
        
        
    @staticmethod    
    def insert_mailing(title: str, content: str, mailing_type: str, keyword: str = None, region: str = None):
        
        with session_factory() as session:
            # Проверяем, что тип рассылки корректен
            if mailing_type not in ['keyword', 'region', 'all_users']:
                raise ValueError("Invalid mailing type. Must be 'keyword', 'region', or 'all_users'.")
            
            # Если тип рассылки 'keyword', то проверяем наличие ключевого слова
            if mailing_type == 'keyword' and not keyword:
                raise ValueError("Keyword is required when mailing type is 'keyword'.")
            
            # Если тип рассылки 'region', то проверяем наличие региона
            if mailing_type == 'region' and not region:
                raise ValueError("Region is required when mailing type is 'region'.")
            
            # Создаем объект рассылки
            new_mailing = Mailing(
                title=title,
                content=content,
                mailing_type=mailing_type,
                keyword=keyword,
                region=region
            )
            
            # Добавляем в сессию и сохраняем в базу данных
            session.add(new_mailing)
            session.commit()
            
            return new_mailing
            
    @staticmethod
    def get_mailings_for_user(phone: str) -> list:
        user = SyncORM.find_user_by_phone(phone)
        if not user:
            return []  # Handle case where user is not found

        # Log user keyword instead of print

        with session_factory() as session:
            try:
                query = select(Mailing).where(
                    or_(
                        Mailing.mailing_type == 'all_users',
                        and_(Mailing.mailing_type == 'keyword', Mailing.keyword == user.key_word.key_word),
                        and_(Mailing.mailing_type == 'region', Mailing.region == user.region)
                    )
                )

                mailings = session.execute(query).scalars().all()

                # Get titles of materials already sent to the user
                user_materials_query = select(UserMaterials.material_name).where(UserMaterials.user_phone == phone)
                user_materials = session.execute(user_materials_query).all()

                
                sent_titles = [user_material.material_name for user_material in user_materials]
                mailings = [mailing for mailing in mailings if mailing.title not in sent_titles]
                print('\n\n\n\n❤️❤️❤️❤️❤️❤️', sent_titles, mailings, phone, '\n\n\n\n')
                return mailings
            except:
                return None
        
    @staticmethod
    def get_mailing_text(header: str):
        with session_factory() as session:
            query = select(Mailing).where(Mailing.title == header)
            return session.execute(query).scalars().first().content