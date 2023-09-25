import logging
from configuration.private_config import admin_name


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Состояние бота
class State:
    def __init__(self, state, menu):
        self.state = state
        self.menu = menu


MAIN = State(1, [['Бездонная шляпа'], ['Настройки игры'], ['Заземлиться']])
ABYSS = State(2, [['Начать'], ['Главное меню']])
GAME = State(3, [['Вытащить слово'], ['Заслуги', 'Сколько ещё слов'], ['Главное меню']])
OPTIONS = State(4, [['Настройки игроков'], ['Размер шляпы', 'Сложность', 'Время'], ['Главное меню']])
OPTIONS_PLAYERS = State(5, [['Добавить', 'Удалить', 'Заменить'], ['Рандомные аватарки'], ['Назад']])
ADMIN_OPTIONS_PLAYERS = State(5, [['Добавить', 'Удалить', 'Заменить'],
                                  ['Рандомные аватарки'],
                                  ['show', 'add', 'del'],
                                  ['Назад']])

# Настройки игры
default_options = {'num_players':   4,
                   'num_words':     10,
                   'players':       ['🌍', '😂', '😃', '🌦'],
                   'logins':        [admin_name],
                   'admins':        [admin_name]}

custom_options = {'num_players':    4,
                  'num_words':      10,
                  'players':        ['🌍', '😂', '😃', '🌦'],
                  'logins':         [admin_name],
                  'admins':         [admin_name]}

# Пул слов
hat_words = set()


#TODO Переделать статистику. Добавить статистику в cusomer_options.
# Так мы сможем добавлять новых игроков без перезаписи статистики.
# Счёт игроков
# Добавить возможность записи состояния для многих игр. Добавить sqlLite
playrs_stat = {x: 0 for x in (custom_options['players'] if len(custom_options['players']) > 0 else default_options)}
