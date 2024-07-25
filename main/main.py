import os.path

from whatsapp_chatbot_python import GreenAPIBot, Notification

import states
from YaDisk import YaDisk
from config_reader import config
from database.queries import SyncORM
from states import States


bot = GreenAPIBot(config.id_instance.get_secret_value(), config.token_whatsapp.get_secret_value())
disk = YaDisk(token=config.token_ya.get_secret_value())


@bot.router.message(command="start")
def start_command(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.set_state(sender, States.KEY_WORD.value)
    notification.answer("Введите ключевое слово")


@bot.router.message(command="search")
def search(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.update_state(sender, States.SEARCH.value)
    notification.answer("Введите ключевое слово для материала")


@bot.router.message(command="files")
def get_all_files(notification: Notification):
    sender = notification.sender
    key = notification.state_manager.get_state_data(sender)["key_word"]
    if not key:
        notification.answer("Пройдите авторизацию, чтобы пользоваться данной командой")
        return

    files = set([i["name"] for i in disk.get_files() if i.get("type") != "dir"])
    notification.answer(("{:s}\n" * len(files)).format(*files)[:-1:])


@bot.router.message(command="send")
def send_message(notification: Notification):
    sender = notification.sender
    notification.state_manager.update_state(sender, States.SEND.value)
    notification.answer("Введите уведомление")


@bot.router.message(state=States.SEND.value)
def send_message_handler(notification: Notification):
    users = SyncORM.get_all_users()
    for user in users:
        notification.api.sending.sendMessage(user.chat_id, notification.message_text)


@bot.router.message(state=States.CATEGORY.value)
def choose_category(notification: Notification):
    sender = notification.sender
    match notification.message_text:
        case "1" | "Срочно и важно":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/1. Срочно и важно")
            if len(res) == 0:
                notification.answer("Материалы не найдены")
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "".join(["{:d}. {:s}\n".format(i + 1, file[0]) for i, file in enumerate(files)])[:-1]
            notification.answer(formatted_string)
            notification.answer("Введите номер материала, чтобы просмотреть его")
            notification.state_manager.set_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "2" | "Информация для нового сотрудника":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/2. Информация для "
                               "нового сотрудника")
            if len(res) == 0:
                notification.answer("Материалы не найдены")
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "".join(["{:d}. {:s}\n".format(i + 1, file[0]) for i, file in enumerate(files)])[:-1]
            notification.answer(formatted_string)
            notification.answer("Введите номер материала, чтобы просмотреть его")
            notification.state_manager.set_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "3" | "Инфопак":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/3. Инфопак")
            if len(res) == 0:
                notification.answer("Материалы не найдены")
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "".join(["{:d}. {:s}\n".format(i + 1, file[0]) for i, file in enumerate(files)])[:-1]
            notification.answer(formatted_string)
            notification.answer("Введите номер материала, чтобы просмотреть его")
            notification.state_manager.set_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "4" | "Работа с программами":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/4. Работа с "
                               "программами")
            if len(res) == 0:
                notification.answer("Материалы не найдены")
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "".join(["{:d}. {:s}\n".format(i + 1, file[0]) for i, file in enumerate(files)])[:-1]
            notification.answer(formatted_string)
            notification.answer("Введите номер материала, чтобы просмотреть его")
            notification.state_manager.set_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "5" | "Памятка мерчандайзера":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/5. Памятка "
                               "мерчандайзера")
            if len(res) == 0:
                notification.answer("Материалы не найдены")
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "".join(["{:d}. {:s}\n".format(i + 1, file[0]) for i, file in enumerate(files)])[:-1]
            notification.answer(formatted_string)
            notification.answer("Введите номер материала, чтобы просмотреть его")
            notification.state_manager.set_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "6" | "База знаний":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/6. База знаний")
            if len(res) == 0:
                notification.answer("Материалы не найдены")
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "".join(["{:d}. {:s}\n".format(i + 1, file[0]) for i, file in enumerate(files)])[:-1]
            notification.answer(formatted_string)
            notification.answer("Введите номер материала, чтобы просмотреть его")
            notification.state_manager.set_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "7" | "Контакты":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/7. Контакты")
            if len(res) == 0:
                notification.answer("Материалы не найдены")
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "".join(["{:d}. {:s}\n".format(i + 1, file[0]) for i, file in enumerate(files)])[:-1]
            notification.answer(formatted_string)
            notification.answer("Введите номер материала, чтобы просмотреть его")
            notification.state_manager.set_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "8" | "KPI и мотивация":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/8. KPI и мотивация")
            if len(res) == 0:
                notification.answer("Материалы не найдены")
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "".join(["{:d}. {:s}\n".format(i + 1, file[0]) for i, file in enumerate(files)])[:-1]
            notification.answer(formatted_string)
            notification.answer("Введите номер материала, чтобы просмотреть его")
            notification.state_manager.set_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case "9" | "FAQ / ЧаВо (часто задаваемые вопросы)":
            res = disk.listdir("disk:/Загрузки/Обучающие материалы для мерчандайзера-новичка/Раздел/9. FAQ_ЧаВо ("
                               "частые вопросы)")
            if len(res) == 0:
                notification.answer("Материалы не найдены")
                return
            files = [(i["name"], i["path"]) for i in res]
            formatted_string = "".join(["{:d}. {:s}\n".format(i + 1, file[0]) for i, file in enumerate(files)])[:-1]
            notification.answer(formatted_string)
            notification.answer("Введите номер материала, чтобы просмотреть его")
            notification.state_manager.set_state_data(sender, {"category": files})
            notification.state_manager.update_state(sender, States.DOWNLOAD.value)
            return
        case _:
            notification.answer("Я вас не понимаю выберите одну из категорий")
            notification.answer("Введите номер раздела:\n\n"
                                "1. Срочно и важно\n"
                                "2. Информация для нового сотрудника\n"
                                "3. Инфопак\n"
                                "4. Работа с программами\n"
                                "5. Памятка мерчандайзера\n"
                                "6. База знаний\n"
                                "7. Контакты\n"
                                "8. KPI и мотивация\n"
                                "9. FAQ / ЧаВо (часто задаваемые вопросы)")
            return


@bot.router.message(state=States.READY.value)
def ready_handler(notification: Notification):
    sender = notification.sender
    phone = sender.split("@")[0]
    key_mat = notification.state_manager.get_state_data(sender)["material"]
    if notification.message_text.lower() == "ознакомлен":
        SyncORM.read_material(key_mat, phone)
        notification.answer("Информация записана")
        return
    notification.answer("Как ознакомитесь с материалом, напишите в чат \"Ознакомлен\"")


@bot.router.message(state=States.SEARCH.value)
def search_handler(notification: Notification) -> None:
    sender = notification.sender
    key = notification.state_manager.get_state_data(sender)["key_word"]
    material = SyncORM.find_material(notification.message_text)
    if material:
        name = material.name
    else:
        notification.answer("Файл не найден")
        return
    if not key:
        notification.answer("Пройдите авторизацию, чтобы пользоваться данной командой")
        return
    files = [(i["name"], i["path"]) for i in disk.get_files()]
    is_send = False
    curr_path = os.path.dirname(__file__)
    prj_dir = os.path.join(curr_path)
    for file in files:
        if name in file[0]:
            try:
                notification.answer("Подождите, идет загрузка...")
                disk.download_file(file[1], f"{prj_dir}/files/{file[0]}")
            except Exception:
                notification.answer("Что то пошло не так")
                return
            notification.answer_with_file(f"{prj_dir}/files/{file[0]}", file[0])
            notification.answer("Как ознакомитесь с материалом, напишите в чат \"Ознакомлен\"")

            notification.state_manager.update_state(sender, States.READY.value)
            notification.state_manager.set_state_data(sender, {"material": notification.message_text})
            os.remove(f"{prj_dir}/files/{file[0]}")
            is_send = True
    if not is_send:
        notification.answer("Файл не найден")


@bot.router.message(command="feedback")
def feedback_command(notification: Notification):
    sender = notification.sender
    key = notification.state_manager.get_state_data(sender)["key_word"]
    if not key:
        notification.answer("Пройдите авторизацию, чтобы пользоваться данной командой")
        return
    notification.state_manager.update_state(sender, States.FEEDBACK.value)
    notification.answer("Введите отзыв")


@bot.router.message(state=States.FEEDBACK.value)
def give_feedback(notification: Notification):
    text = notification.message_text
    sender = notification.sender
    SyncORM.new_feedback(text, sender.split("@")[0])
    notification.answer("Ваш отзыв записан")


@bot.router.message(state=States.DOWNLOAD.value)
def handel_download_file(notification: Notification):
    sender = notification.sender
    files = notification.state_manager.get_state_data(sender)["category"]
    try:
        option = int(notification.message_text)
    except Exception:
        notification.answer("Введите число")
        return
    if option >= len(files):
        notification.answer("Такого варианта нет")
        return
    curr_path = os.path.dirname(__file__)
    prj_dir = os.path.join(curr_path)
    try:
        notification.answer("Подождите, идет загрузка...")
        disk.download_file(files[option - 1][1], f"{prj_dir}/files/{files[option - 1][0]}")
        os.remove(f"{prj_dir}/files/{files[option - 1][0]}")
    except Exception:
        notification.answer("Что то пошло не так")
    notification.answer_with_file(f"{prj_dir}/files/{files[option - 1][0]}", files[option - 1][0])
    notification.answer("Как ознакомитесь с материалом, напишите в чат \"Ознакомлен\"")
    notification.state_manager.update_state(sender, States.READY.value)


@bot.router.message(state=States.KEY_WORD.value)
def key_word_handler(notification: Notification) -> None:
    sender = notification.sender
    key_word = notification.message_text
    key_word = SyncORM.check_key(key_word)
    if key_word:
        chat = notification.chat
        phone = sender.split("@")[0]
        SyncORM.insert_user(key_word_id=key_word.id,chat_id=chat, phone_number=phone)
        notification.state_manager.update_state(sender, States.CATEGORY.value)
        notification.state_manager.set_state_data(sender, {"key_word": key_word})
        notification.answer("Введите номер раздела:\n\n"
                            "1. Срочно и важно\n"
                            "2. Информация для нового сотрудника\n"
                            "3. Инфопак\n"
                            "4. Работа с программами\n"
                            "5. Памятка мерчандайзера\n"
                            "6. База знаний\n"
                            "7. Контакты\n"
                            "8. KPI и мотивация\n"
                            "9. FAQ / ЧаВо (часто задаваемые вопросы)")
    else:
        notification.answer("Ключевое слово не найдено")


if __name__ == "__main__":
    bot.run_forever()
