from aiogram.dispatcher.filters import Filter
from aiogram.types import Message, CallbackQuery

from config import (
    CALLBACKS,
    DEFAULT_HELP,
    DEFAULT_PAYMENT,
    DEFAULT_CHANNELS,
    DEFAULT_SCHEDULE,
    DEFAULT_EVENTS,
    DEFAULT_SETTINGS,
)


class CheckConfirmSchedule(Filter):
    key = "is_confirmed_schedule"

    async def check(self, call: CallbackQuery) -> bool:
        return call.data == CALLBACKS["schedule"]


class CheckConfirmScheduleDelete(Filter):
    key = "is_confirmed_schedule_delete"

    async def check(self, call: CallbackQuery) -> bool:
        return call.data == CALLBACKS["schedule_delete"]


class CheckCancelChoice(Filter):
    key = "is_cancel_choice"

    async def check(self, call: CallbackQuery) -> bool:
        return call.data == CALLBACKS["cancelation"]


class CheckConfirmSchedulePhoto(Filter):
    key = "is_confirmed_schedule_photo"

    async def check(self, call: CallbackQuery) -> bool:
        return call.data == CALLBACKS["schedule_photo"]


class CheckContinueChannels(Filter):
    key = "is_continue_channels_list"

    async def check(self, call: CallbackQuery) -> bool:
        call_use = call.data.split("_")
        return len(call_use) == 2 and call_use[0] == CALLBACKS["channel_change"]


class CheckNextEvent(Filter):
    key = "is_next_event"

    async def check(self, call: CallbackQuery) -> bool:
        call_use = call.data.split("_")
        return len(call_use) == 2 and call_use[0] == CALLBACKS["event_next"]


class CheckGetUserAdmin(Filter):
    key = "is_user_selected_admin"

    async def check(self, call: CallbackQuery) -> bool:
        call_use = call.data.split("_")
        return len(call_use) == 3 and call_use[0] == CALLBACKS["admin_select"]


class CheckUsePayment(Filter):
    key = "is_user_wants_buy"

    async def check(self, call: CallbackQuery) -> bool:
        return call.data in [
            CALLBACKS["hire_gi"],
            CALLBACKS["buy_water_big"],
            CALLBACKS["buy_water_small"],
            CALLBACKS["buy_one_pass"],
        ]


class CheckAttachCoach(Filter):
    key = "is_user_wants_attach_coach"

    async def check(self, call: CallbackQuery) -> bool:
        return call.data == CALLBACKS["admin_attach"]


class CheckSendInvoice(Filter):
    key = "is_user_wants_send_invoice"

    async def check(self, call: CallbackQuery) -> bool:
        return call.data == CALLBACKS["send_invoice"]


class CheckSendInvoiceFile(Filter):
    key = "is_user_wants_send_invoice_file"

    async def check(self, call: CallbackQuery) -> bool:
        return call.data == CALLBACKS["send_invoice_file"]


class CheckAdminConfirm(Filter):
    key = "is_admin_confirmed_invoice"

    async def check(self, call: CallbackQuery) -> bool:
        call_use = call.data.split("_")
        return len(call_use) == 2 and call_use[0] == CALLBACKS["receive_invoice"]


class CheckAdminConfirmFile(Filter):
    key = "is_admin_confirmed_invoice_file"

    async def check(self, call: CallbackQuery) -> bool:
        call_use = call.data.split("_")
        return len(call_use) == 2 and call_use[0] == CALLBACKS["receive_invoice_file"]


class CheckAdminShowPerson(Filter):
    key = "is_admin_show_student"

    async def check(self, call: CallbackQuery) -> bool:
        call_use = call.data.split("_")
        return len(call_use) == 2 and call_use[0] == CALLBACKS["student_show"]


class CheckAdminSelectNext(Filter):
    key = "is_user_clicked_next_admin"

    async def check(self, call: CallbackQuery) -> bool:
        call_use = call.data.split("_")
        return len(call_use) == 2 and call_use[0] == CALLBACKS["admin_next"]


class CheckReplyMenu(Filter):
    key = "is_user_inserted"

    async def check(self, message: Message) -> bool:
        return message.text.strip() in [
            DEFAULT_HELP,
            DEFAULT_PAYMENT,
            DEFAULT_CHANNELS,
            DEFAULT_SCHEDULE,
            DEFAULT_EVENTS,
            DEFAULT_SETTINGS,
        ]
