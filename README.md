# Dogefy Telegram bot
This is the source code of the [Dogefy](https://telegram.me/dogefy_bot) Telegram
bot.

The bot is pretty simple, just listens for photos, downloads them, search for
human front faces and *replaces* them with a doge.

## Requirements
You need the python [`pyTelegramBotAPI`](https://github.com/eternnoir/pyTelegramBotAPI)
and `OpenCV`.

### `pyTelegramBotAPI` installation
```
pip install pyTelegramBotAPI
# or if you want to install it as user, not system-wide
pip install --user pyTelegramBotAPI
# if you have python3 as default you should use pip2
```

### `OpenCV` installation
* Debian based systems (Ubuntu, Linux Mint, ElementaryOS, ...)
```
apt-get install python-opencv
```

* Arch Linux
```
pacman -S opencv
```

## Usage

```
DOGEFY_TKN="123456789:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" python2 dogefybot.py
# if you have python3 as default you should use python2
```

## To-do list
* Maybe add a listener for photos sent as files (no compression).
```
@bot.message_handler(func=lambda m: m.document.mime_type.startswith('image/'),
content_types=['document'])
def handle_photo_as_document(m):
    [...]
```

* Make compatible with `OpenCV 3`
