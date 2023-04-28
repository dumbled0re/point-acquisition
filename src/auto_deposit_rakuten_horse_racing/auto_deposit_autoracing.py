import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def driver_init():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)

    return driver


def main():
    driver = driver_init()
    try:
        # JRAにアクセス
        driver.get("https://vote.autorace.jp/login")
        sleep(3)

        # ログイン
        search = driver.find_element(By.NAME, "userNumber")
        search.send_keys(os.getenv("AUTO_RACE_USER_NUMBER"))

        search = driver.find_element(By.NAME, "password")
        search.send_keys(os.getenv("AUTO_RACE_PASSWORD"))

        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.jsx-2171994817.button.button--primary")
            )
        )
        button.click()
        sleep(3)

        # 入金リンクをクリック
        a_item = driver.find_element(
            By.XPATH, "//*[@id='__next']/div/div/div[1]/div/ul/li[2]/a"
        )
        url = a_item.get_attribute("href")
        driver.get(url)
        sleep(3)

        # 楽天銀行をクリック
        a_item = driver.find_element(
            By.XPATH, "//*[@id='__next']/div/div/div[2]/div/div/div/section[1]/div/a"
        )
        url = a_item.get_attribute("href")
        driver.get(url)
        sleep(3)

        # 100円投入
        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#__next > div > div > div.jsx-3011364962.m__center > div > div > div.jsx-2710184671._bg-white.dark\:_bg-dark-3._p-5._mb-5 > div.jsx-2710184671._max-w-sm._mx-auto._mb-5 > div.jsx-2710184671._flex._justify-between > button:nth-child(1)",
                )
            )
        )
        button.click()
        sleep(3)

        # 入金ボタンクリック
        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#__next > div > div > div.jsx-3011364962.m__center > div > div > div.jsx-2710184671._bg-white.dark\:_bg-dark-3._p-5._mb-5 > button",
                )
            )
        )
        button.click()
        sleep(3)

        # 暗証番号の入力
        search = driver.find_element(
            By.XPATH, "/html/body/reach-portal/div/div/div/div[2]/div[1]/input"
        )
        search.send_keys(os.getenv("AUTO_RACE_PIN"))
        sleep(3)

        # okボタンクリック
        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "body > reach-portal > div > div > div > div:nth-child(2) > div.jsx-2710184671._flex._justify-between > button.jsx-2171994817.button.button--primary._ml-1._w-48",
                )
            )
        )
        button.click()
        sleep(3)

        # 清算
        # element = driver.find_element_by_name('btnWireOut')
        # element.click()

        # ポップアップウィンドウに表示されたメッセージに同意(Alert(driver).dismiss()で、アラートを拒否)
        Alert(driver).accept()

    except ZeroDivisionError:
        pass
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main()
