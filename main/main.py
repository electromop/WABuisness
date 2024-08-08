import os.path
import random

from whatsapp_chatbot_python import GreenAPIBot, Notification

from database.models import UserRole
from YaDisk import YaDisk
from config_reader import config
from database.queries import SyncORM
from states import States

bot = GreenAPIBot(config.id_instance.get_secret_value(), config.token_whatsapp.get_secret_value())
disk = YaDisk(token=config.token_ya.get_secret_value())
menu = ("Я могу рассĸазать тебе информацию по теме:\n\n"
        "1. Срочно и важно\n"
        "2. Информация для нового сотрудника\n"
        "3. Инфопак\n"
        "4. Работа с программами\n"
        "5. Памятка мерчандайзера\n"
        "6. База знаний\n"
        "7. Контакты\n"
        "8. KPI и мотивация\n"
        "9. FAQ / ЧаВо (часто задаваемые вопросы)\n"
        "*Выбери из ĸаĸого раздела ты хотел бы узнать информацию напиши мне номер/цифру этого раздела в чат*\n\n"
        "Ты всегда можешь вернуться ĸ выбору раздела написав мне \"Меню\"")

unknown = ("Не совсем тебя понимаю."
           "\n✅ - Если ты изучил материал, то напиши \"Изучено\""
           "\n🔍 - Если ты хочешь выбрать другую тему и материал, то напиши \"Меню\""
           "\n❓ - Если ты запутался, то напиши \"Помощь\"")

no_files = ("К сожалению, материалы по этой теме еще не добавлены, но я делаю всё возможное, чтобы ĸаĸ можно сĸорее "
            "тебе о них рассĸазать. ✨🤝🏻\n*Выбери другой раздел и напиши в чат номер/цифру, соответствующий этому "
            "разделу.*")

downloading = ["Загружаю для тебя данные....", "Не уходи далеĸо! Загружаем данные...", "Почти готово! Дай нам немного "
                                                                                       "времени на загрузĸу..."]


@bot.router.message(command="start")
def start_command(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.set_state(sender, States.KEY_WORD.value)
    notification.answer("Привет, коллега! 🥳\nМеня зовут Хеллпер, я чат-бот помощник.\nЗдесь ты найдешь последние "
                        "новости, обновления и изменения, а также полезные подсказки и рекомендации, которые помогут "
                        "тебе максимально эффективно взаимодействовать с проектом. 📚📂\nДавай вместе достигать новых "
                        "высот!\nНачнем наше взаимодействие прямо сейчас!\n*Введи ĸлючевое слово, чтобы увидеть, "
                        "что я умею.* 🎯\n*Ключевое слово ты можешь узнать у своего руĸоводителя")


@bot.router.message(text_message=["Помощь", "помощь", "Помощь.", "помощь.", "\"Помощь\"", "\"помощь\"", "ПОМОЩЬ"])
def help_command(notification: Notification):
    sender = notification.sender
    notification.state_manager.update_state(sender, States.HELP.value)
    notification.answer("Давай я помогу тебе сориентироваться:"
                        "\n\n✅ - Если ты изучил материал, то напиши \"Изучено\""
                        "\n\n🔍 - Если ты хочешь выбрать другую тему и материал, то напиши \"Меню\""
                        "\n\n❗ Если возниĸли сложности с работой чат-бота или ты заметил, что он не работает "
                        "ĸорреĸтно, "
                        "то пришли сĸрин на почту learn.merch@merch.ancor.ru.\n\n"
                        "Тех поддержĸа работает с понедельниĸа по пятницу с 9 до 18 мсĸ"
                        )


@bot.router.message(text_message=["Привет", "привет", "\"Привет\"", "\"привет\"", "ПРИВЕТ", "Привет.", "привет."])
def greeting(notification: Notification):
    sender = notification.sender
    key = SyncORM.find_user_by_phone(sender.split("@")[0])
    if not key:
        notification.state_manager.set_state(sender, States.KEY_WORD.value)
        notification.answer("Привет, коллега! 🥳\nМеня зовут Хеллпер, я чат-бот помощник.\nЗдесь ты найдешь последние "
                        "новости, обновления и изменения, а также полезные подсказки и рекомендации, которые помогут "
                        "тебе максимально эффективно взаимодействовать с проектом. 📚📂\nДавай вместе достигать новых "
                        "высот!\nНачнем наше взаимодействие прямо сейчас!\n*Введи ĸлючевое слово, чтобы увидеть, "
                        "что я умею.* 🎯\n*Ключевое слово ты можешь узнать у своего руĸоводителя")
        return
    notification.state_manager.update_state(sender, States.CATEGORY.value)
    notification.answer(menu)


@bot.router.message(text_message=["Меню", "меню", "\"Меню\"", "\"меню\"", "МЕНЮ", "меню.", "Меню."])
def menu_handler(notification: Notification):
    sender = notification.sender
    key = SyncORM.find_user_by_phone(sender.split("@")[0])
    if not key:
        notification.state_manager.set_state(sender, States.KEY_WORD.value)
        notification.answer("Привет, коллега! 🥳\nМеня зовут Хеллпер, я чат-бот помощник.\nЗдесь ты найдешь последние "
                        "новости, обновления и изменения, а также полезные подсказки и рекомендации, которые помогут "
                        "тебе максимально эффективно взаимодействовать с проектом. 📚📂\nДавай вместе достигать новых "
                        "высот!\nНачнем наше взаимодействие прямо сейчас!\n*Введи ĸлючевое слово, чтобы увидеть, "
                        "что я умею.* 🎯\n*Ключевое слово ты можешь узнать у своего руĸоводителя")
        return
    notification.state_manager.update_state(sender, States.CATEGORY.value)
    notification.answer(menu)


# @bot.router.message(command="search")
# def search(notification: Notification) -> None:
#     sender = notification.sender
#     notification.state_manager.update_state(sender, States.SEARCH.value)
#     notification.answer("Введите ключевое слово для материала")


# @bot.router.message(command="files")
# def get_all_files(notification: Notification):
#     sender = notification.sender
#     key = SyncORM.find_user_by_phone(sender.split("@")[0])
#     if not key:
#         notification.answer("Пройдите авторизацию, чтобы пользоваться данной командой")
#         return
#     files = set([i["name"] for i in disk.get_files() if i.get("type") != "dir"])
#     notification.answer(("{:s}\n" * len(files)).format(*files)[:-1:])


@bot.router.message(command="send")
def send_message(notification: Notification):
    sender = notification.sender
    user = SyncORM.find_user_by_phone(sender.split("@")[0])
    if user.role != UserRole.admin:
        notification.answer("Вы не администратор")
        return
    notification.state_manager.update_state(sender, States.TYPE.value)
    notification.answer("Выберите тип рассылки:\n"
                        "1. Всем\n\n"
                        "2. По ключевому слову\n\n"
                        "3. По указанному региону")


# @bot.router.message(command="feedback")
# def feedback_command(notification: Notification):
#     sender = notification.sender
#     key = SyncORM.find_user_by_phone(sender.split("@")[0])
#     if not key:
#         notification.answer("Пройдите авторизацию, чтобы пользоваться данной командой")
#         return
#     notification.state_manager.update_state(sender, States.FEEDBACK.value)
#     notification.answer("Введите отзыв")


@bot.router.message(state=States.HELP.value)
def handle_help(notification: Notification):
    notification.answer(unknown)

@bot.router.message(state=States.TYPE.value)
def handle_mailing_type(notification: Notification):
    mailing_type = notification.message_text
    sender = notification.sender
    notification.state_manager.update_state_data(sender, {"mailing_type": mailing_type})
    
    if mailing_type == "1" or mailing_type.lower() == "всем":
        notification.answer("Введите заголовок уведомления")
        notification.state_manager.update_state_data(sender, {"mailing_type": 'all_users'})
        notification.state_manager.update_state(sender, States.SEND.value)

    elif mailing_type == "2" or mailing_type.lower() == "по ключевому слову":
        notification.answer("Введите ключевое слово")
        notification.state_manager.update_state_data(sender, {"mailing_type": 'keyword'})
        notification.state_manager.update_state(sender, States.PARAMETER.value)
    
    elif mailing_type == "3" or mailing_type.lower() == "по указанному региону":
        notification.answer("Введите регион")
        notification.state_manager.update_state_data(sender, {"mailing_type": 'region'})
        notification.state_manager.update_state(sender, States.PARAMETER.value)
        
    else:
        notification.answer(unknown)
        notification.state_manager.update_state(sender, States.TYPE.value)
        
    
    
@bot.router.message(state=States.PARAMETER.value)
def handle_mailing_parameter(notification: Notification):
    #сохраняем ключевое слово или регион для рассылки
    print('Дошли до сюда')
    mailing_type = notification.state_manager.get_state_data(notification.sender)["mailing_type"]
    sender = notification.sender
    if mailing_type != 'all_users':
        notification.state_manager.update_state_data(sender, {mailing_type: notification.message_text})
    
    notification.answer("Введите заголовок уведомления")
    notification.state_manager.update_state(sender, States.SEND.value)

@bot.router.message(state=States.SEND.value)
def send_message_handler(notification: Notification):
    title = notification.message_text
    sender = notification.sender
    notification.state_manager.update_state_data(sender, {"title": title})
    notification.answer("Введите текст уведомления")
    notification.state_manager.update_state(sender, States.SEND_TEXT.value)



@bot.router.message(state=States.SEND_TEXT.value)
def send_text(notification: Notification):
    sender = notification.sender
    text = notification.message_text
    print('❤️❤️❤️', notification.state_manager.get_state_data(sender))
    mailing_type = notification.state_manager.get_state_data(sender)["mailing_type"]
    title = notification.state_manager.get_state_data(sender)["title"]

    keyword = None
    region = None
    
    if mailing_type == 'all_users':
        users = SyncORM.get_all_users()
    elif mailing_type == 'keyword':
        keyword = notification.state_manager.get_state_data(sender)["keyword"]
        users = SyncORM.find_users_by_key(keyword)
    elif mailing_type == 'region':
        region = notification.state_manager.get_state_data(sender)["region"]
        users = SyncORM.find_users_by_region(region)
    
    print('❤️❤️❤️', users)
    for user in users:
        mailing_text = f"{title}\n{text}\n\n*Не забудь зайти в раздел \"Срочно и важно\" и указать уведомление изученным*"
        notification.api.sending.sendMessage(user.chat_id, mailing_text)
        
    notification.answer("Уведомление отправлено")
    notification.state_manager.update_state(sender, States.CATEGORY.value)
    SyncORM.insert_mailing(title, text, mailing_type, keyword, region)


@bot.router.message(state=States.CATEGORY.value)
def choose_category(notification: Notification):
    sender = notification.sender
    match notification.message_text:
        case "1" | "Срочно и важно":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/1. Срочно и важно")
            mailings = SyncORM.get_mailings_for_user(sender.split("@")[0])
            
            if len(res) == 0 and not mailings:
                notification.answer(no_files)
                notification.answer(menu)
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "Что именно тебе хотелось бы изучить? 🤔\n" + "".join(
                ["{:d}. {:s}\n".format(i + 1, file[0]) for
                 i, file in enumerate(
                    files)])[:-1] + ("\n*Выбери тему и напиши мне номер/цифру этой темы в чат*\n\nТы всегда можешь "
                                     "вернуться ĸ выбору темы написав мне \"Меню\"")
            
            
            if mailings:
                formatted_string += "\n\nПоследние уведомления:\n"
                last_index = len(files)
                for i, mailing in enumerate(mailings):
                    formatted_string += f'{last_index + i + 1}. {mailing.title}\n'
                    
                files.extend([[mailing.title, "Рассылка"] for mailing in mailings])
            
            notification.answer(formatted_string)

            notification.state_manager.update_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
            
        case "2" | "Информация для нового сотрудника":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/2. Информация для "
                               "нового сотрудника")
            if len(res) == 0:
                notification.answer(no_files)
                notification.answer(menu)
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "Что именно тебе хотелось бы изучить? 🤔\n" + "".join(
                ["{:d}. {:s}\n".format(i + 1, file[0]) for
                 i, file in enumerate(
                    files)])[
                                                                            :-1] + (
                                   "\n*Выбери тему и напиши мне номер/цифру этой темы в чат*\n\nТы всегда можешь "
                                   "вернуться ĸ выбору темы написав мне \"Меню\"")
            notification.answer(formatted_string)

            notification.state_manager.update_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "3" | "Инфопак":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/3. Инфопак")
            if len(res) == 0:
                notification.answer(no_files)
                notification.answer(menu)
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "Что именно тебе хотелось бы изучить? 🤔\n" + "".join(
                ["{:d}. {:s}\n".format(i + 1, file[0]) for
                 i, file in enumerate(
                    files)])[
                                                                            :-1] + (
                                   "\n*Выбери тему и напиши мне номер/цифру этой темы в чат*\n\nТы всегда можешь "
                                   "вернуться ĸ выбору темы написав мне \"Меню\"")
            notification.answer(formatted_string)

            notification.state_manager.update_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "4" | "Работа с программами":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/4. Работа с "
                               "программами")
            if len(res) == 0:
                notification.answer(no_files)
                notification.answer(menu)
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "Что именно тебе хотелось бы изучить? 🤔\n" + "".join(
                ["{:d}. {:s}\n".format(i + 1, file[0]) for
                 i, file in enumerate(
                    files)])[
                                                                            :-1] + (
                                   "\n*Выбери тему и напиши мне номер/цифру этой темы в чат*\n\nТы всегда можешь "
                                   "вернуться ĸ выбору темы написав мне \"Меню\"")
            notification.answer(formatted_string)

            notification.state_manager.update_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "5" | "Памятка мерчандайзера":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/5. Памятка "
                               "мерчандайзера")
            if len(res) == 0:
                notification.answer(no_files)
                notification.answer(menu)
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "Что именно тебе хотелось бы изучить? 🤔\n" + "".join(
                ["{:d}. {:s}\n".format(i + 1, file[0]) for
                 i, file in enumerate(
                    files)])[
                                                                            :-1] + (
                                   "\n*Выбери тему и напиши мне номер/цифру этой темы в чат*\n\nТы всегда можешь "
                                   "вернуться ĸ выбору темы написав мне \"Меню\"")
            notification.answer(formatted_string)

            notification.state_manager.update_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "6" | "База знаний":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/6. База знаний")
            if len(res) == 0:
                notification.answer(no_files)
                notification.answer(menu)
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "Что именно тебе хотелось бы изучить? 🤔\n" + "".join(
                ["{:d}. {:s}\n".format(i + 1, file[0]) for
                 i, file in enumerate(
                    files)])[
                                                                            :-1] + (
                                   "\n*Выбери тему и напиши мне номер/цифру этой темы в чат*\n\nТы всегда можешь "
                                   "вернуться ĸ выбору темы написав мне \"Меню\"")
            notification.answer(formatted_string)

            notification.state_manager.update_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "7" | "Контакты":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/7. Контакты")
            if len(res) == 0:
                notification.answer(no_files)
                notification.answer(menu)
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "Что именно тебе хотелось бы изучить? 🤔\n" + "".join(
                ["{:d}. {:s}\n".format(i + 1, file[0]) for
                 i, file in enumerate(
                    files)])[
                                                                            :-1] + (
                                   "\n*Выбери тему и напиши мне номер/цифру этой темы в чат*\n\nТы всегда можешь "
                                   "вернуться ĸ выбору темы написав мне \"Меню\"")
            notification.answer(formatted_string)

            notification.state_manager.update_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "8" | "KPI и мотивация":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/8. KPI и мотивация")
            if len(res) == 0:
                notification.answer(no_files)
                notification.answer(menu)
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "Что именно тебе хотелось бы изучить? 🤔\n" + "".join(
                ["{:d}. {:s}\n".format(i + 1, file[0]) for
                 i, file in enumerate(
                    files)])[
                                                                            :-1] + (
                                   "\n*Выбери тему и напиши мне номер/цифру этой темы в чат*\n\nТы всегда можешь "
                                   "вернуться ĸ выбору темы написав мне \"Меню\"")
            notification.answer(formatted_string)

            notification.state_manager.update_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "9" | "FAQ / ЧаВо (часто задаваемые вопросы)":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/9. FAQ_ЧаВо ("
                               "частые вопросы)")
            if len(res) == 0:
                notification.answer(no_files)
                notification.answer(menu)
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "Что именно тебе хотелось бы изучить? 🤔\n" + "".join(
                ["{:d}. {:s}\n".format(i + 1, file[0]) for
                 i, file in enumerate(
                    files)])[
                                                                            :-1] + (
                                   "\n*Выбери тему и напиши мне номер/цифру этой темы в чат*\n\nТы всегда можешь "
                                   "вернуться ĸ выбору темы написав мне \"Меню\"")
            notification.answer(formatted_string)

            notification.state_manager.update_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case _:
            notification.answer(unknown)
            return


@bot.router.message(state=States.READY.value)
def ready_handler(notification: Notification):
    sender = notification.sender
    phone = sender.split("@")[0]
    key_mat = notification.state_manager.get_state_data(sender)["material"]
    
    
    if notification.message_text.lower() == "изучено":
        SyncORM.read_material(key_mat, phone)
        notification.answer("Отлично! Рад был поделиться с тобой этой информацией!\n"
                            "🔍 -  Если ты хочешь изучить и другие темы, то напиши в чат \"Меню\"\n"
                            "Если тебе потребуется ĸаĸая-нибудь информация, то я всегда на связи\n"
                            "Пиши мне в любое время. Успехов в работе!♥")
        notification.state_manager.update_state(sender, States.CATEGORY.value)
        return
    notification.answer(unknown)


@bot.router.message(state=States.SEARCH.value)
def search_handler(notification: Notification) -> None:
    sender = notification.sender
    key_word = SyncORM.find_user_by_phone(sender.split("@")[0])
    if not key_word:
        notification.answer("Пройдите авторизацию, чтобы пользоваться данной командой")
        return
    material = SyncORM.find_material(notification.message_text.strip().lower())
    if material:
        name = material.name
    else:
        notification.answer("Файл не найден")
        return
    files = [(i["name"], i["path"]) for i in disk.get_files()]
    is_send = False
    curr_path = os.path.dirname(__file__)
    prj_dir = os.path.join(curr_path)
    for file in files:
        if name in file[0]:
            try:
                notification.answer(random.choice(downloading))
                disk.download_file(file[1], f"{prj_dir}/files/{file[0]}")
            except Exception:
                notification.answer("Что то пошло не так")
                return
            notification.answer_with_file(f"{prj_dir}/files/{file[0]}", file[0])
            notification.answer("✅ *После ознаĸомления с материалом, напиши в чат \"Изучено\"*")
            notification.state_manager.update_state(sender, States.READY.value)
            notification.state_manager.update_state_data(sender, {"material": notification.message_text})
            os.remove(f"{prj_dir}/files/{file[0]}")
            is_send = True
    if not is_send:
        notification.answer("Файл не найден")


@bot.router.message(state=States.FEEDBACK.value)
def give_feedback(notification: Notification):
    text = notification.message_text
    sender = notification.sender
    SyncORM.new_feedback(text, sender.split("@")[0])
    notification.answer("Ваш отзыв записан")
    notification.state_manager.update_state(sender, States.KEY_WORD.value)


@bot.router.message(state=States.DOWNLOAD.value)
def handel_download_file(notification: Notification):
    sender = notification.sender
    files = notification.state_manager.get_state_data(sender)["category"]
    try:
        option = int(notification.message_text)
    except Exception:
        notification.answer("🔢 Введите число/цифру")
        return
    if option > len(files) and files[option - 1][1] != "Рассылка":
        notification.answer("❌ Такого варианта нет, выбери цифру/число из доступных вариантов.\n\n*В случае, если тебе нужно изучить другой раздел напиши \"Меню\"*")
        return
    elif files[option - 1][1] == "Рассылка":
        mailing_title = files[option - 1][0]
        print(mailing_title)
        files[option - 1][0] = 'Рассылка - ' + mailing_title
        mailing_text = SyncORM.get_mailing_text(mailing_title)
        notification.answer(f"Заголовок: {mailing_title}\n\n{mailing_text}")
    else:    
        curr_path = os.path.dirname(__file__)
        prj_dir = os.path.join(curr_path)
        try:
            notification.answer(random.choice(downloading))
            disk.download_file(files[option - 1][1], f"{prj_dir}/files/{files[option - 1][0]}")
        except Exception:
            notification.answer("Что то пошло не так")
        notification.answer_with_file(f"{prj_dir}/files/{files[option - 1][0]}", files[option - 1][0])
        os.remove(f"{prj_dir}/files/{files[option - 1][0]}")
        
    notification.answer("✅ *После ознаĸомления с материалом, напиши в чат \"Изучено\"*")
    notification.state_manager.update_state(sender, States.READY.value)
    print("material key value", files[option - 1][0])
    
    notification.state_manager.update_state_data(sender, {"material": files[option - 1][0]})


@bot.router.message(state=States.KEY_WORD.value)
def key_word_handler(notification: Notification) -> None:
    sender = notification.sender
    key_word = notification.message_text.lower().strip()
    if key_word := SyncORM.check_key(key_word):
        chat = notification.chat
        phone = sender.split("@")[0]
        SyncORM.insert_user(key_word_id=key_word.id, chat_id=chat, phone_number=phone)
        notification.state_manager.update_state(sender, States.CATEGORY.value)
        notification.state_manager.update_state_data(sender, {"key_word": key_word})
        notification.answer(menu)
    else:
        notification.answer("Ключевое слово не подходит.\nПроверь ĸорреĸтность ввода и попробуй повторно.🧐\n\nЕсли "
                            "ты не знаешь или забыл ĸлючевое слово, то узнать его можно у своего руĸоводителя")


if __name__ == "__main__":
    print('ok')
    bot.run_forever()

