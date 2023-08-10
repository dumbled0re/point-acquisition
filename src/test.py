import re
import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
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


def quit_driver(driver):
    driver.close()
    driver.quit()


def convert_to_int(text):
    return int(re.sub(r"[^\d]", "", text))


def deposit_autorace(driver):
    # JRAにアクセス
    driver.get("https://vote.autorace.jp/login")
    sleep(3)

    # ログイン
    search = driver.find_element(By.NAME, "userNumber")
    search.send_keys(config.AUTO_RACE_USER_NUMBER)

    search = driver.find_element(By.NAME, "password")
    search.send_keys(config.AUTO_RACE_PASSWORD)

    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.jsx-2171994817.button.button--primary")
        )
    )
    button.click()
    sleep(3)

    # 入金リンク
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
    search.send_keys(config.AUTO_RACE_PIN)
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

    # ポップアップウィンドウに表示されたメッセージに同意(Alert(driver).dismiss()で、アラートを拒否)
    # Alert(driver).accept()


def deposit_spat4(driver):
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

    # 入金ページに遷移
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/form/div/div[3]/div/ul/li[4]/input")
        )
    )
    button.click()
    sleep(3)

    driver.switch_to.window(driver.window_handles[-1])

    # 100円入力
    search = driver.find_element(By.ID, "ENTERR")
    search.send_keys("100")

    # 通知の必要
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "MAILR"))
    )
    button.click()
    sleep(3)

    # 入金指示確認
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/form/div/input"))
    )
    button.click()
    sleep(3)

    # 暗証番号の入力
    search = driver.find_element(By.ID, "MEMBERPASSR")
    search.send_keys(config.SPAT4_MEMBERPASS)

    # 入金ボタン
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "EXEC"))
    )
    button.click()
    sleep(5)


def collect_autorace(driver):
    # JRAにアクセス
    driver.get("https://vote.autorace.jp/login")
    sleep(3)

    # ログイン
    search = driver.find_element(By.NAME, "userNumber")
    search.send_keys(config.AUTO_RACE_USER_NUMBER)

    search = driver.find_element(By.NAME, "password")
    search.send_keys(config.AUTO_RACE_PASSWORD)

    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.jsx-2171994817.button.button--primary")
        )
    )
    button.click()
    sleep(3)

    # 精算リンク
    a_item = driver.find_element(
        By.XPATH, "//*[@id='__next']/div/div/div[1]/div/ul/li[3]/a"
    )
    url = a_item.get_attribute("href")
    driver.get(url)
    sleep(3)

    # 精算可能金額を取得
    text = driver.find_element(
        By.XPATH, "//*[@id='__next']/div/div/div[2]/div/div/div[2]/div[2]/span"
    ).text
    amount = convert_to_int(text)

    search = driver.find_element(
        By.XPATH, "//*[@id='__next']/div/div/div[2]/div/div/div[2]/div[1]/div/input"
    )
    search.send_keys(amount)

    # 精算ボタンクリック
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//*[@id='__next']/div/div/div[2]/div/div/div[2]/button",
            )
        )
    )
    button.click()
    sleep(3)

    # 暗証番号の入力
    search = driver.find_element(
        By.XPATH, "/html/body/reach-portal/div/div/div/div[2]/div[1]/input"
    )
    search.send_keys(config.AUTO_RACE_PIN)

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

    # ポップアップウィンドウに表示されたメッセージに同意(Alert(driver).dismiss()で、アラートを拒否)
    # Alert(driver).accept()


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
        # EC.presence_of_all_elements_located((By.XPATH, "//div[@class='go_btn']"))
        EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='go_btn']"))
    )

    # 全てのボタンをクリック
    for elem in elems:
        elem.click()
        sleep(1)
    sleep(5)


def main():
    slack = SlackNotify()
    arg = sys.argv
    if not len(arg) > 1:
        print("引数がありません")
        sys.exit()
    if arg[1] == "deposit_autorace":
        try:
            driver = driver_init()
            deposit_autorace(driver)
            slack.slack_notify(
                text="オートレースに入金が完了しました",
                username="auto-deposit-autoracing",
                color="good",
            )
        except ZeroDivisionError:
            slack.slack_notify(
                text="オートレースに入金が失敗しました",
                username="auto-deposit-autoracing",
                color="danger",
            )
        finally:
            quit_driver(driver)
    elif arg[1] == "deposit_spat4":
        try:
            driver = driver_init()
            deposit_spat4(driver)
            slack.slack_notify(
                text="SPAT4に入金が完了しました",
                username="auto-deposit-spat4",
                color="good",
            )
        except ZeroDivisionError:
            slack.slack_notify(
                text="SPAT4に入金が失敗しました",
                username="auto-deposit-spat4",
                color="danger",
            )
        finally:
            quit_driver(driver)
    elif arg[1] == "collect_autorace":
        try:
            driver = driver_init()
            collect_autorace(driver)
            slack.slack_notify(
                text="オートレースの精算が完了しました",
                username="auto-collect-autorace",
                color="good",
            )
        except ZeroDivisionError:
            slack.slack_notify(
                text="オートレースの精算が失敗しました",
                username="auto-collect-autorace",
                color="danger",
            )
        finally:
            quit_driver(driver)
    elif arg[1] == "collect_spat4":
        try:
            driver = driver_init()
            collect_spat4(driver)
            slack.slack_notify(
                text="SPAT4の精算が完了しました",
                username="auto-collect-spat4",
                color="good",
            )
        except ZeroDivisionError:
            slack.slack_notify(
                text="SPAT4の精算が失敗しました",
                username="auto-collect-spat4",
                color="danger",
            )
        finally:
            quit_driver(driver)
    elif arg[1] == "point_income":
        try:
            driver = driver_init()
            get_point_from_point_income(driver)
            slack.slack_notify(
                text="Point Incomeのクリックが成功しました",
                username="auto-get-point-income",
                color="good",
            )
        except ZeroDivisionError:
            slack.slack_notify(
                text="Point Incomeのクリックが失敗しました",
                username="auto-get-point-income",
                color="danger",
            )
        finally:
            quit_driver(driver)
    else:
        print("指定の引数の処理がありません。")


if __name__ == "__main__":
    main()
