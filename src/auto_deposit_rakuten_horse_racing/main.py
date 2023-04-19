import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)

driver.get("https://zenn.dev/")
time.sleep(3)
driver.close()
driver.quit()
