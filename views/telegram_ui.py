from aiogram.types import (
    Message,
    CallbackQuery,
    ContentType,
    InputMediaPhoto,
    LabeledPrice,
    PreCheckoutQuery,
)

from views.telegram_usage import dp, bot
from views.telegram_buttons import (
    return_channels,
    return_caption_tournament,
    return_events_next,
    return_menu_basic,
    get_caption_invoice,
    return_payment_basic,
    return_proper_description,
    return_confirm_schedule_change,
    return_schedule_or_payment_admins,
    return_admins_select_list,
    return_settings_user,
)
from models.db_functions import (
    _check_admin,
    insert_user,
    insert_admins,
    check_date_payed_today,
    _get_list_admins,
    return_admin_selected,
    _update_dates,
    _return_admins_list,
    _check_coach,
    _get_teacher_data,
    check_user_has_admin,
    insert_user_admins,
    get_dates_payment,
    return_user_info,
)
from utilities.selenium_utilities import get_new_events
from utilities.file_utilities import (
    delete_old_schedules,
    get_schedule_file,
    get_schedule_photo,
    get_photo_path,
    add_new_invoice,
    add_new_invoice_file,
    add_new_schedule_file,
    check_schedule_file_pdf,
    check_schedule_file_photo,
    # _remove_tmp_file,
    check_invoice_file_already,
)
from views.filters import (
    CheckReplyMenu,
    CheckUsePayment,
    CheckCancelChoice,
    CheckConfirmSchedule,
    CheckConfirmSchedulePhoto,
    CheckConfirmScheduleDelete,
    CheckContinueChannels,
    CheckNextEvent,
    CheckSendInvoice,
    CheckSendInvoiceFile,
    CheckAdminConfirm,
    CheckAdminConfirmFile,
    CheckAdminSelectNext,
    CheckGetUserAdmin,
    CheckAttachCoach,
)
from config import (
    admin_notification,
    schedule_admin_change,
    ADMINS_DEFAULT,
    DEFAULT_HELP,
    DEFAULT_EVENTS,
    DEFAULT_PAYMENT,
    DEFAULT_SCHEDULE,
    DEFAULT_CHANNELS,
    DEFAULT_SETTINGS,
    CALLBACKS,
    DICT_ERRORS,
    DICT_MESSAGES,
    DEFAULT_PHOTO_NAME,
    DEFAULT_PHOTO_USED,
    PAYMENT_CHARACTERISTICS,
    DICT_CAPTIONS_SCHEDULE,
    PAYMENT_PROVIDER_TOKEN,
)


@dp.message_handler(commands=["start"])
async def send_welcome(message: Message):
    insert_user(message.chat)
    await message.reply(
        DICT_MESSAGES['start'],
        reply_markup=return_menu_basic(),
    )
    if not check_user_has_admin(message.chat.id):
        await send_coaches(message)


async def send_coaches(message):
    admins_db = _return_admins_list()
    if admins_db and not message.chat.id in admins_db:
        await bot.send_message(
            message.chat.id,
            DICT_MESSAGES['admin_selection'],
            reply_markup=return_admins_select_list(
                _get_teacher_data(admins_db),
                message.chat.id,
            ),
        )
    elif not admins_db:
        for admin_default in ADMINS_DEFAULT:
            await bot.send_message(
                admin_default,
                DICT_ERRORS['update_admins'],
            )


@dp.message_handler(commands=['admin_update'])
async def update_admins(message: Message):
    if insert_admins(message.chat.id):
        await message.reply(
            DICT_MESSAGES['confirm_admin_update'],
            parse_mode='Markdown',
            reply_markup=return_menu_basic(),
        )


@dp.message_handler(commands=['settings'])
async def produce_user_settings(message: Message):
    insert_user(message.chat)
    if _check_coach(message.chat.id):
        await bot.send_message(
            message.chat.id,
            DICT_MESSAGES['admin_settings'],
        )
    else: 
        id_coach_presence = check_user_has_admin(message.chat.id)
        if id_coach_presence:
            id_coach_presence_list = _get_teacher_data([id_coach_presence,])
            id_coach_presence_list = id_coach_presence_list[0]
        else:
            id_coach_presence_list = []
        date_start, date_expired = get_dates_payment(message.chat.id)
        await bot.send_message(
            message.chat.id,
            DICT_MESSAGES['settings_basic'],
            reply_markup=return_settings_user(
                id_coach_presence_list,
                date_start,
                date_expired,
            ),
        )


@dp.message_handler(commands=['events'])
async def send_events(message: Message):
    new_events = get_new_events()
    value_use, markup = return_events_next(new_events)
    if new_events['error']:
        for admin in _get_list_admins():
            await bot.send_message(
                admin,
                DICT_ERRORS['admin_schedule'],
                parse_mode='Markdown',
                reply_markup=return_menu_basic(),
            )
        await message.reply(
            DICT_ERRORS['admin_schedule_user'],
            parse_mode='Markdown',
            reply_markup=return_menu_basic(),
        )
    else:
        await bot.send_photo(
                message.chat.id,
                value_use['photo'],
                caption = return_caption_tournament(value_use),
                reply_markup=markup,
                parse_mode="Markdown",
            )


@dp.message_handler(commands=['payment'])
async def send_payment(message: Message):
    #TODO continue from here to change values
    await bot.send_message(
        message.chat.id,
        DICT_MESSAGES['payment_start'],
        parse_mode='Markdown',
        reply_markup=return_payment_basic(),
    )


@dp.message_handler(content_types=[ContentType.DOCUMENT])
async def check_working_new_scheduler(message: Message):
    document_name = message.document.file_name
    if is_coach:=_check_coach(message.chat.id):
        if (
            not check_schedule_file_pdf(document_name)
            and not check_schedule_file_photo(document_name)
        ):
            await bot.send_message(
                message.chat.id,
                DICT_ERRORS["file_send"],
                reply_to_message_id=message.message_id,
                reply_markup=return_menu_basic(),
            )
            return
        await bot.send_message(
            message.chat.id,
            DICT_MESSAGES["confirmation_schedule"],
            reply_to_message_id=message.message_id,
            reply_markup=return_confirm_schedule_change(),
        )
    elif not is_coach and _check_admin(message.chat.id):
        if (
            not check_schedule_file_pdf(document_name)
            and not check_schedule_file_photo(document_name)
        ):
            await bot.send_message(
                message.chat.id,
                DICT_ERRORS["file_send"],
                reply_to_message_id=message.message_id,
                reply_markup=return_menu_basic(),
            )
            return
        await bot.send_message(
            message.chat.id,
            DICT_MESSAGES['selection_admin_schedule_payment'],
            reply_to_message_id=message.message_id,
            reply_markup=return_schedule_or_payment_admins(
                CALLBACKS["send_invoice_file"],
                CALLBACKS["schedule"],
            ),
        )
    elif check_user_has_admin(message.chat.id):
        await bot.send_message(
            message.chat.id,
            DICT_MESSAGES["confirmation_send"],
            reply_to_message_id=message.message_id,
            reply_markup=return_confirm_schedule_change(
                CALLBACKS["send_invoice_file"]
            ),
        )
    else:
        admins_db = _return_admins_list()
        await bot.send_message(
            message.chat.id,
            DICT_MESSAGES['user_attach_coach'],
            reply_to_message_id=message.message_id,
            reply_markup=return_admins_select_list(
                _get_teacher_data(admins_db),
                message.chat.id,
            ),
        )


@dp.message_handler(content_types=[ContentType.PHOTO])
async def send_schedule_payment_check(message: Message):
    if is_coach:=_check_coach(message.chat.id):
        await bot.send_message(
            message.chat.id,
            DICT_MESSAGES["confirmation_schedule"],
            reply_to_message_id=message.message_id,
            reply_markup=return_confirm_schedule_change(CALLBACKS["schedule_photo"]),
        )
    elif not is_coach and _check_admin(message.chat.id):
        await bot.send_message(
            message.chat.id,
            DICT_MESSAGES['selection_admin_schedule_payment'],
            reply_to_message_id=message.message_id,
            reply_markup=return_schedule_or_payment_admins(
                CALLBACKS["send_invoice"],
                CALLBACKS["schedule_photo"],
            ),
        )
    elif check_user_has_admin(message.chat.id):
        await bot.send_message(
            message.chat.id,
            DICT_MESSAGES["confirmation_send"],
            reply_to_message_id=message.message_id,
            reply_markup=return_confirm_schedule_change(CALLBACKS["send_invoice"]),
        )
    else:
        admins_db = _return_admins_list()
        await bot.send_message(
            message.chat.id,
            DICT_MESSAGES['user_attach_coach'],
            reply_to_message_id=message.message_id,
            reply_markup=return_admins_select_list(
                _get_teacher_data(admins_db),
                message.chat.id,
            ),
        )


@dp.message_handler(commands=["schedule"])
async def send_schedule(message: Message):
    file_name, file_original = get_schedule_file()
    if file_name:
        with open(file_name, "rb") as file_schedule:
            if check_schedule_file_pdf(file_name):
                await bot.send_document(
                    message.chat.id,
                    file_schedule,
                    caption=DICT_CAPTIONS_SCHEDULE[file_original],
                )
            elif check_schedule_file_photo(file_name):
                await bot.send_photo(
                    message.chat.id,
                    file_schedule,
                    caption=DICT_CAPTIONS_SCHEDULE[file_original],
                )
    else:
        await bot.send_message(
            message.chat.id,
            DICT_CAPTIONS_SCHEDULE["Mistake"],
            reply_to_message_id=message.message_id,
            reply_markup=return_menu_basic(),
        )
        for admin in _get_list_admins():
            await bot.send_message(
                admin,
                DICT_ERRORS['admin_filename'],
                parse_mode='Markdown',
                reply_markup=return_menu_basic(),
            )


@dp.message_handler(commands=["schedule_delete"])
async def produce_delete_old_schedules(message: Message):
    if _check_admin(message.chat.id):
        await bot.send_message(
            message.chat.id,
            DICT_MESSAGES["confirmation_schedule_delete"],
            reply_to_message_id=message.message_id,
            reply_markup=return_confirm_schedule_change(
                CALLBACKS["schedule_delete"],
            ),
        )


@dp.message_handler(commands=["channels"])
async def send_channels(message: Message):
    dict_use, reply_markups = return_channels()
    photo_used = p if (p := dict_use.get("photo")) else DEFAULT_PHOTO_USED
    with open(get_photo_path(photo_used), "rb") as file_photo:
        await bot.send_photo(
            message.chat.id,
            file_photo,
            caption=return_proper_description(
                dict_use["name"],
                dict_use["description"],
            ),
            reply_markup=reply_markups,
            parse_mode="Markdown",
        )


@dp.message_handler(commands=['help','instruction'])
async def produce_help(message: Message):
    await bot.send_message(
        message.chat.id,
        DICT_MESSAGES['help_basic'],
    )


@dp.callback_query_handler(CheckConfirmSchedule())
async def produce_schedule_change(call: CallbackQuery) -> None:
    document_name = call.message.reply_to_message.document.file_name
    file_info = await bot.get_file(call.message.reply_to_message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    full_path = add_new_schedule_file(document_name)
    with open(full_path, "wb") as new_file:
        new_file.write(downloaded_file.getvalue())
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None,
    )
    x = return_user_info(call.message.chat.id)
    x = ' '.join(z.strip() for z in x[1:] if z) + f'(ID: {x[0]})'
    for i in _get_list_admins():
        await bot.send_message(
            i,
            schedule_admin_change(x),
        )


@dp.callback_query_handler(CheckConfirmScheduleDelete())
async def produce_schedule_delete(call: CallbackQuery) -> None:
    if _check_admin(call.message.chat.id):
        delete_old_schedules()
        await bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None,
        )


@dp.callback_query_handler(CheckGetUserAdmin())
async def produce_user_admin_connection(call: CallbackQuery) -> None:
    _, id_user, id_admin = call.data.split('_')
    id_user, id_admin = int(id_user), int(id_admin)
    insert_user_admins(id_user, id_admin)
    await bot.edit_message_text(
        DICT_MESSAGES['admin_selected'],
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None,
    )


@dp.callback_query_handler(CheckCancelChoice())
async def produce_cancel_choice(call: CallbackQuery) -> None:
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None,
    )


@dp.callback_query_handler(CheckConfirmSchedulePhoto())
async def produce_schedule_change_photo(call: CallbackQuery) -> None:
    full_path = add_new_schedule_file(get_schedule_photo(DEFAULT_PHOTO_NAME))
    await call.message.reply_to_message.photo[-1].download(destination_file=full_path)
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None,
    )
    x = return_user_info(call.message.chat.id)
    x = ' '.join(z.strip() for z in x[1:] if z) + f'(ID: {x[0]})'
    for i in _get_list_admins():
        await bot.send_message(
            i,
            schedule_admin_change(x),
        )


@dp.callback_query_handler(CheckContinueChannels())
async def produce_change_channel(call: CallbackQuery) -> None:
    index_use = int(call.data.split("_")[1])
    dict_use, reply_markups = return_channels(index_use)
    photo_used = p if (p := dict_use.get("photo")) else DEFAULT_PHOTO_USED
    with open(get_photo_path(photo_used), "rb") as file_photo:
        new_photo = InputMediaPhoto(file_photo)
        await bot.edit_message_media(
            chat_id=call.message.chat.id,
            media=new_photo,
            message_id=call.message.message_id,
        )
        await bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=reply_markups,
            caption=return_proper_description(
                dict_use["name"],
                dict_use["description"],
            ),
            parse_mode="Markdown",
        )


@dp.callback_query_handler(CheckNextEvent())
async def produce_next_event(call: CallbackQuery) -> None:
    index_use = int(call.data.split("_")[1])
    new_events = get_new_events()
    value_use, markup = return_events_next(new_events, index_use)
    new_photo = InputMediaPhoto(value_use['photo'])
    await bot.edit_message_media(
        chat_id=call.message.chat.id,
        media=new_photo,
        message_id=call.message.message_id,
    )
    await bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption = return_caption_tournament(value_use),
        reply_markup=markup,
        parse_mode="Markdown",
    )


@dp.callback_query_handler(CheckAdminSelectNext())
async def produce_next_event(call: CallbackQuery) -> None:
    index_use = int(call.data.split("_")[1])
    admins_db = _return_admins_list()
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=return_admins_select_list(
            _get_teacher_data(admins_db),
            call.message.chat.id,
            index_use,
        ),
    )


@dp.callback_query_handler(CheckAdminConfirm())
async def produce_admin_confirm_invoice(call: CallbackQuery) -> None:
    """Produce confirmation for the admin of the pictures"""
    value_id_user = int(call.data.split('_')[-1])
    if check_date_payed_today(value_id_user):#check_invoice_file_already(value_id_user):
        await bot.edit_message_caption(
            call.message.chat.id,
            call.message.message_id,
            caption=DICT_MESSAGES['confirmation_already'],
            reply_markup=None
        )
        await bot.send_message(
            value_id_user,
            DICT_MESSAGES['confirmation_db'],
            reply_markup=return_menu_basic(),
        )
    else:
        full_path = add_new_invoice(
            value_id_user,
            call.message.chat.id,
            False
        )
        await call.message.photo[-1].download(
            destination_file=full_path
        )
        await bot.edit_message_caption(
            call.message.chat.id,
            call.message.message_id,
            caption=DICT_MESSAGES['confirmation_success_admin'],
            reply_markup=None
        )
        await bot.send_message(
            value_id_user,
            DICT_MESSAGES['confirmation_success_user'],
            reply_markup=return_menu_basic(),
        )
        _update_dates(value_id_user)
        x = return_user_info(value_id_user)
        x = ' '.join(z.strip() for z in x[1:] if z) + f'(ID: {x[0]})'
        y = return_user_info(call.message.chat.id)
        y = ' '.join(z.strip() for z in y[1:] if z) + f'(ID: {y[0]})'
        for i in _get_list_admins():
            await bot.send_message(
                i,
                admin_notification(x, y),
                reply_markup=return_menu_basic(),
            )


@dp.callback_query_handler(CheckAdminConfirmFile())
async def produce_admin_confirm_invoice_file(call: CallbackQuery) -> None:
    """Produce confirmation for the admin of the files"""
    value_id_user = int(call.data.split('_')[-1])
    if check_date_payed_today(value_id_user):#check_invoice_file_already(value_id_user):
        await bot.edit_message_caption(
            call.message.chat.id,
            call.message.message_id,
            caption=DICT_MESSAGES['confirmation_already'],
            reply_markup=None
        )
        await bot.send_message(
            value_id_user,
            DICT_MESSAGES['confirmation_db'],
            reply_markup=return_menu_basic(),
        )
    else:
        full_path = add_new_invoice_file(
            value_id_user,
            call.message.chat.id,
        )
        file_info = await bot.get_file(call.message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        with open(full_path, "wb") as new_file:
            new_file.write(downloaded_file.getvalue())
        await bot.edit_message_caption(
            call.message.chat.id,
            call.message.message_id,
            caption=DICT_MESSAGES['confirmation_success_admin'],
            reply_markup=None
        )
        await bot.send_message(
            value_id_user,
            DICT_MESSAGES['confirmation_success_user'],
            reply_markup=return_menu_basic(),
        )
        _update_dates(value_id_user)
        x = return_user_info(value_id_user)
        x = ' '.join(z.strip() for z in x[1:] if z) + f'(ID: {x[0]})'
        y = return_user_info(call.message.chat.id)
        y = ' '.join(z.strip() for z in y[1:] if z) + f'(ID: {y[0]})'
        for i in _get_list_admins():
            await bot.send_message(
                i,
                admin_notification(x, y),
                reply_markup=return_menu_basic(),
            )


@dp.callback_query_handler(CheckSendInvoice())
async def produce_sending_invoice_admin(call: CallbackQuery) -> None:
    admin_send = return_admin_selected(call.message.chat.id)
    await bot.edit_message_text(
        DICT_MESSAGES["confirmation_send_user"],
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None,
    )
    await bot.send_photo(
        chat_id=admin_send,
        photo=call.message.reply_to_message.photo[-1].file_id,
        caption=get_caption_invoice(call.message.chat),
        reply_markup=return_confirm_schedule_change(
            f'{CALLBACKS["receive_invoice"]}_{call.message.chat.id}',
        ),
        parse_mode="Markdown",
    )


@dp.callback_query_handler(CheckSendInvoiceFile())
async def produce_sending_invoice_admin_file(call: CallbackQuery) -> None:
    """Function for the sending for the admin invoice to check"""
    admin_send = return_admin_selected(call.message.chat.id)
    await bot.edit_message_text(
        DICT_MESSAGES["confirmation_send_user"],
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None,
    )
    if not check_schedule_file_pdf(
        call.message.reply_to_message.document.file_name
    ):
        await bot.send_message(
            call.message.chat.id,
            DICT_MESSAGES['confirmation_file_error'],
            reply_markup=return_menu_basic(),
        )
    else:
        await bot.send_document(
            admin_send,
            call.message.reply_to_message.document.file_id,
            caption=get_caption_invoice(call.message.chat),
            reply_markup=return_confirm_schedule_change(
                f'{CALLBACKS["receive_invoice_file"]}_{call.message.chat.id}',
            ),
            parse_mode="Markdown",
        )
 

@dp.callback_query_handler(CheckAttachCoach())
async def produce_user_coach_attachment(call: CallbackQuery) -> None:
    await send_coaches(call.message)


@dp.callback_query_handler(CheckUsePayment())
async def produce_send_invoice(call: CallbackQuery) -> None:
    #TODO continue working from here
    if call.data == CALLBACKS['hire_gi']:
        call_data = 'hire_gi'
    elif call.data == CALLBACKS['buy_water_big']:
        call_data = 'buy_water_big'
    elif call.data == CALLBACKS['buy_water_small']:
        call_data = 'buy_water_small'
    elif call.data == CALLBACKS['buy_one_pass']:
        call_data = 'buy_one_pass'
    await bot.send_invoice(
        call.message.chat.id,
        title=DICT_MESSAGES[call_data],
        description=PAYMENT_CHARACTERISTICS[call_data]['description'],
        provider_token = PAYMENT_PROVIDER_TOKEN,
        currency='uah',
        # photo_url='https://telegra.ph/file/d08ff863531f10bf2ea4b.jpg',
        photo_height=512,
        photo_width=512,
        photo_size=512,
        prices=[
            LabeledPrice(
                label=DICT_MESSAGES[call_data],
                amount=PAYMENT_CHARACTERISTICS[call_data]['price']
            ),
        ],
        payload=PAYMENT_CHARACTERISTICS[call_data]['payload'],
    )


@dp.message_handler(CheckReplyMenu())
async def develop_menu_reaction(message: Message):
    if message.text == DEFAULT_SCHEDULE:
        await send_schedule(message)

    if message.text == DEFAULT_CHANNELS:
        await send_channels(message)

    if message.text == DEFAULT_PAYMENT:
        await send_payment(message)

    if message.text == DEFAULT_EVENTS:
        await send_events(message)

    if message.text == DEFAULT_SETTINGS:
        await produce_user_settings(message)

    if message.text == DEFAULT_HELP:
        await produce_help(message)


# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    print(payment_info)
    print('333333333333333333333333333333333333333333333')
    print('333333333333333333333333333333333333333333333')
    print('333333333333333333333333333333333333333333333')