#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys, re, logging
exit = sys.exit
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackContext
from telegram.ext.filters import Filters
from telegram.error import InvalidToken
from telegram import ParseMode, Update
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s[%(name)s] %(message)s")
log = logging.getLogger("MainScript")

def token():
    try:
        with open("token.txt","r") as f:
            return f.read().rstrip('\n')
    except FileNotFoundError:
        log.error("No token.txt!")
        return ""

def rawhandler(update, context):
    msg = update.message.text
    log.info("Received message with content: {}".format(msg))
    if msg == "WWSSAADD" or msg == "^^vv<<>>" or msg == "573" or msg == "WWSSAADD573" or msg == "^^vv<<>>573":
        log.info("Konami Command!")
        update.message.reply_text("Konami Command!")
        update.message.reply_text("😜")
    else:
        update.message.reply_text(msg)

def starttxt():
    try:
        with open("start.txt","r") as f:
            return f.read().rstrip('\n')
    except FileNotFoundError:
        log.warning("No start.txt, using the example.")
        try:
            with open("start.txt.example","r") as f:
                return f.read().rstrip('\n')
        except FileNotFoundError:
            log.warning("No start.txt.example!")
            return ""

def GetCMDCallBack(cname,rcont):
    def CMDCB(update: Update, context: CallbackContext):
        log.info("Got {} command!".format(cname))
        update.message.reply_text(rcont,parse_mode=ParseMode.MARKDOWN_V2)
    return CMDCB

def main(tok):
    if tok == "":
        log.critical("No token!")
        exit(3)
    try:
        updater = Updater(tok, use_context=True)
        log.info("Get updater success!")
    except InvalidToken:
        log.critical("Invalid Token! Plase edit token.txt and fill in a valid token.")
        raise
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("ping", GetCMDCallBack("ping","pong")))
    dp.add_handler(CommandHandler("start", GetCMDCallBack("start",starttxt())))
    dp.add_handler(MessageHandler(Filters.text, rawhandler))
    updater.start_polling()
    log.info("Started the bot! Use Ctrl-C to stop it.")
    updater.idle()

if __name__ == '__main__':
    main(token())


