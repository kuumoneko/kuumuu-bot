# kuumuu-bot

> A discord bot by Kuumo using Python

# Install

```
    pip install -r requirements.txt
```

# Before starting

1. Create a folder `data_base` (You will save discord token, bing AI cookies and google Bard cookies in this folder)
2. Create file named `__init__.py` in `data_base` (For import config.py)
3. Create file named `config.py` in `data_base` (You will save your discord bot TOKEN here)
```
Discord_TOKEN = "Your token here"

Secure_1PSID = ""

Secure_1PSIDTS = ""
```
4. Create file named `cookies.json` (You will save Bing AI cookies here)

5. Setup cookies extension
```
Go to your web browser
Download an extension for reading cookies
You can use any cookies exxtension to get cookies
```

# Get discord bot Token

1. Go to https://discord.com/developers/applications/
2. Chose your discord bot
3. Chose `Bot`
4. Chose `Reset Token` and follow the directions
5. Go to `config.py`
6. Paste your Token to variable named `Discord_TOKEN`

# Get Bing AI cookies

1. Go to https://bing.com/chat
2. Run your `cookies extension`
3. Copy all cookies by using `export by json` to your clipboard
4. Go to `cookies.json`
5. Paste the cookies

# Get Google Bard cookies

1. Go to https://bard.google.com/
2. Run your `cookies extension`
3. Copy value of `Secure_1PSID` to your clipboard
4. Copy value of `Secure_1PSIDTS` to your clipboard
5. Go to `config.py`
6. Paste value of `Secure_1PSID` to variable named `Secure_1PSID`
7. Paste value of `Secure_1PSIDTS` to variable named `Secure_1PSIDTS`

# Set up other file in main

1. Go to `src.aclient`
2. Replace `config.kuumuu_TOKEN` by `config.Discord_TOKEN`