from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# from utils.slack_notify import SlackNotify


def driver_init():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)

    return driver


# slack = SlackNotify()
driver = driver_init()
driver.get("https://maasaablog.com/")
# slack.slack_notify(driver.title, "apple")
driver.quit()
