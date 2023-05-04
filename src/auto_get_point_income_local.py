from time import sleep

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import config
from utils.slack_notify import SlackNotify


def driver_init():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--lang=ja-JP")
    chrome_options.add_argument("--disable-dev-shm-usage")

    capabilities = DesiredCapabilities.CHROME.copy()

    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        desired_capabilities=capabilities,
        options=chrome_options,
    )
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
    sleep(5)


def main():
    try:
        slack = SlackNotify()
        driver = driver_init()
        get_point_from_point_income(driver)

        slack.slack_notify(
            text="Point Incomeのクリックが成功しました",
            username="auto_get_point_income",
            color="good",
        )
    except ZeroDivisionError:
        slack.slack_notify(
            text="Point Incomeのクリックが失敗しました",
            username="auto_get_point_income",
            color="danger",
        )
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main()
