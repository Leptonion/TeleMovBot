import threading
import time
from datetime import timedelta, date
from bot_core import Start, MainMenu, Search, Movie, TV, Bot, send_remind
from api_core import req
from dialog import lang
from reminder import set_data, get_list, session, RemList
import os

acc = Bot()
acc.set_key(os.environ.get('TBOT_KEY'))
req.set_key(os.environ.get('TMDB_KEY'))
bot = acc.get_bot()
trending_list = ['__trending_movie_day', '__trending_movie_week',
                 '__trending_tv_day', '__trending_tv_week']


def trending_choose(val):
    if val == '__trending_movie_day':
        return Search.trending_movie_day()
    elif val == '__trending_movie_week':
        return Search.trending_movie_week()
    elif val == '__trending_tv_day':
        return Search.trending_tv_day()
    elif val == '__trending_tv_week':
        return Search.trending_tv_week()


# First start handler
@bot.message_handler(commands=['start'])
def start(message):
    data = Start.dialog_start()

    check_poll = threading.Thread(target=check_process, args=(message.chat.id,), name='rem_checker')
    check_poll.start()

    bot.send_message(message.chat.id, text=data["message"], reply_markup=data["keyboard"])


# Main buttons handler
@bot.message_handler(content_types=["text"])
def main_btn_handler(message):
    if message.text == lang.language.button_menu:
        data = MainMenu.menu()
        req.list_current_page = 1
        bot.delete_message(message.chat.id, message_id=message.message_id)
        bot.send_message(message.chat.id, text=data["message"], reply_markup=data["keyboard"])

    elif message.text == lang.language.button_language:
        data = MainMenu.lang_change()
        bot.delete_message(message.chat.id, message_id=message.message_id)
        bot.send_message(message.chat.id, text=data["message"], reply_markup=data["keyboard"])


# Callback navigation handler
@bot.callback_query_handler(func=lambda call: True)
def inline_callback(call):
    if call.data == "search":
        data = Search.search_menu()
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(call.message.chat.id, text=data["message"], reply_markup=data["keyboard"])
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)

    elif call.data == "trending":
        data = Search.trending_menu()
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(call.message.chat.id, text=data["message"], reply_markup=data["keyboard"])
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)

    elif call.data == 'upcoming':
        data = Search.upcoming_movie()
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(call.message.chat.id, text=data["message"], reply_markup=data["keyboard"])
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)

    elif call.data == "search_movie":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        send = bot.send_message(chat_id=call.message.chat.id, text=lang.language.message_search_request_movie)
        bot.register_next_step_handler(send, search_list_movie)

    elif call.data == "search_tv":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        send = bot.send_message(chat_id=call.message.chat.id, text=lang.language.message_search_request_tv)
        bot.register_next_step_handler(send, search_list_tv)

    elif call.data == "trending_movie":
        data = Search.trending_movie_menu()
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(call.message.chat.id, text=data["message"], reply_markup=data["keyboard"])
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)

    elif call.data == "trending_tv":
        data = Search.trending_tv_menu()
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(call.message.chat.id, text=data["message"], reply_markup=data["keyboard"])
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)

    elif '__'+call.data in trending_list:
        data = trending_choose('__'+call.data)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, text=data['message'], reply_markup=data["keyboard"])

    elif call.data.split('==')[0] == "movie_list_up":
        req.list_current_page += 1
        if call.data.split('==')[1] in trending_list:
            data = trending_choose(call.data.split('==')[1])
        elif call.data.split('==')[1] == 'upcoming_movie':
            data = Search.upcoming_movie()
        else:
            data = Search.search_movie(call.data.split('==')[1])
        bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(call.message.chat.id, text=data["message"], reply_markup=data["keyboard"])
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)

    elif call.data.split('==')[0] == "movie_list_down":
        req.list_current_page -= 1
        if call.data.split('==')[1] in trending_list:
            data = trending_choose(call.data.split('==')[1])
        elif call.data.split('==')[1] == 'upcoming_movie':
            data = Search.upcoming_movie()
        else:
            data = Search.search_movie(call.data.split('==')[1])
        bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(call.message.chat.id, text=data["message"], reply_markup=data["keyboard"])
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)

    elif call.data.split('==')[0] == "view_movie_id":
        data = Movie.mov_from_id(call.data.split('==')[1])
        bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(chat_id=call.message.chat.id, text=data['message'],
                             reply_markup=data["keyboard"], parse_mode='MarkdownV2')
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)

    elif call.data.split('==')[0] == "tv_list_up":
        req.list_current_page += 1
        if call.data.split('==')[1] in trending_list:
            data = trending_choose(call.data.split('==')[1])
        else:
            data = Search.search_tv(call.data.split('==')[1])
        bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(call.message.chat.id, text=data["message"], reply_markup=data["keyboard"])
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)

    elif call.data.split('==')[0] == "tv_list_down":
        req.list_current_page -= 1
        if call.data.split('==')[1] in trending_list:
            data = trending_choose(call.data.split('==')[1])
        else:
            data = Search.search_tv(call.data.split('==')[1])
        bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(call.message.chat.id, text=data["message"], reply_markup=data["keyboard"])
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)

    elif call.data.split('==')[0] == "view_tv_id":
        data = TV.tv_from_id(call.data.split('==')[1])
        bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(chat_id=call.message.chat.id, text=data['message'],
                             reply_markup=data["keyboard"], parse_mode='MarkdownV2')
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)

    elif call.data == "back_to_list":
        data = Search.last_list
        bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(call.message.chat.id, text=data["message"], reply_markup=data["keyboard"])
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)

    elif call.data.split('==')[0] == "language_change":
        lang.set_lang(call.data.split('==')[1])
        data = Start.dialog_start()
        bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, text=data["message"], reply_markup=data['keyboard'])

    elif call.data == 'tracking':
        data = Search.tracking_list(get_list())
        bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(call.message.chat.id, text=data["message"], reply_markup=data["keyboard"])
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)

    elif call.data.split('==')[0] == 'mov_track':
        data = req.get_movie_details(call.data.split('==')[1])
        set_data(mov_id=call.data.split('==')[1],
                 release_date=data['release_date'].replace('\\', ''),
                 mov_tittle=data['title'])
        data = Search.last_list
        bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        if data:
            bot.send_message(call.message.chat.id, text=data["message"], reply_markup=data["keyboard"])
        else:
            bot.send_message(call.message.chat.id, text=lang.language.message_error_api)


#  Next step handlers
def search_list_movie(message):
    data = Search.search_movie(message.text)
    bot.delete_message(message.chat.id, message_id=message.message_id)
    bot.delete_message(message.chat.id, message_id=message.message_id-1)
    if data:
        bot.send_message(chat_id=message.chat.id, text=data["message"], reply_markup=data["keyboard"])
    else:
        bot.send_message(chat_id=message.chat.id, text=lang.language.message_error_api)


def search_list_tv(message):
    data = Search.search_tv(message.text)
    bot.delete_message(message.chat.id, message_id=message.message_id)
    bot.delete_message(message.chat.id, message_id=message.message_id-1)
    if data:
        bot.send_message(chat_id=message.chat.id, text=data["message"], reply_markup=data["keyboard"])
    else:
        bot.send_message(chat_id=message.chat.id, text=lang.language.message_error_api)


# Checker polling (threaded)
def check_process(mess_id):
    while True:
        today_date = date.today()
        print('Check!')
        data = session.query(RemList).filter_by(release_date=today_date + timedelta(days=7)).all()
        for i in data:
            if i.remember == 3:
                i.remember -= 1
                session.commit()
                send_remind(i.mov_id, 3, mess_id)

        data = session.query(RemList).filter_by(release_date=today_date + timedelta(days=3)).all()
        for i in data:
            if i.remember == 2:
                i.remember -= 1
                session.commit()
                send_remind(i.mov_id, 2, mess_id)

        data = session.query(RemList).filter_by(release_date=today_date).all()
        for i in data:
            if i.remember == 1:
                send_remind(i.mov_id, 1, mess_id)
                session.delete(i)
                session.commit()

        time.sleep(10800)


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(5)
