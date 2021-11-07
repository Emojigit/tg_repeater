#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys, re, logging, git, os
exit = sys.exit
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackContext
from telegram.ext.filters import Filters
from telegram.error import InvalidToken
from telegram import ParseMode, Update, Bot
from git.exc import InvalidGitRepositoryError
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s[%(name)s] %(message)s")
log = logging.getLogger("MainScript")
chans = []

def dirty():
    fd = os.path.dirname(os.path.realpath(__file__))
    try:
        gr = git.Repo(fd)
    except InvalidGitRepositoryError:
        return false
    return gr.is_dirty(untracked_files=True)
    

def token():
    try:
        with open("token.txt","r") as f:
            return f.read().rstrip('\n')
    except FileNotFoundError:
        log.error("No token.txt!")
        return ""

def GRH(bot):
    def rawhandler(update, context):
        msg = update.message.text
        log.info("Received message with content: {}".format(msg))
        if msg.startswith(("(NOMO)","(NOREPEAT)","(NORE)")):
            log.info("Prefix matched!")
            return
        if update.message.chat_id not in chans:
            chans.append(update.message.chat_id)
            if dirty():
                bot.sendMessage(update.message.chat_id, "This bot is not in the stable state.")
        if msg == "WWSSAADD" or msg == "^^vv<<>>" or msg == "573" or msg == "WWSSAADD573" or msg == "^^vv<<>>573":
            log.info("Konami Command!")
            bot.sendMessage(update.message.chat_id, "Konami Command!")
            bot.sendMessage(update.message.chat_id, "😜")
        else:
            # Eric Liu wear girl's dressing BOOST!
            if msg.contains("Eric") or msg.contains("女裝") or msg.contains("劉醬") or msg.contains("刘酱"):
		bot.sendMessage(update.message.chat_id, "劉醬快女裝！")
            # Do not ping!
            RMSG = re.sub('@[a-zA-Z0-9_]+[ ]?', '<ping>', msg)
            # Eric Liu wear girl's dressing, a meme on zh wikipedia
            RMSG = RMSG.replace("劉醬快女裝！", "我十分同意！")
            RMSG = RMSG.replace("劉醬女裝！", "我100%同意！")
            # How dare you?
            RMSG = RMSG.replace("How dare you?", "Greta Thunberg said: \"How dare you?\"")
            bot.sendMessage(update.message.chat_id, RMSG)
    return MessageHandler(Filters.text, rawhandler)

def GOH(bot):
    def otherhandler(update, context):
        log.info("Received other message!")
        if update.message.chat_id not in chans:
            chans.append(update.message.chat_id)
            if dirty():
                bot.sendMessage(update.message.chat_id, "This bot is not in the stable state.")
        bot.forward_message(chat_id=update.message.chat_id,
                        from_chat_id=update.message.chat_id,
                        message_id=update.message.message_id)
    return MessageHandler(Filters.all, otherhandler)

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
        bot = Bot(token=tok)
        updater = Updater(bot=bot, use_context=True)
        log.info("Get updater success!")
    except InvalidToken:
        log.critical("Invalid Token! Plase edit token.txt and fill in a valid token.")
        raise
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("ping", GetCMDCallBack("ping","pong")))
    dp.add_handler(CommandHandler("start", GetCMDCallBack("start",starttxt())))
    dp.add_handler(GRH(bot))
    dp.add_handler(GOH(bot))
    updater.start_polling()
    log.info("Started the bot! Use Ctrl-C to stop it.")
    updater.idle()

if __name__ == '__main__':
    main(token())

