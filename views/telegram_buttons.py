from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from datetime import datetime
from utilities.file_utilities import make_chunks
from config import (
    CALLBACKS,
    DICT_MESSAGES,
    LIST_CHANNELS,
    DEFAULT_HELP,
    DEFAULT_EVENTS,
    DEFAULT_PAYMENT,
    DEFAULT_SCHEDULE,
    DEFAULT_CHANNELS,
    DEFAULT_SETTINGS,
)


def get_caption_invoice(chat: object) -> str:
    value_start = (
        "Ми отримали скріншот про оплату. Нижче будуть вказані данні про транзакцію:"
    )
    value_id = f"*ID:* {chat.id}" if chat.id else ""
    value_name_full = (
        f"*Ім'я:* {full_name}"
        if (full_name := ' '.join(i.strip() for i in [chat.first_name, chat.last_name] if i))
        and any(i.strip() for i in [chat.first_name, chat.last_name])
        else "Не написав ім'я"
    )
    value_username = f"*Профіль:* @{chat.username}" if chat.username else ""
    value_date = f'*Дата відправлення:* {datetime.now().strftime("%Y-%m-%d")}'
    value_confirm = "Ви *підтверджуєте* що отримали гроші?"
    return "\n".join(
        f
        for f in [
            value_start,
            value_id,
            value_name_full,
            value_username,
            value_date,
            value_confirm,
        ]
        if f
    )


def return_caption_tournament(value_dict: dict[str, str]) -> str:
    return (
        f'*Назва: {value_dict["name"]}*\n'
        f'*Дата проведення: {value_dict["date"]}*\n'
        f'*Локація: {value_dict["location"]}*\n'
    )


def return_proper_description(name: str, description: str) -> str:
    string_name = f"*{DICT_MESSAGES['name']}: {name}*"
    string_description = f"*{DICT_MESSAGES['description']}:*\n{description}"
    return "\n".join(
        [
            string_name,
            string_description,
        ]
    )


def return_events_next(new_events: dict, index_use: int = 0):
    value_prev = index_use - 1
    value_next = index_use + 1
    new_events = new_events["lists"]
    if not new_events:
        return {}, None
    if value_next > len(new_events) - 1:
        value_next = value_next % len(new_events)
    if value_prev < 0:
        value_prev = value_prev % len(new_events)
    value_used = new_events[index_use]
    return value_used, InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=DICT_MESSAGES["url"],
                    url=value_used["url"],
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=f'{CALLBACKS["event_next"]}_{value_prev}',
                ),
                InlineKeyboardButton(
                    text=f"{index_use + 1} / {len(new_events)}",
                    callback_data="None",
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=f'{CALLBACKS["event_next"]}_{value_next}',
                ),
            ],
        ]
    )


def return_channels(index_use: int = 0) -> tuple[str, object]:
    value_prev = index_use - 1
    value_next = index_use + 1
    if value_next > len(LIST_CHANNELS) - 1:
        value_next = value_next % len(LIST_CHANNELS)
    if value_prev < 0:
        value_prev = value_prev % len(LIST_CHANNELS)
    value_used = LIST_CHANNELS[index_use]
    return value_used, InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=DICT_MESSAGES["url"],
                    url=value_used["url"],
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=f'{CALLBACKS["channel_change"]}_{value_prev}',
                ),
                InlineKeyboardButton(
                    text=f"{index_use + 1} / {len(LIST_CHANNELS)}",
                    callback_data="None",
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=f'{CALLBACKS["channel_change"]}_{value_next}',
                ),
            ],
        ]
    )


def return_confirm_schedule_change(
    callback_confirm: str = CALLBACKS["schedule"],
) -> object:
    return InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=DICT_MESSAGES["confirm_yes"],
                    callback_data=callback_confirm,
                ),
                InlineKeyboardButton(
                    text=DICT_MESSAGES["confirm_no"],
                    callback_data=CALLBACKS["cancelation"],
                ),
            ]
        ],
    )


def return_schedule_or_payment_admins(callback_invoice, callback_schedule):
    return InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=DICT_MESSAGES['confirm_admin_send_screen'],
                    callback_data=callback_invoice,
                ),
            ],
            [
                InlineKeyboardButton(
                    text=DICT_MESSAGES['confirm_admin_schedule_change'],
                    callback_data=callback_schedule,
                ),
            ],
            [
                InlineKeyboardButton(
                    text=DICT_MESSAGES['cancelation'],
                    callback_data=CALLBACKS["cancelation"],
                ),
            ],
        ]
    )


def return_settings_user(
    id_coach_presence_list: list,
    date_start: str,
    date_expired: str,
) -> object:
    inline_keyboard = []
    if id_coach_presence_list:
        _, coach_name, coach_last = id_coach_presence_list
        inline_keyboard.extend(
            [
                [
                    InlineKeyboardButton(
                        'Ваш тренер:',
                        callback_data="None",
                    ),
                    InlineKeyboardButton(
                        ' '.join(
                            i.strip()
                            for i
                            in [
                                coach_name,
                                coach_last,
                            ]
                            if i
                        ),
                        callback_data='None',
                    ),
                ],
                [
                    InlineKeyboardButton(
                        'Змінити Тренера',
                        callback_data=CALLBACKS['admin_attach'],
                    ),
                ],
            ]
        )
    else:
        inline_keyboard.extend(
            [
                [
                    InlineKeyboardButton(
                        'Вказати Тренера',
                        callback_data=CALLBACKS['admin_attach'],
                    ),
                ],
            ]
        )
    inline_keyboard.extend(
        [
            [
                InlineKeyboardButton(
                    'Дата оплати:',
                    callback_data="None",
                ),
                InlineKeyboardButton(
                    date_start if date_start else 'Не оплачено',
                    callback_data="None",
                ),
            ],
            [
                InlineKeyboardButton(
                    'Закінчується:',
                    callback_data="None",
                ),
                InlineKeyboardButton(
                    date_expired if date_expired else 'Не оплачено',
                    callback_data="None",
                ),
            ]
        ]
    )
    return InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=inline_keyboard,
    )


def return_admins_select_list(
    list_admins: list[str],
    user_asked: int,
    index_use: int = 0,
) -> object:
    list_admins = make_chunks(list_admins)
    value_prev = index_use - 1
    value_next = index_use + 1
    if value_next > len(list_admins) - 1:
        value_next = value_next % len(list_admins)
    if value_prev < 0:
        value_prev = value_prev % len(list_admins)
    list_buttons = [
        [
            InlineKeyboardButton(
                text=f"{surname} {name}",
                callback_data=f"{CALLBACKS['admin_select']}_{user_asked}_{id_admin}",
            )
        ]
        for (
            id_admin,
            name,
            surname,
        )
        in list_admins[index_use]
    ]
    if len(list_admins) > 1:
        list_buttons.append(
        [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=f'{CALLBACKS["admin_next"]}_{value_prev}',
                ),
                InlineKeyboardButton(
                    text=f"{index_use + 1} / {len(list_admins)}",
                    callback_data="None",
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=f'{CALLBACKS["admin_next"]}_{value_next}',
                ),
            ]
        )
    return InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=list_buttons,
    )


def return_payment_basic() -> object:
    return InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=DICT_MESSAGES["buy_water_small"],
                    callback_data=CALLBACKS["buy_water_small"],
                ),
            ],
            [
                InlineKeyboardButton(
                    text=DICT_MESSAGES["buy_water_big"],
                    callback_data=CALLBACKS["buy_water_big"],
                ),
            ],
            [
                InlineKeyboardButton(
                    text=DICT_MESSAGES["hire_gi"],
                    callback_data=CALLBACKS["hire_gi"],
                ),
            ],
            [
                InlineKeyboardButton(
                    text=DICT_MESSAGES["buy_one_pass"],
                    callback_data=CALLBACKS["buy_one_pass"],
                ),
            ],
        ],
    )


def return_menu_basic() -> object:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(DEFAULT_SCHEDULE),
                InlineKeyboardButton(DEFAULT_PAYMENT),
            ],
            [
                InlineKeyboardButton(DEFAULT_CHANNELS),
                InlineKeyboardButton(DEFAULT_EVENTS),
            ],
            [
                InlineKeyboardButton(DEFAULT_HELP),
                InlineKeyboardButton(DEFAULT_SETTINGS),
            ],
        ],
        one_time_keyboard=False,
    )