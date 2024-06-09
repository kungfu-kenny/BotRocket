import os
from dotenv import load_dotenv

load_dotenv()

HEADLESS = True
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

DEFAULT_PAYMENT = 'Магазин'
DEFAULT_SCHEDULE = 'Розклад'
DEFAULT_CHANNELS = 'Канали'
DEFAULT_EVENTS = 'Події'
DEFAULT_HELP = 'Допомога'
DEFAULT_SETTINGS = 'Профіль'

DEFAULT_PHOTO_NAME = 'testfile.jpg'
DEFAULT_PHOTO_USED = 'photo_2024-04-08_10-29-04.jpg'
PATH_USE = os.getcwd()
PATH_STORAGE = os.path.join(
    PATH_USE,
    "misc",
    "storage",
)
PATH_STORAGE_TMP = os.path.join(
    PATH_USE,
    "misc",
    "storage_tmp",
)
PATH_STORAGE_INVOICE = os.path.join(
    PATH_USE,
    "misc",
    "invoices",
)
PATH_PHOTOS = os.path.join(
    PATH_USE,
    "misc",
    "photos",
)
JSON_FILE_ADMINS = os.path.join(
    # PATH_STORAGE,
    PATH_USE,
    "misc",
    'admins.json',
)

ADMINS_DEFAULT = []
if (
    os.getenv("TELEGRAM_ADMIN_DEFAULT") and
    os.getenv("TELEGRAM_ADMIN_DEFAULT").isdigit()
):
    ADMINS_DEFAULT.append(int(os.getenv("TELEGRAM_ADMIN_DEFAULT")))

PATH_SCHEDULE_DEFAULT = os.getenv('TELEGRAM_SCHEDULE_NAME_DEFAULT')

CALLBACKS = {
    'cancelation': '000',
    
    'schedule': '101',
    'schedule_photo': '110',
    'schedule_delete': '100',
    
    'channel_change': '200',
    
    'buy_water_big': '300',
    'buy_water_small': '301',
    'hire_gi': '310',
    'buy_one_pass': '320',
    
    'event_next': '400',
    
    'send_invoice': '500',
    'send_invoice_file': '501',
    
    'receive_invoice': '600',
    'receive_invoice_file': '601',

    'admin_next': '700',
    'admin_select': '701',
    'admin_attach': '702',
}
PAYMENT_CHARACTERISTICS = {
    'buy_water_big': {
        "price": 2500,
        "description": 'Якщо ви забули на тренування водичку, '
        'у вас є можливіть придбати велику пляшку води вартістю 25 грн.',
        "photo": 'photo_2024-04-08_14-44-38.jpg',
        "payload": 'Оплата великої пляшки води',
    },
    'buy_water_small': {
        "price": 2000,
        "description": 'Якщо ви забули на тренування водичку, '
        'у вас є можливіть придбати маленьку пляшечку води вартістю 20 грн.',
        "photo": 'photo_2024-04-08_14-44-38.jpg',
        "payload": 'Оплата малої пляшки води',
    },
    'hire_gi': {
        "price": 20000,
        "description": 'Ви маєте можливість взяти на прокат Гі '
        'якщо у вас воно з тих чи інших причин відсутнє. '
        'Вартість цієї послуги становить 200 гривень',
        "photo": 'photo_2024-04-08_14-51-40.jpg',
        "payload": 'Оплата прокату ГІ',
    },
    'buy_one_pass': {
        "price": 50000,
        "description": 'Ви маєте можливість оплатити разове тренування. '
        'Вартість цієї послуги становить 500 гривень',
        "photo": 'photo_2024-04-08_14-51-40.jpg',
        "payload": "Оплата разового тренування",
    }
}
DICT_MESSAGES = {
    'cancelation': 'Скасувати',
    'url': 'Посилання',
    'confirm_no': 'Ні',
    'confirm_yes': 'Так',
    'confirm_admin_schedule': 'Замінити розклад',
    'confirm_admin_send_screen': 'Надіслати скрін про оплату',
    'confirm_admin_schedule_change': 'Замінити розклад',
    'confirm_admin_update': 'Оновили дані адмінів в файлі',
    'confirmation_send': 'Хочете надіслати скрін про оплату?',
    'confirmation_send_user': 'Ми надішлемо ваш скрін тренеру згодом',
    'confirmation_schedule': 'Ви впевнені що збираєтесь замінити розклад?',
    'confirmation_schedule_delete': 'Ви впевнені що збираєтесь видалити старі розклади?',
    'confirmation_success_user': 'Адмін підтвердив ваш платіж',
    'confirmation_success_admin': 'Успішно підтверджено',
    'confirmation_already': 'Платіж вже було передчасно підтверджено',
    'confirmation_file_error': 'Інвойси приймаються лише у вигляді фото або .pdf файлів.'
        ' Дякуємо за розуміння',
    'confirmation': "Ви точно впевнені?",
    'name': "Назва",
    'description': "Опис",
    'buy_water_big': "Велика пляшка води, 1.0л",
    'buy_water_small': "Маленька пляшка води, 0.5л",
    'hire_gi': "Прокат Гі",
    'buy_one_pass': "Разове тренування",
    'payment_start': 'Тут ви можете здійснити оплати за разові послуги.'
        ' Зверніть увагу що оплата абоненту здійснюється окремо',
    'start': '**Вітаємо!**\nЦей бот призначено аби полегшити роботу із спортзалом'
        ' на всіх можливих рівнях. Приємного користування',
    'confirmation_db': 'В базі даних вже присутній запис за поточний місяць.'
        ' Якщо ви оплатили наперед, то узгодьте це з тренером'
        ' або надішліть наступного календарного місяця. Дякуємо за увагу',
    'admin_selection': 'Для роботи з оплатою, будь ласка оберіть свого тренера',
    'admin_selected': 'Ви успішно прикріпилися до тренера. Дякуємо за ініціативу',
    'admin_settings': 'Так як ви тренер, вам це функціонал непотрібен',
    'settings_basic': 'Ваш профіль',
    'help_basic': 'Цей блок призначений для допомоги орієнтуванню в боті. Великий документ готується',
    'selection_admin_schedule_payment': "Виберіть необхідне",
    'user_attach_coach': 'Ця функція доступна лише за умови ви змогли додатися до тренера.'
      'Будь ласка, оберіть вашого коуча і перешліть скрін знову',
}
DICT_ERRORS = {
    'file_send': "Ми не можемо використати цей файл як новий розклад, оскільки в нього не той формат",
    'admin_schedule': 'Ми маємо проблему з отриманням розкладу',
    'admin_schedule_user': 'Ми маємо проблему з отриманням розкладу. Адмін розгляне це згодом',
    'admin_filename': 'У нас є проблема з отриманням розкладу. Розгляньте це будь-ласка',
    'update_admins': 'Будь ласка введіть тренерів',
    'no_admins': "Нажаль, у нас є проблеми із введенням тренерів, адмін скоро це узгодить",
}
DICT_CAPTIONS_SCHEDULE = {
    True: 'Лови актуальний розклад школи',
    False: 'Лови актуальний розклад школи. Зверни увагу що розклад може змінитися',
    "Mistake": 'Нажаль, у нас проблеми з відображенням актуального розкладу',
}

CHANNEL_JITSU = {
    'name': 'Jitsu',
    'photo': 'channels4_profile.jpg',
    'description': 'Ютуб канал з детальними розборами для новачків, інтерв\'ю та інших цікавинок.',
    'url': 'https://www.youtube.com/@jitsuukraine',
}
CHANNEL_ONLYFANS = {
    'name': 'Тигровий OnlyFans',
    'photo': 'photo_2024-04-08_01-49-52.jpg',
    'description': 'Відеоуровки, записані з радикально-патріархального крила Ракети.'
    ' Заходьте щоб бути в курсі занять.',
    'url': 'https://t.me/senoklyfans',
}
CHANNEL_PROJECT_GUARD = {
    'name': 'Project Guard',
    'photo': 'photo_2024-04-08_01-05-50.jpg',
    'description': 'Найбільший канал із сутичками, відеоуроками від всіма улюбленого Юри Гарда.',
    'url': 'https://t.me/projectguard',
}
LIST_CHANNELS = [
    CHANNEL_JITSU,
    CHANNEL_ONLYFANS,
    CHANNEL_PROJECT_GUARD,
]
admin_notification = \
    lambda x, y: f'Користувач {x} здійснив оплату абонементу, а адмін {y} це узгодив'
schedule_admin_change = lambda x: \
    f'Адміністратор {x} замінив розклад. Візьміть це на розгляд'