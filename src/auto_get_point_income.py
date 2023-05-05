from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import config


def driver_init():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)

    return driver


def get_point_from_point_income(driver):
    driver.get("https://pointi.jp/entrance.php")
    sleep(3)

    search = driver.find_element(By.NAME, "email_address")
    search.send_keys(config.POINT_INCOME_EMAIL)

    password = driver.find_element(By.NAME, "password")
    password.send_keys(config.POINT_INCOME_PASSWORD)

    driver.execute_script("arguments[0].scrollIntoView(true);", password)

    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "Submit"))
    )
    button.click()
    sleep(3)

    driver.get("https://pointi.jp/daily.php")
    sleep(3)

    elems = WebDriverWait(driver, 10).until(
        # EC.presence_of_all_elements_located((By.XPATH, "//div[@class='click_btn']"))
        EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='click_btn']"))
    )

    # 全てのボタンをクリック
    for elem in elems:
        elem.click()
        sleep(1)
    sleep(3)


def main():
    try:
        driver = driver_init()
        get_point_from_point_income(driver)
    except ZeroDivisionError:
        pass
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main()
