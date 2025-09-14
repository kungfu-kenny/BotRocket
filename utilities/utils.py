from datetime import datetime, timedelta


def get_simple_date(element_date: str):
    if element_date:
        return datetime.strptime(element_date, "%Y.%m.%d")
    return datetime.now() + timedelta(days=30)


def produce_sorting_by_date_by_name(list_users: list) -> list:
    return sorted(
        list_users,
        key=lambda x: (get_simple_date(x[3]), x[1]),
        reverse=True
    )


def produce_username_empty(list_users: list, index_username: int = 1) -> list:
    #TODO add here the new 
    for list_user in list_users:
        if not list_user[index_username]:
            list_user[index_username] = "Не вказано"
    return list_users


def provide_dates(date_old: str) -> str:
    if not date_old:
        return "⚪️"
    date_provided = datetime.strptime(date_old, "%Y.%m.%d")
    delta_days = abs(
        (datetime.now() - datetime.strptime(date_old, "%Y.%m.%d")).days
    )
    if date_provided > datetime.now() and delta_days > 7:
        return "🟢"
    if delta_days < 7:
        return "🟡"
    if datetime.now() > date_provided and 7 < delta_days < 60:
        return "🔴"
    if datetime.now() > date_provided and delta_days > 60:
        return "⚫️"


def produce_status(list_users: list, list_abandon: list=[]) -> list:
    return [
        [
            id_tg,
            name,
            provide_status,
            date_legit if date_legit else "Вперше",
        ]
        for id_tg, name, _, date_legit in list_users
        if (provide_status := provide_dates(date_legit))
        and not provide_status in list_abandon        
    ]
