import os
import json
import shutil
from datetime import datetime
from config import (
    PATH_STORAGE,
    PATH_PHOTOS,
    PATH_STORAGE_INVOICE,
    PATH_STORAGE_TMP,
    PATH_SCHEDULE_DEFAULT,
)


def check_folder():
    for i in [
        PATH_STORAGE,
        PATH_STORAGE_TMP,
        PATH_STORAGE_INVOICE,
    ]:
        (os.path.exists(i) or os.path.isdir(i) or os.mkdir(i))


def add_new_invoice(id_user: int, id_admin: int, tmp_file: bool = True) -> str:
    check_folder()
    date_send = datetime.now().strftime("%Y_%m_%d")
    folder = PATH_STORAGE_INVOICE if not tmp_file else PATH_STORAGE_TMP
    return os.path.join(
        folder,
        f"{id_admin}_{id_user}_{date_send}.jpg"
    )


def check_invoice_file_already(id_user: int) -> bool:
    check_folder()
    date_send = datetime.now().strftime("%Y_%m")
    for file_tst in os.listdir(PATH_STORAGE_INVOICE):
        if f'_{id_user}_{date_send}' in file_tst:
            return True
    return False


def add_new_invoice_file(id_user: int, id_admin: int) -> str:
    check_folder()
    date_send = datetime.now().strftime("%Y_%m_%d")
    folder = PATH_STORAGE_INVOICE
    return os.path.join(
        folder,
        f"{id_admin}_{id_user}_{date_send}.pdf"
    )


def _remove_tmp_file(file_loc: str) -> None:
    os.remove(file_loc)


def remove_storage_tmp() -> None:
    for i in os.listdir(PATH_STORAGE_TMP):
        if any(
            v in i.lower() for v in [
                ".pdf",
                '.jpg',
                '.png',
                '.jpeg',
            ]
        ):
            os.remove(
                os.path.join(
                    PATH_STORAGE_TMP,
                    i,
                )
            )


def add_new_schedule_file(file_name:str) -> str:
    check_folder()
    for i in os.listdir(PATH_STORAGE):
        shutil.move(
            os.path.join(PATH_STORAGE, i),
            os.path.join(PATH_STORAGE_TMP, i)
        )
    return os.path.join(PATH_STORAGE, file_name)


def get_schedule_file() -> tuple[str, bool]:
    check_folder()
    if PATH_SCHEDULE_DEFAULT in os.listdir(PATH_STORAGE):
        return os.path.join(PATH_STORAGE, PATH_SCHEDULE_DEFAULT), True
    for f in os.listdir(PATH_STORAGE):
        if check_schedule_file_pdf(f) or check_schedule_file_photo(f):  #'.pdf' in f.lower():
            return os.path.join(PATH_STORAGE, f), False
    return None, False


def check_schedule_file_pdf(f) -> bool:
    return ".pdf" in f.lower()


def get_photo_path(f: str) -> str:
    return os.path.join(PATH_PHOTOS, f)


def check_schedule_file_photo(f) -> bool:
    return any(
        v in f.lower() for v in [
            '.jpg',
            '.png',
            '.jpeg',
        ]
    )


def get_schedule_photo(file_name:str = 'test.png') -> str:
    check_folder()
    return os.path.join(
        PATH_STORAGE,
        file_name,
    )


def delete_old_schedules(schedule:bool=True) -> None:
    check_folder()
    for i in os.listdir(PATH_STORAGE_TMP):
        if '.db' in i:
            continue
        if schedule:
            if '.json' in i:
                continue
            os.remove(os.path.join(PATH_STORAGE_TMP, i))
        else:
            if not '.json' in i:
                continue
            os.remove(os.path.join(PATH_STORAGE_TMP, i))


def get_file_dict_events() -> str:
    check_folder()
    date_today = os.path.join(
        PATH_STORAGE_TMP,
        f'{datetime.now().strftime("%Y_%m_%d")}.json',
    )
    if os.path.exists(date_today) and os.path.isfile(date_today):
        return date_today


def save_json_events(value_json: dict) -> None:
    delete_old_schedules(False)
    with open(
        os.path.join(
            PATH_STORAGE_TMP,
            f'{datetime.now().strftime("%Y_%m_%d")}.json',
        ),
        'w'
    ) as f:
        json.dump(value_json, f)


def make_chunks(value_list: list, chunk_size: int = 3) -> list:
    return [
        value_list[i: i + chunk_size]
        for i
        in range(
            0,
            len(value_list),
            chunk_size,
        )
    ]
    