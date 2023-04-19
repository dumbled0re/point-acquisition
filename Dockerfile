FROM --platform=linux/amd64 python:3.9.16-bullseye

# Google Chromeのインストール
RUN apt-get update -yqq \
    && apt-get install -yqq \
        wget \
        gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update -yqq \
    # 公式リポジトリにあるバージョン確認する
    # && apt-cache madison google-chrome-stable \
    && apt-get install -yqq google-chrome-stable=112.0.5615.121-1 \
    && rm /etc/apt/sources.list.d/google-chrome.list \
    && rm -rf /var/lib/apt/lists/*

# ChromeDriverのインストール
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/112.0.5615.49/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Pythonの依存関係のインストール
WORKDIR /usr/src

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r ./requirements.txt
