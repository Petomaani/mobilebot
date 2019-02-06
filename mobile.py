# -*- coding: utf-8 -*-

import logging
from datetime import date, timedelta, datetime

from config import TOKEN
from telegram.ext import Updater, MessageHandler, Filters


class TelegramBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
                                   '%(message)s', level=logging.INFO)

        updater = Updater(token=TOKEN)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(MessageHandler(Filters.command, self.commandsHandler))

        self.commands = {'wabu': self.wabu,
                         'kiitos': self.kiitos,
                         'sekseli': self.sekseli,
                         'pöytä': self.pöytä,
                         'insv': self.insv,
                         }

        self.viim_kom = {command: [] for command in self.commands.keys()}

        updater.start_polling()
        updater.idle()

    @staticmethod
    def wabu(bot, update):
        wabu = date(2019, 4, 15)
        tanaan = date.today()
        erotus = wabu - tanaan
        bot.send_message(chat_id=update.message.chat_id,
                         text=f'Wabun alkuun on {erotus.days} päivää', disable_notification=True)

    @staticmethod
    def kiitos(bot, update):
        print(update.message.chat_id)
        bot.send_message(chat_id=update.message.chat_id, text='Kiitos Jori', disable_notification=True)

    @staticmethod
    def sekseli(bot, update):
        text = 'Akseli sekseli guu nu kaijakka niko toivio sitä r elsa'
        bot.send_message(chat_id=update.message.chat_id, text=text, disable_notification=True)

    @staticmethod
    def pöytä(bot, update):
        bot.send_video(chat_id=update.message.chat_id, video=open('jorigif/poyta.mp4', 'rb'), disable_notification=True)

    @staticmethod
    def insv(bot, update):
        file_id = "CAADBAADqgADsnJvGjljGk2zOaJJAg"
        bot.send_sticker(chat_id=update.message.chat_id, sticker=file_id, disable_notification=True)

    @staticmethod
    def aikaTarkistus(viesti_aika):
        if datetime.today() - viesti_aika < timedelta(0, 30):
            return True
        else:
            return False

    def viimeKomentoTarkistus(self, komento, update, sekunnit=5):
        for msg in self.viim_kom[komento]:
            if msg.message.chat_id == update.message.chat_id:
                if datetime.today() - msg.message.date > timedelta(0, sekunnit):
                    self.viim_kom[komento].remove(msg)
                    self.viim_kom[komento].append(update)
                    return True
                else:
                    return False
        self.viim_kom[komento].append(update)
        return True

    def commandsHandler(self, bot, update):
        if not self.aikaTarkistus(update.message.date):
            return
        command = self.commandParser(update.message.text)
        if command not in self.commands:
            return
        if self.viimeKomentoTarkistus(command, update):
            self.commands[command](bot, update)

    @staticmethod
    def commandParser(teksti):
        command = ''
        for i in teksti:
            if i == ' ':
                break
            elif i != '/':
                command += i
        return command


if __name__ == '__main__':
    TelegramBot()
