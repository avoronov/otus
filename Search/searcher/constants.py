import copy

DEFAULT_SEARCH_RESULTS = 5
MAX_SEARCH_RESULTS = 50

SEARCH_ENGINE_YANDEX = 'yandex'
SEARCH_ENGINE_GOOGLE = 'google'

ALLOWED_SEARCH_ENGINES = {
   SEARCH_ENGINE_YANDEX: {
       "url": "https://www.yandex.ru/search/",
       "kwd": "text",
       "attrs": {"class": "organic__url"},
   },
   SEARCH_ENGINE_GOOGLE: {
       "url": "https://www.google.ru/search",
       "kwd": "q",
       "attrs": {"target": "_blank", "rel": "noopener"}
   },
}

def get_allowed_search_engines():
    return ALLOWED_SEARCH_ENGINES.keys()

def get_search_engine_settings(engine_name):
    assert engine_name in get_allowed_search_engines(), 'Bad engine given'
    settings = ALLOWED_SEARCH_ENGINES.get(engine_name)
    return copy.deepcopy(settings)