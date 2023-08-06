# kuumuu-bot

> A discord bot by Kuumo using Python

# Install

```
    pip install -r requirements.txt
```

# Usage

## 1. Create a folder `data_base` (You will save discord token, bing AI cookies and google Bard cookies in this folder)
## 2. Create file named `__init__.py` in `data_base` (For import config.py)
## 3. Create file named `config.py` in `data_base (You will save your discord bot TOKEN here)
```
Discord_TOKEN = "Your token here"

Secure_1PSID = ""

Secure_1PSIDTS = ""
```
## 4 Create file named `cookies.json` (You will save Bing AI cookies here)

## Setup cookies extension

You can use any cookies exxtension to get cookies

## Bing AI cookies

1. Go to https://bing.com/chat
2. Run your `cookies extension`
3. Copy all cookies by using `export by json` to your clipboard
4. Go to `cookies.json`
5. Paste the cookies

## Google Bard cookies

1. Go to https://bard.google.com/
2. Run your `cookies extension`
3. Copy value of `Secure_1PSID` to your clipboard
4. Copy value of `Secure_1PSIDTS` to your clipboard
5. Go to `config.py`
6. Paste value of `Secure_1PSID` to variable named `Secure_1PSID`
7. Paste value of `Secure_1PSIDTS` to variable named `Secure_1PSIDTS`
