import json
import os

import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

# from utils.slack_notify import SlackNotify


class SlackNotify:
    """
    スラック通知のクラス
    """

    def __init__(self) -> None:
        self.slack_hook_url = os.getenv("SLACK_WEBHOOK_URL")
        assert self.slack_hook_url is not None, "環境変数にSLACK_WEBHOOK_URLが設定されていません。"

    def slack_notify(
        self,
        text: str,
        username: str = "incoming-webhook",
        color: str = "good",
        icon_emoji: str = ":ghost:",
    ) -> None:
        """スラックに通知を送るメソッド

        Args:
            text (str): 送る文字列
            username (str): ユーザー名
            color (str): 色
            icon_emoji (str): アイコンの絵文字
        """

        data = json.dumps(
            {
                "username": username,
                "icon_emoji": icon_emoji,  # 投稿のプロフィール画像に入れる絵文字
                "attachments": [
                    {
                        "text": text,
                        "color": color,  # good, warning, danger
                    }
                ],
            }
        )

        requests.post(self.slack_hook_url, data=data)


slack = SlackNotify()

chrome_options = webdriver.ChromeOptions()
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
