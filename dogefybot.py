#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import cv2
import time
import telebot


# Check for environment variable
if 'DOGEFY_TKN' not in os.environ:
    print >> sys.stderr, "Environment variable 'DOGEFY_TKN' not defined."
    exit(1)

# Initialize bot api with token from environment
bot = telebot.TeleBot(os.environ['DOGEFY_TKN'])

# Ignore messages older than x seconds
time_ignore = 5*60

# Doge image and final image extension
img_doge = cv2.imread('doge.png', -1)
img_ext = '_dogefied.png'

# Cascade classifier parameters, can be tricky to adjust...
cc_scale_factor = 1.2
cc_min_neighbors = 4
cc_min_size = (20, 20)
# (1.2 5 30,30) (1.2 5 20,20) (1.3 4 20.20) (1.2 4 20,20)


# Dogefy magic happens here (very wow, such magic, many pattern recognition)
def dogefy(img_file):
    face_cc = cv2.CascadeClassifier(('/usr/share/opencv/haarcascades/'
                                     'haarcascade_frontalface_alt.xml'))

    img = cv2.imread(img_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = face_cc.detectMultiScale(gray,
                                     scaleFactor=cc_scale_factor,
                                     minNeighbors=cc_min_neighbors,
                                     minSize=cc_min_size,
                                     flags=cv2.CASCADE_SCALE_IMAGE)

    for (x, y, w, h) in faces:
        doge_res = cv2.resize(img_doge, (w, h))

        for c in range(0, 3):
            img[y:y+h, x:x+w, c] = doge_res[:, :, c] * \
                                   (doge_res[:, :, 3] / 255.0) + \
                                   img[y:y+h, x:x+w, c] * \
                                   (1.0 - (doge_res[:, :, 3] / 255.0))

    n_faces = len(faces)
    if n_faces > 0:
        cv2.imwrite(img_file+img_ext, img)

    return n_faces


# Bot photo handler
@bot.message_handler(content_types=['photo'])
def handle_photo(m):
    if (int(time.time()) - time_ignore) > m.date:
        return

    cid = m.chat.id

    f_id = None
    b_size = 0
    for p in m.photo:
        t_size = p.height * p.width
        if t_size > b_size:
            b_size = t_size
            f_id = p.file_id

    f_info = bot.get_file(f_id)
    f_download = bot.download_file(f_info.file_path)

    with open(f_id, 'wb') as f:
        f.write(f_download)

    n_faces = dogefy(f_id)
    if n_faces > 0:
        bot.send_chat_action(cid, 'upload_photo')

        bot.send_photo(cid,
                       open(f_id+img_ext, 'rb'),
                       caption='Very wow, such doge%s.' %
                       ('s' if n_faces > 1 else ''),
                       reply_to_message_id=m.message_id)

        os.unlink(f_id+img_ext)

    os.unlink(f_id)

bot.polling()
