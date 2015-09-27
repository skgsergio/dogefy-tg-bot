# Dogefy Telegram bot
This is the source code of the [Dogefy](https://telegram.me/dogefy_bot) Telegram
bot.

The bot is pretty simple, just listens for photos, downloads them, search for
human front faces and *replaces* them with a doge.

Please rate it following this [link](https://telegram.me/storebot?start=dogefy_bot)

## Requirements
You need the python [`pyTelegramBotAPI`](https://github.com/eternnoir/pyTelegramBotAPI)
and [`OpenCV`](http://opencv.org/).

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

You may need to install `opencv-data` if not working.

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

## License: GPLv3
```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
