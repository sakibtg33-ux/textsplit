# Telegram TXT Split Bot

এই bot আপনার দেওয়া `split_d200.py`-এর logic অনুসরণ করে একটি `.txt` ফাইলকে প্রতি **৫০টি line** করে ভাগ করবে এবং `split_001.txt`, `split_002.txt`, `split_003.txt` ইত্যাদি নামে আলাদা document হিসেবে একই chat-এ পাঠাবে।

## ১. Token বসানো

`bot.py` ফাইল খুলে এই লাইনে BotFather থেকে পাওয়া token বসান:

```python
BOT_TOKEN = "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE"
```

Token কাউকে প্রকাশ করবেন না। Token প্রকাশ হয়ে গেলে BotFather-এর `/revoke` ব্যবহার করে নতুন token নিন।

## ২. Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ৩. Run

```bash
python3 bot.py
```

Terminal বন্ধ করলে bot বন্ধ হয়ে যাবে। ২৪/৭ চালাতে Linux server-এ `systemd`, Docker, অথবা কোনো process manager ব্যবহার করুন। সহজভাবে নিজের কম্পিউটারেও চালানো যাবে, তবে কম্পিউটারটি চালু ও internet-connected থাকতে হবে।

## ৪. ব্যবহার

Telegram-এ bot খুলে `/start` পাঠান। এরপর একটি UTF-8 `.txt` ফাইল document হিসেবে পাঠান। Bot প্রথমে মোট কতটি অংশ তৈরি হয়েছে জানাবে এবং তারপর প্রতিটি split file পাঠাবে।

## গুরুত্বপূর্ণ সীমা

Public Telegram Bot API দিয়ে bot সাধারণত সর্বোচ্চ ২০ MB input file download করতে পারে। বড় file-এর জন্য local Bot API server বা অন্য upload architecture দরকার হতে পারে।

## ফাইলসমূহ

| File | কাজ |
|---|---|
| `bot.py` | মূল Telegram bot |
| `requirements.txt` | Python dependency |
| `test_split.py` | split logic যাচাই করার test |

## পরীক্ষা

```bash
python3 test_split.py
python3 -m py_compile bot.py
```

বর্তমান test-এ ১২৩টি line থেকে ৫০, ৫০ এবং ২৩ line-এর তিনটি অংশ যাচাই করা হয়েছে।

## Render Web Service deployment

এই Web Service version চালাতে Render-এ **Web Service** নির্বাচন করুন।

| Field | Value |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python web_service.py` |
| Environment Variable | `BOT_TOKEN` = BotFather token |
| Instance Type | Free testing অথবা paid always-on service |

`web_service.py` একটি HTTP health endpoint চালু করে এবং একই সঙ্গে Telegram polling bot চালায়। Browser-এ Render URL খুললে `TXT split Telegram bot is running` দেখা যাবে।

**Static Site-এর জন্য এই bot deploy করা যাবে না**, কারণ Static Site শুধু HTML/CSS/JavaScript asset serve করে; Python process বা Telegram polling চালায় না।

Free Web Service idle অবস্থায় sleep করতে পারে। তাই পরীক্ষার জন্য Free ব্যবহার করা গেলেও নিরবচ্ছিন্ন ২৪/৭ bot-এর জন্য paid always-on service বেশি নির্ভরযোগ্য।
