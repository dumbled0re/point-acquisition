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


def collect_spat4(driver):
    # spat4にアクセス
    driver.get("https://www.spat4.jp/keiba/pc")
    sleep(3)

    # ログイン
    search = driver.find_element(By.ID, "MEMBERNUMR")
    search.send_keys(config.SPAT4_MEMBERNUM)

    search = driver.find_element(By.ID, "MEMBERIDR")
    search.send_keys(config.SPAT4_MEMBERID)

    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/form/a/span"))
    )
    button.click()
    sleep(3)

    # 精算ページに遷移
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/form/div/div[3]/div/ul/li[5]/input")
        )
    )
    button.click()
    sleep(3)

    driver.switch_to.window(driver.window_handles[-1])

    # 通知の必要
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "MAILR"))
    )
    button.click()
    sleep(3)

    # 精算指示確認
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='seisanForm']/div/input"))
    )
    button.click()
    sleep(3)

    # 暗証番号の入力
    search = driver.find_element(By.ID, "MEMBERPASSR")
    search.send_keys(config.SPAT4_MEMBERPASS)

    # 精算ボタン
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "EXEC"))
    )
    button.click()
    sleep(3)


def main():
    try:
        driver = driver_init()
        collect_spat4(driver)
    except ZeroDivisionError:
        pass
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main()
