from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from utils.slack_notify import SlackNotify

slack = SlackNotify()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--lang=ja-JP")
chrome_options.add_argument("--disable-dev-shm-usage")

capabilities = DesiredCapabilities.CHROME.copy()

driver = webdriver.Remote(
    command_executor="http://selenium:4444/wd/hub",
    desired_capabilities=capabilities,
    options=chrome_options,
)

driver.get("https://maasaablog.com/")
slack.slack_notify(driver.title, "apple")
driver.quit()
