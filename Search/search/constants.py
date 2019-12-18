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
