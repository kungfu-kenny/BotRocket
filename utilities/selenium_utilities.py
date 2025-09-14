import json
import traceback
from time import sleep
from datetime import datetime
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from utilities.file_utilities import (
    save_json_events,
    get_file_dict_events,
)
from config import HEADLESS


@contextmanager
def Driver(url: str = None):
    options = FirefoxOptions()
    if HEADLESS:
        options.add_argument('--headless')
    driver = webdriver.Firefox(
        options=options,
        service=FirefoxService(GeckoDriverManager().install()),
        # firefox_binary=FirefoxBinary(FIREFOX_BIN),
        # service=FirefoxService('misc/geckodriver/geckodriver'),
        # executable_path='geckodriver/geckodriver',
    )
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(10)
    try:
        if url:
            driver.get(url)
        yield driver
    # except Exception:
    #     print(traceback.format_exc())
    finally:
        driver.close()


def select_country_ukraine(
    driver: object,
    css_selector: str='input.multiselect-tags-search[aria-placeholder="Select countries"]'
):
    value_use = driver.find_elements(
        By.CSS_SELECTOR,
        css_selector,
    )
    if not value_use:
        return
    value_use = value_use[0]
    value_use.click()
    value_use.send_keys("Ukraine")
    value_use.send_keys(Keys.ENTER)


def get_ajp():
    errors = False
    res = []
    try:
        with Driver('https://ajptour.com/en/federation/1/events') as driver:
            sleep(2)
            for event in driver.find_elements(
                By.CSS_SELECTOR,
                'div.event-bg.cover-bg.eventItem'
            ):
                
                if not (continent := event.get_attribute('data-continent')) or not continent == 'Europe':
                    continue
                name_used = event.get_attribute('data-name').strip()
                if not (
                    any(
                        k in name_used.lower().split(' ')
                        for k in [
                            'kyiv',
                            'odesa',
                            'lviv',
                            'dnipro',
                            'kharkiv',
                        ]
                    )
                    or 'ukraine' in name_used.lower()
                ):
                    continue
                location_used = 'Ukraine'
                for k in [
                    'kyiv',
                    'odesa',
                    'lviv',
                    'dnipro',
                    'kharkiv',
                ]:
                    if k in name_used.lower():
                        location_used = k.capitalize()
                        break
                date_number = (
                    str(datetime.utcnow().year) +
                    ' ' + event.get_attribute('data-date')
                )
                event_dict = {
                    "name": name_used,
                    "url": event.get_attribute('data-url').strip(),
                    "photo": i[0].get_attribute('src') if (
                        i:= event.find_elements(By.TAG_NAME, 'img')
                    ) else None,
                    "date": datetime.strptime(date_number, "%Y %B %d"),
                    "location": location_used,
                }
                res.append(event_dict)
    except Exception as e:
        print(e)
        print('111111111111111111111111111111111111111111')
        errors = True
    finally:
        return res, errors


def get_smoothcomp():
    errors = False
    res_smootgcomp = []
    try:
        with Driver('https://smoothcomp.com/en/events/upcoming') as driver:
            select_country_ukraine(driver)
            sleep(2)
            for event in driver.find_elements(
                By.CSS_SELECTOR,
                'div.col-xs-6.col-md-3.col-sm-clear-2.col-xs-clear-2.col-md-clear-4.col-lg-clear-4'
            ):
                if not 'Ukraine' in (location_use := i[0].text.strip() if (
                        i := event.find_elements(By.CSS_SELECTOR, 'p.margin-xs-0.truncate')
                    ) else None
                ):
                    continue
                date_original = i[0].text.strip() if (
                    i := event.find_elements(By.CSS_SELECTOR, 'div.flex-grow-1.date')
                ) else None
                if not date_original:
                    continue
                date_original =  date_original.split('-')[0].strip()
                date_original = str(datetime.utcnow().year) + ' ' + date_original
                event_dict = {
                    "name": i[0].text.strip() if (
                        i:= event.find_elements(By.CSS_SELECTOR, 'a.event-title.color-inherit')
                    ) else None,
                    "url": i[0].get_attribute('href') if (
                        i:= event.find_elements(By.CSS_SELECTOR, 'a.event-title.color-inherit')
                    ) else None,
                    "photo": i[0].get_attribute('src') if (
                        i:= event.find_elements(By.CSS_SELECTOR, 'img.full-width.img-rounded')
                    ) else None,
                    "date": datetime.strptime(date_original, "%Y %B %d"),
                    "location": location_use.split(',')[0].strip(),
                }
                res_smootgcomp.append(event_dict)
    except Exception as e:
        print(e)
        print('111111111111111111111111111111111111111111')
        errors = True
    finally:
        return res_smootgcomp, errors


def get_new_events() -> list[dict[str, str]]:
    if file_path := get_file_dict_events():
        with open(file_path, 'r') as f:
            list_events = json.load(f)
        return list_events
    list_events, errors = get_smoothcomp()
    list_events_a, errors_a = get_ajp()
    errors_a = False
    #TODO add here ajp problem later
    # if not errors_a:
    #     list_events.extend(list_events_a)
    list_events.sort(key=lambda x: x["date"])
    for x in list_events:
        x["date"] = datetime.strftime(x['date'], '%Y.%m.%d')
    dict_to_json = {
        "error": errors or errors_a,
        "lists": list_events,
    }
    save_json_events(dict_to_json)
    return dict_to_json


if __name__ == '__main__':
    get_new_events()