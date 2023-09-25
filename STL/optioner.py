import emoji
from random import randint

from configuration.config import custom_options


def get_emoji_list(num):
    result = []
    while len(result) < num:
        current_emoji = list(emoji.EMOJI_DATA.keys())[randint(0, len(emoji.EMOJI_DATA.keys()))]
        if current_emoji not in custom_options['players']:
            result.append(list(emoji.EMOJI_DATA.keys())[randint(0, len(emoji.EMOJI_DATA.keys()))])
    return result


def get_emoji():
    result = list(emoji.EMOJI_DATA.keys())[randint(0, len(emoji.EMOJI_DATA.keys()))]
    while result in custom_options['players']:
        result = list(emoji.EMOJI_DATA.keys())[randint(0, len(emoji.EMOJI_DATA.keys()))]
    return result
