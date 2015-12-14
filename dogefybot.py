#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import cv2
import time
import logging
import telebot


# Check for environment variable
if 'DOGEFY_TKN' not in os.environ:
    print >> sys.stderr, "Environment variable 'DOGEFY_TKN' not defined."
    exit(1)

# Initialize logger (only logs exceptions and polling status at info+ level)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# Initialize bot api with token from environment
bot = telebot.TeleBot(os.environ['DOGEFY_TKN'])

# Ignore messages older than x seconds
time_ignore = 5*60

# Doge image and final image extension
img_doge = cv2.imread('doge.png', -1)
img_ext = '_dogefied.png'

# Cascade classifier parameters, can be tricky to adjust...
cc_scale_factor = 1.2
cc_min_neighbors = 5
cc_min_size = (20, 20)
cc_flags = cv2.CASCADE_SCALE_IMAGE | cv2.CASCADE_DO_ROUGH_SEARCH


# Dogefy magic happens here (very wow, such magic, many pattern recognition)
def dogefy(img_file):
    # Initialize the classifier with the frontal face haar cascades
    face_cc = cv2.CascadeClassifier(('/usr/share/opencv/haarcascades/'
                                     'haarcascade_frontalface_alt_tree.xml'))

    # Read image
    img = cv2.imread(img_file)
    # Convert to grays
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Equalize histogram, for improving contrast (this helps detection)
    gray = cv2.equalizeHist(gray)

    # Perform detection
    faces = face_cc.detectMultiScale(gray,
                                     scaleFactor=cc_scale_factor,
                                     minNeighbors=cc_min_neighbors,
                                     minSize=cc_min_size,
                                     flags=cc_flags)

    # Dogefy all the faces!
    for (x, y, w, h) in faces:
        # Resize the doge according to the face
        doge_res = cv2.resize(img_doge, (w, h))

        # Copy the resided doge over the face keeping the alpha channel
        for c in range(0, 3):
            img[y:y+h, x:x+w, c] = doge_res[:, :, c] * \
                                   (doge_res[:, :, 3] / 255.0) + \
                                   img[y:y+h, x:x+w, c] * \
                                   (1.0 - (doge_res[:, :, 3] / 255.0))

    # Write the file if there is at least one face
    n_faces = len(faces)
    if n_faces > 0:
        cv2.imwrite(img_file+img_ext, img)

    return n_faces


# Bot photo handler
@bot.message_handler(content_types=['photo'])
def handle_photo(m):
    # Ignore old messages
    if (int(time.time()) - time_ignore) > m.date:
        return

    # Chat id, for sending actions and file
    cid = m.chat.id

    # Search the biggest photo (avoid thumbnails)
    f_id = None
    b_size = 0
    for p in m.photo:
        t_size = p.height * p.width
        if t_size > b_size:
            b_size = t_size
            f_id = p.file_id

    # Download and write the file
    f_info = bot.get_file(f_id)
    f_download = bot.download_file(f_info.file_path)

    with open(f_id, 'wb') as f:
        f.write(f_download)

    # Dogefy all the faces!!
    n_faces = dogefy(f_id)
    if n_faces > 0:
        # Send "uploading photo" action since can take a few seconds
        bot.send_chat_action(cid, 'upload_photo')

        # Upload the photo and do it as a reply
        bot.send_photo(cid,
                       open(f_id+img_ext, 'rb'),
                       caption='Very wow, such doge%s.' %
                       ('s' if n_faces > 1 else ''),
                       reply_to_message_id=m.message_id)

        try:
            os.unlink(f_id+img_ext)
        except:  # You shouldn't do this never but... *effort*
            pass

    # If there is no faces and is not a group tell the user
    elif cid > 0:
        bot.send_chat_action(cid, 'typing')
        bot.reply_to(m, 'Very fail, such sad, no faces.')

    try:
        os.unlink(f_id)
    except:  # You shouldn't do this never but... *effort*
        pass


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(m):
    # Ignore old messages
    if (int(time.time()) - time_ignore) > m.date:
        return

    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m,
                 ("Hi, I search for faces in sent photos and if I find any I "
                  "replace them for *doges*. _Very wow._"
                  "\n\nPlease rate me at the @storebot following this link:"
                  " https://telegram.me/storebot?start=dogefy\_bot"
                  "\n\nQ: Why do I need _access to messages_?"
                  "\nA: In order to get images sent to groups I need it. "
                  "I don't like it either, I would prefer a system where bot "
                  "developers can register _atomic permissions_ like "
                  "_get-image_, _send-image_, _get-audio_, _send-audio_, ..."
                  "\n\nThe source code is licensed under _GPLv3_ and can be "
                  "found at https://github.com/skgsergio/dogefy-tg-bot"),
                 disable_web_page_preview=True, parse_mode="Markdown")

bot.polling(none_stop=True)
