from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from itertools import chain

import json


class CD:
    def __init__(self, payload, mode):
        self.payload = payload
        self.mode = mode

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __iter__(self):
        yield from {
            "payload": self.payload,
            "mode": self.mode
        }.items()


def menu(list_menu):
    return ReplyKeyboardMarkup(list_menu, resize_keyboard=True)


def inline_menu(list_menu, mode, vert=False):
    list_ = []
    if vert:
        for i in list_menu:
            list_.append([InlineKeyboardButton(text=i,
                                               callback_data=str(CD(payload=i, mode=mode)))])
        return InlineKeyboardMarkup(list_)

    for i in list_menu:
        list_.append(InlineKeyboardButton(text=i,
                                          callback_data=str(CD(payload=i, mode=mode))))
    return InlineKeyboardMarkup([list_])


def reg_menu(list_menu):
    return f"^{'|'.join(list(chain.from_iterable(list_menu)))}$"
