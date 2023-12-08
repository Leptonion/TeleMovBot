from dataclasses import dataclass


class Language:
    def __init__(self):
        self.lang_dict = {'en': English, 'ru': Russian, 'ua': Ukraine}
        self.language = English

    def set_lang(self, keyword: str):
        if keyword in self.lang_dict.keys():
            self.language = self.lang_dict[keyword]


# Language dataclasses

@dataclass
class English:
    keyword = 'en'
    lang_ask = 'Choose language:'
    message_main = 'Welcome to the personal bot Kinoman.\nI will help you find movies and TV series.\n ' \
                   'I\'m waiting for your instructions!'
    button_menu = 'Menu'
    button_language = 'Language'
    message_menu = 'Select an item'
    button_menu_search = 'Search'
    button_menu_trending = 'Trending'
    button_menu_upcoming = 'Upcoming'
    message_trending_movie = 'Movie trending:'
    message_trending_tv = 'TV trending:'
    message_upcoming_movie = 'New Upcoming movies:'
    button_trending_day = 'Today'
    button_trending_week = 'Week'
    message_trending = 'Trending:'
    message_search = 'Search:'
    button_search_movie = 'Movie'
    button_search_tv = 'TV'
    message_search_request_movie = 'Enter movie title:\n' \
                                   '(Please enter your search term in response to this message!)'
    message_search_response = 'Search result:'
    message_trending_response = 'Trending result:'
    message_pages = 'Page.'
    button_movie_trailer = 'Trailer'
    button_movie_imdb = 'IMDB'
    button_list_back = 'Back to list'
    message_search_request_tv = 'Enter the TV title:\n' \
                                '(Please enter your search term in response to this message!)'
    message_all_overview = 'Overview:'
    message_all_poster = 'Poster'
    message_tv_seasons = 'Seasons:'
    message_tv_status = 'Status:'
    message_tv_status_ended = 'Ended'
    message_tv_status_ongoing = 'Ongoing'
    button_movie_track = 'Track'
    button_tracking = 'Tracking'
    message_reminder_first = '*Coming out today:*'
    message_reminder_second = '*Coming out in 3 days:*'
    message_reminder_third = '*Coming out in 7 days:*'
    message_error_api = 'Error:\nSomething went wrong! Try repeating your request.'


@dataclass
class Russian:
    keyword = 'ru'
    lang_ask = 'Выберите язык:'
    message_main = 'Вас приветствует персональный бот Киноман.\nЯ помогу вам с поиском фильмов и сериалов.\n ' \
                   'Жду ваших указаний!'
    button_menu = 'Меню'
    button_language = 'Язык'
    message_menu = 'Основное меню:'
    button_menu_search = 'Поиск'
    button_menu_trending = 'Тренды'
    button_menu_upcoming = 'Скоро'
    message_trending_movie = 'Фильмы в тренде:'
    message_trending_tv = 'Сериалы в тренде:'
    message_upcoming_movie = 'Новые фильмы, скоро:'
    button_trending_day = 'Сегодня'
    button_trending_week = 'За неделю'
    message_trending = 'Тренды:'
    message_search = 'Поиск:'
    button_search_movie = 'Фильм'
    button_search_tv = 'Сериал'
    message_search_request_movie = 'Введите название фиьма:\n ' \
                                   '(Пожалуйста введите ваш поисковый запрос в ответ на это сообщение!)'
    message_search_response = 'Результат по поиску:'
    message_trending_response = 'Результат трендов:'
    message_pages = 'Стр.'
    button_movie_trailer = 'Трейлер'
    button_movie_imdb = 'IMDB'
    button_list_back = 'Назад к списку'
    message_search_request_tv = 'Введите название сериала:\n' \
                                '(Пожалуйста введите ваш поисковый запрос в ответ на это сообщение!)'
    message_all_overview = 'Описание:'
    message_all_poster = 'Постер'
    message_tv_seasons = 'Сезонов:'
    message_tv_status = 'Выход серий:'
    message_tv_status_ended = 'Завершён'
    message_tv_status_ongoing = 'Продолжается'
    button_movie_track = 'Отслеживать'
    button_tracking = 'Отслеживание'
    message_reminder_first = '*Выйдет сегодня:*'
    message_reminder_second = '*Выйдет через 3 дня:*'
    message_reminder_third = '*Выйдет через 7 дней:*'
    message_error_api = 'Ошибка:\nЧто-то пошло не так! Попробуйте повторить ваш запрос.'


@dataclass
class Ukraine:
    keyword = 'ua'
    lang_ask = 'Виберіть мову:'
    message_main = 'Вас вітає персональний бот Кіноман.\nЯ допоможу вам з пошуком фільмів та серіалів.\n ' \
                   'Чекаю ваших вказівок!'
    button_menu = 'Меню'
    button_language = 'Мова'
    message_menu = 'Виберіть пункт'
    button_menu_search = 'Пошук'
    button_menu_trending = 'Тренди'
    button_menu_upcoming = 'Незабаром'
    message_trending_movie = 'Фільми в тренді:'
    message_trending_tv = 'Серіали в тренді:'
    message_upcoming_movie = 'Нові фільми, незабаром:'
    button_trending_day = 'Сьогодні'
    button_trending_week = 'За тиждень'
    message_trending = 'Тренди:'
    message_search = 'Пошук:'
    button_search_movie = 'Фільм'
    button_search_tv = 'Серіал'
    message_search_request_movie = 'Введіть назву фільму:\n ' \
                                   '(Будь ласка введіть ваш пошуковий запит у відповідь на це повідомлення!)'
    message_search_response = 'Результат пошуку:'
    message_trending_response = 'Результат трендів:'
    message_pages = 'Стор.'
    button_movie_trailer = 'Трейлер'
    button_movie_imdb = 'IMDB'
    button_list_back = 'Назад до списку'
    message_search_request_tv = 'Введіть назву серіалу:\n' \
                                '(Будь ласка введіть ваш пошуковий запит у відповідь на це повідомлення!)'
    message_all_overview = 'Опис:'
    message_all_poster = 'Постер'
    message_tv_seasons = 'Сезонів:'
    message_tv_status = 'Вихід серій:'
    message_tv_status_ended = 'Закінчився'
    message_tv_status_ongoing = 'Продовжується'
    button_movie_track = 'Слідкувати'
    button_tracking = 'Відслідковування'
    message_reminder_first = '*Вийде сьогодні:*'
    message_reminder_second = '*Вийде через 3 дня:*'
    message_reminder_third = '*Вийде через 7 днів:*'
    message_error_api = 'Помилка:\nЩось пішло не так! Спробуйте повторити ваш запит.'


lang = Language()
