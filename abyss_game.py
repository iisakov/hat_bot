from random import randint
from configuration import config


def filling_hat():
    with open('source/russian.txt') as ru:
        words = ru.readlines()
        while len(config.hat_words) < config.custom_options['num_words'] * config.custom_options['num_players']:
            config.hat_words.add(words[randint(1, len(words))][:-1])


def update_state():
    config.playrs_stat = {x: 0 for x in (config.custom_options['players'] if len(config.custom_options['players']) > 0 else config.default_options)}


def get_word():
    if len(config.hat_words) > 0:
        return config.hat_words.pop()
    else:
        return ':end:'


def get_num_word():
    return len(config.hat_words)
