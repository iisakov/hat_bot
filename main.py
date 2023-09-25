import abyss_game
import json

from STL import render, grounder, optioner
from configuration import config, private_config

from telegram import Update
from telegram.ext import (filters, MessageHandler, CallbackQueryHandler, ApplicationBuilder, ContextTypes,
                          CommandHandler, ConversationHandler)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username in config.custom_options['logins']:
        config.custom_options = config.default_options
        config.custom_options['players'] = optioner.get_emoji_list(4)
        await update.message.reply_text(f'd')  # TODO Добиться получения всех пользователей чата
        await update.message.reply_text(f'Привет, {update.effective_user.first_name}! Давай сыграем.',
                                        reply_markup=render.menu(config.MAIN.menu))
        return config.MAIN.state
    else:
        await update.message.reply_text(f'Привет, {update.effective_user.first_name}! Ты кто?.')


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Бездонная шляпа':
        await update.message.reply_text(f'Переключаюсь на {update.message.text}',
                                        reply_markup=render.menu(config.ABYSS.menu))
        return config.ABYSS.state

    if update.message.text == 'Настройки игры':
        await update.message.reply_text(f'Переключаюсь на {update.message.text}',
                                        reply_markup=render.menu(config.OPTIONS.menu))
        return config.OPTIONS.state

    if update.message.text == 'Заземлиться':
        grounder.p_stat()
        await update.message.reply_text(f'Начинаем с чистого листа, все заслуги заземлены')


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Вытащить слово':
        await update.message.reply_text(f"{abyss_game.get_word()}",
                                        reply_markup=render.inline_menu(list_menu=config.custom_options['players'],
                                                                        mode='view_word'))
        return config.GAME.state

    if update.message.text == 'Заслуги':
        for p_kay, p_values in config.playrs_stat.items():
            await update.message.reply_text(f'{p_kay}: {p_values}')

    if update.message.text == 'Главное меню':
        await update.message.reply_text(text=f'Переключаюсь на {update.message.text}',
                                        reply_markup=render.menu(config.MAIN.menu))
        return config.MAIN.state

    if update.message.text == 'Сколько ещё слов':
        await update.message.reply_text(f'В шляпе {abyss_game.get_num_word()} слов.')


async def players_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = json.loads(query.data)
    message = query.message
    config.playrs_stat[data['payload']] += 1
    await query.edit_message_text(text=f"'{message.text}' -> {data['payload']}")


async def options_player_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = json.loads(query.data)
    if data['mode'] == 'add':
        config.custom_options['players'].append(data['payload'])
        config.custom_options['num_players'] += 1
        await query.edit_message_text(text=f"Список игроков: {'  '.join(config.custom_options['players'])}")

    if data['mode'] == 'del':
        config.custom_options['players'].remove(data['payload'])
        config.custom_options['num_players'] -= 1
        await query.edit_message_text(text=f"Список игроков: {'  '.join(config.custom_options['players'])}")

    if data['mode'] == 'replace':
        config.custom_options['players'].remove(data['payload'])
        config.custom_options['players'].append(optioner.get_emoji())
        await query.edit_message_text(text=f"Список игроков: {'  '.join(config.custom_options['players'])}")

    if data['mode'] == 'login_del':
        config.custom_options['logins'].remove(data['payload'])
        await query.edit_message_text(text=f"login list: {'  '.join(config.custom_options['logins'])}")


async def word_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = json.loads(query.data)

    if data['mode'] == 'num':
        config.custom_options['num_words'] = data['payload']
        await query.edit_message_text(text=f"Слов в шляпе будет: {config.custom_options['num_words'] * config.custom_options['num_players']}")


async def abyss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Начать':
        abyss_game.filling_hat()
        abyss_game.update_state()
        await update.message.reply_text(f'Переключаюсь на {update.message.text}',
                                        reply_markup=render.menu(config.GAME.menu))
        return config.GAME.state

    if update.message.text == 'Главное меню':
        await update.message.reply_text(f'Переключаюсь на {update.message.text}',
                                        reply_markup=render.menu(config.MAIN.menu))
        return config.MAIN.state


async def options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Настройки игроков':

        if update.effective_user.username in config.custom_options['admins']:
            await update.message.reply_text(f'Переключаюсь на {update.message.text}',
                                            reply_markup=render.menu(config.ADMIN_OPTIONS_PLAYERS.menu))
            return config.ADMIN_OPTIONS_PLAYERS.state
        else:
            await update.message.reply_text(f'Переключаюсь на {update.message.text}',
                                        reply_markup=render.menu(config.OPTIONS_PLAYERS.menu))
            return config.OPTIONS_PLAYERS.state

    if update.message.text == 'Сложность':
        await update.message.reply_text(f'Мы работаем над этим')

    if update.message.text == 'Время':
        await update.message.reply_text(f'Мы работаем над этим')

    if update.message.text == 'Размер шляпы':
        await update.message.reply_text(f'Сколько слов на игрока',
                                        reply_markup=render.inline_menu(list_menu=[5, 10, 15, 20],
                                                                        mode='num'))

    if update.message.text == 'Главное меню':
        await update.message.reply_text(f'Переключаюсь на {update.message.text}',
                                        reply_markup=render.menu(config.MAIN.menu))
        return config.MAIN.state


async def options_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Добавить':
        await update.message.reply_text(f"Какой аватар добавить?",
                                        reply_markup=render.inline_menu(list_menu=optioner.get_emoji_list(4),
                                                                        mode='add'))

    if update.message.text == 'Удалить':
        await update.message.reply_text(f"Кого будем удалять?",
                                        reply_markup=render.inline_menu(list_menu=config.custom_options['players'],
                                                                        mode='del'))

    if update.message.text == 'Заменить':
        await update.message.reply_text(f"Кого будем заменять?",
                                        reply_markup=render.inline_menu(list_menu=config.custom_options['players'],
                                                                        mode='replace'))

    if update.message.text == 'Рандомные аватарки':
        config.custom_options['players'] = optioner.get_emoji_list(len(config.custom_options['players']))
        await update.message.reply_text(text=f"Список игроков: {'  '.join(config.custom_options['players'])}")

    if update.message.text == 'Назад':
        await update.message.reply_text(f'Переключаюсь на {update.message.text}',
                                        reply_markup=render.menu(config.OPTIONS.menu))
        return config.OPTIONS.state

    if update.message.text == 'show':
        print(update.message.text)
        await update.message.reply_text(text=f"login list: {'  '.join(config.custom_options['logins'])}")
        await update.message.reply_text(text=f"admin list: {'  '.join(config.custom_options['admins'])}")

    if update.message.text == 'add':
        await update.message.reply_text(text=f"type: '/loginAdd' and username")

    if update.message.text == 'del':
        await update.message.reply_text(f"Кого будем удалять?",
                                        reply_markup=render.inline_menu(list_menu=config.custom_options['logins'],
                                                                        mode='login_del',
                                                                        vert=True))


async def login_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username in config.custom_options['admins']:
        for login in update.message.text.split(" ")[1:]:
            config.custom_options['logins'].append(login)
        await update.message.reply_text(text=f"login list: {', '.join(config.custom_options['logins'])}")


if __name__ == '__main__':
    application = ApplicationBuilder().token(private_config.token).build()

    handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            config.MAIN.state:              [MessageHandler(filters.Regex(render.reg_menu(config.MAIN.menu)), main_menu),
                                             CommandHandler("start", start)],
            config.ABYSS.state:             [MessageHandler(filters.Regex(render.reg_menu(config.ABYSS.menu)), abyss),
                                             CommandHandler("start", start)],
            config.OPTIONS.state:           [MessageHandler(filters.Regex(render.reg_menu(config.OPTIONS.menu)), options),
                                             CallbackQueryHandler(word_button),
                                             CommandHandler("start", start)],
            config.GAME.state:              [MessageHandler(filters.Regex(render.reg_menu(config.GAME.menu)), game),
                                             CallbackQueryHandler(players_button),
                                             CommandHandler("start", start)],
            config.OPTIONS_PLAYERS.state:   [MessageHandler(filters.Regex(render.reg_menu(config.OPTIONS_PLAYERS.menu + config.ADMIN_OPTIONS_PLAYERS.menu)), options_players),
                                             CallbackQueryHandler(options_player_button),
                                             CommandHandler("loginAdd", login_add),
                                             CommandHandler("start", start)
                                             ]},
        fallbacks=[]
    )
    application.add_handler(handler)

    application.run_polling()
