import telebot
from telebot import types
from api_core import req
from dialog import lang
from reminder import check_date


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Bot(metaclass=Singleton):
    def __init__(self):
        self.__key = None

    def set_key(self, key: str):
        self.__key = key

    def get_bot(self):
        return telebot.TeleBot(self.__key, num_threads=5)


acc = Bot()
bot = acc.get_bot()


# Bot starter
class Start:

    @staticmethod
    def dialog_start():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(text=lang.language.button_menu),
                   types.KeyboardButton(text=lang.language.button_language)]
        keyboard.add(*buttons)
        message = lang.language.message_main
        return {"message": message, "keyboard": keyboard}


# Main panel buttons
class MainMenu:

    @staticmethod
    def menu():
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=lang.language.button_menu_search, callback_data="search"),
                   types.InlineKeyboardButton(text=lang.language.button_menu_trending, callback_data="trending"),
                   types.InlineKeyboardButton(text=lang.language.button_menu_upcoming, callback_data="upcoming"),
                   types.InlineKeyboardButton(text=lang.language.button_tracking, callback_data="tracking")]
        keyboard.add(*buttons)
        message = lang.language.message_menu
        return {"message": message, "keyboard": keyboard}

    @staticmethod
    def lang_change():
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text='English', callback_data="language_change==en"),
                   types.InlineKeyboardButton(text='Русский', callback_data="language_change==ru"),
                   types.InlineKeyboardButton(text='Українська', callback_data="language_change==ua")]
        for x in buttons:
            keyboard.add(x)
        message = lang.language.lang_ask
        return {"message": message, "keyboard": keyboard}


# Main navigation class
class Search:
    last_list = None

    @staticmethod
    def search_menu():
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=lang.language.button_search_movie, callback_data="search_movie"),
                   types.InlineKeyboardButton(text=lang.language.button_search_tv, callback_data="search_tv")]
        keyboard.add(*buttons)
        message = lang.language.message_search
        return {"message": message, "keyboard": keyboard}

    @staticmethod
    def trending_menu():
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=lang.language.button_search_movie, callback_data='trending_movie'),
                   types.InlineKeyboardButton(text=lang.language.button_search_tv, callback_data='trending_tv')]
        keyboard.add(*buttons)
        message = lang.language.message_trending
        return {"message": message, "keyboard": keyboard}

    @staticmethod
    def search_movie(val: str):
        api_res = req.get_movie_search(val)
        if not api_res:
            return None
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=f"{x['title']} ({x['release_date'][0:4]})",
                                              callback_data=f"view_movie_id=={x['id']}") for x in api_res["results"]]
        for i in buttons:
            keyboard.add(i)
        if api_res['total_pages'] == 1:
            ...
        elif req.list_current_page == 1:
            keyboard.add(types.InlineKeyboardButton(text=">", callback_data=f"movie_list_up=={val}"))
        elif req.list_current_page == api_res['total_pages']:
            keyboard.add(types.InlineKeyboardButton(text="<", callback_data=f"movie_list_down=={val}"))
        else:
            keyboard.add(*[types.InlineKeyboardButton(text="<", callback_data=f"movie_list_down=={val}"),
                           types.InlineKeyboardButton(text=">", callback_data=f"movie_list_up=={val}")])
        message = f"{lang.language.message_search_response} {val}\n{lang.language.message_pages} " \
                  f"{api_res['page']}/{api_res['total_pages']}"
        Search.last_list = {"message": message, "keyboard": keyboard}
        return {"message": message, "keyboard": keyboard}

    @staticmethod
    def search_tv(val: str):
        api_res = req.get_tv_search(val)
        if not api_res:
            return None
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=f"{x['name']} ({x['first_air_date'][0:4]})",
                                              callback_data=f"view_tv_id=={x['id']}") for x in api_res["results"]]
        for i in buttons:
            keyboard.add(i)
        if api_res['total_pages'] == 1:
            ...
        elif req.list_current_page == 1:
            keyboard.add(types.InlineKeyboardButton(text=">", callback_data=f"tv_list_up=={val}"))
        elif req.list_current_page == api_res['total_pages']:
            keyboard.add(types.InlineKeyboardButton(text="<", callback_data=f"tv_list_down=={val}"))
        else:
            keyboard.add(*[types.InlineKeyboardButton(text="<", callback_data=f"tv_list_down=={val}"),
                           types.InlineKeyboardButton(text=">", callback_data=f"tv_list_up=={val}")])
        message = f"{lang.language.message_search_response} {val}\n{lang.language.message_pages} " \
                  f"{api_res['page']}/{api_res['total_pages']}"
        Search.last_list = {"message": message, "keyboard": keyboard}
        return {"message": message, "keyboard": keyboard}

    @staticmethod
    def trending_movie_menu():
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=lang.language.button_trending_day,
                                              callback_data="trending_movie_day"),
                   types.InlineKeyboardButton(text=lang.language.button_trending_week,
                                              callback_data="trending_movie_week")]
        keyboard.add(*buttons)
        message = lang.language.message_trending_movie
        return {"message": message, "keyboard": keyboard}

    @staticmethod
    def trending_tv_menu():
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=lang.language.button_trending_day, callback_data="trending_tv_day"),
                   types.InlineKeyboardButton(text=lang.language.button_trending_week,
                                              callback_data="trending_tv_week")]
        keyboard.add(*buttons)
        message = lang.language.message_trending_tv
        return {"message": message, "keyboard": keyboard}

    @staticmethod
    def upcoming_movie():
        val = 'upcoming_movie'
        api_res = req.get_movie_upcoming()
        if not api_res:
            return None
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=f"{x['title']} ({x['release_date'][0:4]})",
                                              callback_data=f"view_movie_id=={x['id']}") for x in api_res["results"]]
        for i in buttons:
            keyboard.add(i)
        if api_res['total_pages'] == 1:
            ...
        elif req.list_current_page == 1:
            keyboard.add(types.InlineKeyboardButton(text=">", callback_data=f"movie_list_up=={val}"))
        elif req.list_current_page == api_res['total_pages']:
            keyboard.add(types.InlineKeyboardButton(text="<", callback_data=f"movie_list_down=={val}"))
        else:
            keyboard.add(*[types.InlineKeyboardButton(text="<", callback_data=f"movie_list_down=={val}"),
                           types.InlineKeyboardButton(text=">", callback_data=f"movie_list_up=={val}")])
        message = f"{lang.language.message_upcoming_movie} \n{lang.language.message_pages} " \
                  f"{api_res['page']}/{api_res['total_pages']}"
        Search.last_list = {"message": message, "keyboard": keyboard}
        return {"message": message, "keyboard": keyboard}

    @staticmethod
    def trending_movie_day():
        val = '__trending_movie_day'
        api_res = req.get_movie_trending_day()
        if not api_res:
            return None
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=f"{x['title']} ({x['release_date'][0:4]})",
                                              callback_data=f"view_movie_id=={x['id']}") for x in api_res["results"]]
        for i in buttons:
            keyboard.add(i)
        if api_res['total_pages'] == 1:
            ...
        elif req.list_current_page == 1:
            keyboard.add(types.InlineKeyboardButton(text=">", callback_data=f"movie_list_up=={val}"))
        elif req.list_current_page == api_res['total_pages']:
            keyboard.add(types.InlineKeyboardButton(text="<", callback_data=f"movie_list_down=={val}"))
        else:
            keyboard.add(*[types.InlineKeyboardButton(text="<", callback_data=f"movie_list_down=={val}"),
                           types.InlineKeyboardButton(text=">", callback_data=f"movie_list_up=={val}")])
        message = f"{lang.language.message_trending_response}\n{lang.language.message_pages} " \
                  f"{api_res['page']}/{api_res['total_pages']}"
        Search.last_list = {"message": message, "keyboard": keyboard}
        return {"message": message, "keyboard": keyboard}

    @staticmethod
    def trending_movie_week():
        val = '__trending_movie_week'
        api_res = req.get_movie_trending_week()
        if not api_res:
            return None
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=f"{x['title']} ({x['release_date'][0:4]})",
                                              callback_data=f"view_movie_id=={x['id']}") for x in api_res["results"]]
        for i in buttons:
            keyboard.add(i)
        if api_res['total_pages'] == 1:
            ...
        elif req.list_current_page == 1:
            keyboard.add(types.InlineKeyboardButton(text=">", callback_data=f"movie_list_up=={val}"))
        elif req.list_current_page == api_res['total_pages']:
            keyboard.add(types.InlineKeyboardButton(text="<", callback_data=f"movie_list_down=={val}"))
        else:
            keyboard.add(*[types.InlineKeyboardButton(text="<", callback_data=f"movie_list_down=={val}"),
                           types.InlineKeyboardButton(text=">", callback_data=f"movie_list_up=={val}")])
        message = f"{lang.language.message_trending_response}\n{lang.language.message_pages} " \
                  f"{api_res['page']}/{api_res['total_pages']}"
        Search.last_list = {"message": message, "keyboard": keyboard}
        return {"message": message, "keyboard": keyboard}

    @staticmethod
    def trending_tv_day():
        val = '__trending_tv_day'
        api_res = req.get_tv_trending_day()
        if not api_res:
            return None
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=f"{x['name']} ({x['first_air_date'][0:4]})",
                                              callback_data=f"view_tv_id=={x['id']}") for x in api_res["results"]]
        for i in buttons:
            keyboard.add(i)
        if api_res['total_pages'] == 1:
            ...
        elif req.list_current_page == 1:
            keyboard.add(types.InlineKeyboardButton(text=">", callback_data=f"tv_list_up=={val}"))
        elif req.list_current_page == api_res['total_pages']:
            keyboard.add(types.InlineKeyboardButton(text="<", callback_data=f"tv_list_down=={val}"))
        else:
            keyboard.add(*[types.InlineKeyboardButton(text="<", callback_data=f"tv_list_down=={val}"),
                           types.InlineKeyboardButton(text=">", callback_data=f"tv_list_up=={val}")])
        message = f"{lang.language.message_trending_response}\n{lang.language.message_pages} " \
                  f"{api_res['page']}/{api_res['total_pages']}"
        Search.last_list = {"message": message, "keyboard": keyboard}
        return {"message": message, "keyboard": keyboard}

    @staticmethod
    def trending_tv_week():
        val = '__trending_tv_week'
        api_res = req.get_tv_trending_week()
        if not api_res:
            return None
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=f"{x['name']} ({x['first_air_date'][0:4]})",
                                              callback_data=f"view_tv_id=={x['id']}") for x in api_res["results"]]
        for i in buttons:
            keyboard.add(i)
        if api_res['total_pages'] == 1:
            ...
        elif req.list_current_page == 1:
            keyboard.add(types.InlineKeyboardButton(text=">", callback_data=f"tv_list_up=={val}"))
        elif req.list_current_page == api_res['total_pages']:
            keyboard.add(types.InlineKeyboardButton(text="<", callback_data=f"tv_list_down=={val}"))
        else:
            keyboard.add(*[types.InlineKeyboardButton(text="<", callback_data=f"tv_list_down=={val}"),
                           types.InlineKeyboardButton(text=">", callback_data=f"tv_list_up=={val}")])
        message = f"{lang.language.message_trending_response}\n{lang.language.message_pages} " \
                  f"{api_res['page']}/{api_res['total_pages']}"
        Search.last_list = {"message": message, "keyboard": keyboard}
        return {"message": message, "keyboard": keyboard}

    @staticmethod
    def tracking_list(data):
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=f'{x.mov_tittle} ({x.release_date})',
                                              callback_data=f"view_movie_id=={x.mov_id}") for x in data]
        for i in buttons:
            keyboard.add(i)
        message = 'Tracking list:'
        Search.last_list = {"message": message, "keyboard": keyboard}
        return {"message": message, "keyboard": keyboard}


# Movie working class
class Movie:

    @staticmethod
    def mov_from_id(mov_id):
        data = req.get_movie_details(mov_id)
        if not data:
            return None
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=lang.language.button_movie_trailer, url=data['trailer']),
                   types.InlineKeyboardButton(text=lang.language.button_movie_imdb, url=data['imdb']),
                   types.InlineKeyboardButton(text=lang.language.button_movie_track,
                                              callback_data=f"mov_track=={mov_id}"),
                   types.InlineKeyboardButton(text=lang.language.button_list_back, callback_data="back_to_list")]
        if not check_date(data['release_date'], mov_id):
            buttons.pop(2)
        for i in buttons:
            if i.url != 'Empty':
                keyboard.add(i)
        message = f"*{data['title']}*\n" \
                  f"{data['release_date']}\n\n" \
                  f"{data['genres']}\n\n" \
                  f"{lang.language.message_all_overview} {data['overview']}\n\n" \
                  f"[{lang.language.message_all_poster}]({data['poster']})"
        return {"message": message, "keyboard": keyboard}


# TV series working class
class TV:

    @staticmethod
    def tv_from_id(tv_id):
        data = req.get_tv_details(tv_id)
        if not data:
            return None
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=lang.language.button_movie_trailer, url=data['trailer']),
                   types.InlineKeyboardButton(text=lang.language.button_list_back, callback_data="back_to_list")]
        for i in buttons:
            if i.url != 'Empty':
                keyboard.add(i)
        message = f"*{data['title']}*\n" \
                  f"{data['release_date']}\n\n" \
                  f"{data['genres']}\n\n" \
                  f"{lang.language.message_tv_seasons} {data['seasons_count']}\n\n" \
                  f"{lang.language.message_tv_status} {data['status']}\n\n" \
                  f"{lang.language.message_all_overview} \n{data['overview']}\n\n" \
                  f"[{lang.language.message_all_poster}]({data['poster']})"
        return {"message": message, "keyboard": keyboard}


# Sender funtion for remind checker!
def send_remind(mov_id: str, interval: int, mess_id):
    bot = acc.get_bot()  # Not good - but it working))
    message_tittle = {1: lang.language.message_reminder_first,
                      2: lang.language.message_reminder_second,
                      3: lang.language.message_reminder_third}
    data = req.get_movie_details(mov_id)
    try:
        keyboard = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text=lang.language.button_movie_trailer, url=data['trailer']),
                   types.InlineKeyboardButton(text=lang.language.button_movie_imdb, url=data['imdb'])]
        for i in buttons:
            if i.url != 'Empty':
                keyboard.add(i)
        message = f"{message_tittle[interval]}\n\n" \
                  f"*{data['title']}*\n" \
                  f"{data['release_date']}\n\n" \
                  f"{data['genres']}\n\n" \
                  f"{lang.language.message_all_overview} {data['overview']}\n\n" \
                  f"[{lang.language.message_all_poster}]({data['poster']})"
        bot.send_message(mess_id, text=message, reply_markup=keyboard, parse_mode='MarkdownV2')
    except Exception as e:
        print(e)
