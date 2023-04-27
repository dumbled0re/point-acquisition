import os
from time import sleep

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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


def main():
    slack = SlackNotify()
    driver = driver_init()
    try:
        # JRAにアクセス
        print("autorace login start")
        driver.get("https://vote.autorace.jp/login")
        sleep(5)

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

        print("autorace login end")
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
        sleep(5)

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
        sleep(5)

        # 暗証番号の入力
        search = driver.find_element(
            By.XPATH, "/html/body/reach-portal/div/div/div/div[2]/div[1]/input"
        )
        search.send_keys(os.getenv("AUTO_RACE_PIN"))
        sleep(5)

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
        sleep(5)

        # 清算
        # element = driver.find_element_by_name('btnWireOut')
        # element.click()

        # ポップアップウィンドウに表示されたメッセージに同意(Alert(driver).dismiss()で、アラートを拒否)
        # Alert(driver).accept()

        # 入金完了通知
        slack.slack_notify(
            text="Auto Race ネット投票に入金が完了しました",
            username="auto_deposit_rakuten_horse_racing",
            color="good",
        )
    except ZeroDivisionError:
        slack.slack_notify(
            text="Auto Race ネット投票に入金ができませんでした",
            username="auto_deposit_rakuten_horse_racing",
            color="danger",
        )
    finally:
        driver.close()
        driver.quit()
        print("driver stop")


if __name__ == "__main__":
    main()
