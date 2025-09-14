import os
import json
from random import choice
from datetime import datetime, timedelta
from models.database import (
    User,
    UserAdmins,
    AdminSettings,
    db_session,
)
from config import (
    JSON_FILE_ADMINS,
    ADMINS_DEFAULT,
)


def _return_admins_list() -> list:
    """
    Returns only admins which should be in database;
    Otherwise they are coaches
    """
    user_select = []
    with db_session() as conn:
        user_select = [
            i[0]
            for i 
            in conn.query(User.id).filter_by(is_admin=True).all()
        ]
    return user_select


def return_admin_preferences(id_admin: int) -> list[bool]:
    """
    Return admin preferences to the admin. Insert if empty
    """
    with db_session() as conn:
        if not(
            admin_preferences := conn.query(
                AdminSettings,
            ).filter_by(id=id_admin).all()
        ):
            conn.add(
                AdminSettings(id=id_admin)
            )
            conn.commit()
        return [
            i for i 
            in conn.query(
                AdminSettings.show_new_users,
                AdminSettings.show_responsible,
                AdminSettings.show_day_minus,
                AdminSettings.show_overdue,
                AdminSettings.show_inactive,
                AdminSettings.show_unattached,
            ).filter_by(id=id_admin).all()
        ][0]


def update_admin_preferences(id_admin, number_filter, number_old) -> None:
    number_old = False if int(number_old) else True
    match number_filter:
        case "0":
            col = "show_new_users"
        case "1":
            col = "show_responsible"
        case "2":
            col = "show_day_minus"
        case "3":
            col = "show_overdue"
        case "4":
            col = "show_inactive"
        case "5":
            col = "show_unattached"
    with db_session() as conn:
        conn.query(AdminSettings).filter_by(
                id = id_admin,
            ).update({col: number_old})
        conn.commit()


def _get_list_admins() -> list[int]:
    """
    Returns all values for the users
    """
    list_db = _return_admins_list()
    list_db.extend(ADMINS_DEFAULT)
    return list(set(list_db))


def _get_teacher_data(admin_list: list[int]) -> list:
    value_admins = []
    with db_session() as conn:
        value_admins = conn.query(
            User.id,
            User.name,
            User.surname,
        ).filter(User.id.in_(admin_list)).all()
    return value_admins


def _check_coach(value_id: int) -> bool:
    return value_id in _return_admins_list()


def _check_admin(value_id: int) -> bool:
    #TODO add here for testing
    # return False
    return value_id in _get_list_admins()


def return_user_info(value_id: int) -> str:
    user_info = []
    with db_session() as conn:
        user_info = conn.query(
            User.id,
            User.name,
            User.surname,
        ).filter_by(id=value_id).one()
    return user_info


def return_admin_selected(value_id: int):
    if id_admin := check_user_has_admin(value_id):
        return id_admin
    return choice(ADMINS_DEFAULT)


def check_date_payed_today(value_id: int):
    payment_date = []
    with db_session() as conn:

        payment_date = conn.query(User.join_date_start).filter_by(id=value_id).one()
    if not payment_date:
        return False
    if not payment_date[0]:
        return False
    # (datetime.now().month, payment_date)
    if (
        datetime.now().strftime("%Y.%m.%d") == payment_date[0]
    ):
        return True
    return False


def _update_dates(value_id: int, value_date: str = datetime.now().strftime("%Y.%m.%d")):
    with db_session() as conn:
        value_end_date = conn.query(User.join_date_end).filter_by(id=value_id).one()
        value_end_date = value_end_date[0] if value_end_date else None
        if not value_end_date:
            value_end_date = datetime.strptime(value_date, "%Y.%m.%d")
        elif (
            value_end_date and
            datetime.strptime(value_end_date, "%Y.%m.%d") < datetime.now()
        ):
            value_end_date = datetime.strptime(value_date, "%Y.%m.%d")
        else:
            value_end_date = datetime.strptime(value_end_date, "%Y.%m.%d")
        value_end_date += timedelta(days=30)
        value_end_date = datetime.strftime(value_end_date, "%Y.%m.%d")
        conn.query(User).filter_by(
            id = value_id
        ).update(
            {
                "join_date_start": value_date,
                "join_date_end": value_end_date,
            }
        )
        conn.commit()


def get_dates_payment(id_user:int) -> list:
    value_dates = [None, None]
    with db_session() as conn:
        value_dates = conn.query(
            User.join_date_start,
            User.join_date_end,
        ).filter_by(id=id_user).one()
    return value_dates


def check_user_has_admin(id_user, conn: object=None):
    #TODO remove after
    # return ADMINS_DEFAULT[0]
    value_id = None
    if not conn:
        with db_session() as conn:
            value_id = conn.query(
                UserAdmins.id_admin,
            ).filter_by(id_user=id_user).all()
    else:
        value_id = conn.query(
            UserAdmins.id_admin,
        ).filter_by(id_user=id_user).all()
    if not value_id:
        return
    return value_id[0][0]


def insert_user_admins(id_user:int, id_admin:int) -> None:
    with db_session() as conn:
        value_check = check_user_has_admin(id_user, conn)
        if not value_check:
            conn.add(
                UserAdmins(
                    id_admin = id_admin,
                    id_user = id_user,
                )
            )
        else:
            conn.query(UserAdmins).filter_by(
                   id_user = id_user,
                ).update({"id_admin": id_admin})
        conn.commit()


def insert_admins(admin_asked: int) -> bool:
    user_sel = (False,)
    with db_session() as conn:
        user_sel = conn.query(User.is_admin).filter_by(id=admin_asked).one()
    if not user_sel[0] and not admin_asked in ADMINS_DEFAULT:
        return
    if not os.path.exists(JSON_FILE_ADMINS):
        return
    value_admins = []
    with open(JSON_FILE_ADMINS, 'r') as json_admins:
        value_admins = json.load(json_admins)
    with db_session() as conn:
        for admin_json in value_admins:
            if not admin_json.get('id'):
                continue
            admin_present = \
                conn.query(User).filter_by(id=admin_json.get('id')).all()
            if not admin_present:
                conn.add(
                    User(
                        id = admin_json.get("id"),
                        name = admin_json.get("name"),
                        surname = admin_json.get("surname"),
                        username = admin_json.get("username"),
                        is_admin = True,
                        join_date_start = None,
                        join_date_end = None
                    )
                )
            elif admin_present and not admin_present[0].is_admin:
                admin_json['is_admin'] = True
                conn.query(User).filter_by(
                   id = admin_json.get('id')
                ).update(admin_json)
        conn.commit()
    return True


def select_user(user_id: int) -> object:
    with db_session() as conn:
        user_select = conn.query(User).filter_by(id=user_id).all()
    return user_select


def return_coach_students(user_id: int) -> list:
    value_return = []
    with db_session() as conn:
        if conn.query(User).filter_by(
            id=user_id,
            is_admin=True,
        ).all():
            value_return = [
                i for i 
                in conn.query(
                    User.id,
                    User.username,
                    User.join_date_start,
                    User.join_date_end,
                ).select_from(
                    User
                ).join(
                    UserAdmins,
                    UserAdmins.id_user == User.id,
                ).filter(
                    UserAdmins.id_admin == user_id
                ).all()
            ]
            # TODO add here the possibility see unattached users
    return value_return


def insert_user(chat: object):
    if not select_user(chat.id):
        with db_session() as conn:
            conn.add(
                User(
                    id = chat.id,
                    name = chat.first_name,
                    surname = chat.last_name,
                    username = chat.username,
                    is_admin = _check_coach(chat.id),
                    join_date_start = None,
                    join_date_end = None,
                )
            )   
            conn.commit()
