from datetime import datetime


def produce_sorting_by_date_by_name(list_users: list) -> list:
    list_users = sorted(
        list_users,
        key=lambda x: (datetime.strptime(x[3], "%Y.%m.%d"), x[1]),
        reverse=True
    )
    list_users = sorted(
        list_users,
        key=lambda x: x[1]
    )
    # list_users = sorted(
    #     list_users,
    #     key=lambda x: datetime.strptime(x[3], "%Y.%m.%d"),  # sort by date (descending)
    #     reverse=True
    # )
    return list_users


def provide_dates(date_old: str) -> str:
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


def produce_status(list_users: list) -> list:
    return [
        [
            id_tg,
            name,
            provide_dates(date_legit),
            date_legit,
        ]
        for id_tg, name, _, date_legit in list_users
    ]

