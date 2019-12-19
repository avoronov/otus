from bs4 import BeautifulSoup
import copy
import logging
import re
from requests import get, codes
from requests.exceptions import HTTPError, RequestException
from urllib.parse import (
    urlparse,
    urlunparse
)

from .constants import *
from .exceptions import *
from .log_utils import *


LOG = get_logger()

def _yandex_url_sanitize(href):
    url = urlparse(href)
    url = url._replace(params="", query="", fragment="")
    return urlunparse(url)

def _google_url_sanitize(href):
    href = re.sub("^(.*)(?=https?\:\/\/)", "", href)

    url = urlparse(href)
    url = url._replace(params="", query="", fragment="")

    return urlunparse(url)

ALLOWED_SEARCH_ENGINES = {
   SEARCH_ENGINE_YANDEX: {
       "url": "https://www.yandex.ru/search/",
       "kwd": "text",
       "attrs": {"class": "organic__url"},
       "url_sanitizer": _yandex_url_sanitize,
   },
   SEARCH_ENGINE_GOOGLE: {
       "url": "https://www.google.ru/search",
       "kwd": "q",
       "attrs": {"target": "_blank", "rel": "noopener"},
       "url_sanitizer": _google_url_sanitize,
   },
}

def _get_allowed_search_engines():
    return ALLOWED_SEARCH_ENGINES.keys()

def _get_search_engine_settings(engine_name, set_name):
    assert engine_name in _get_allowed_search_engines(), 'Bad engine given'
    return ALLOWED_SEARCH_ENGINES.get(engine_name)[set_name]

def _validate_args(theme, engine, count):
    LOG.debug("func _validate_args(theme='{}', engine='{}', count={}) started".format(theme, engine, count))

    if theme is None or len(theme) < 1:
        raise NoThemeToSearch("No theme to search given")

    allowed_search_engines = _get_allowed_search_engines()
    if engine not in allowed_search_engines:
        msg = "Unsupported search engine '{engine}'!".format(engine=engine)
        msg += " Supported engins are: {engines}".format(engines=", ".join(allowed_search_engines))
        raise NotSupportedSearchEngine(msg)

    if count > MAX_SEARCH_RESULTS:
        raise InvalidResultsCount("Max allowed count of search results is {count}".format(count=MAX_SEARCH_RESULTS))

    LOG.debug("\targs look apropriate")
    LOG.debug("func _validate_args ended")

def _get_url_and_params(engine, theme):
    LOG.debug("func _get_url_and_params(engine='{}', theme='{}') started".format(engine, theme))

    url = _get_search_engine_settings(engine, "url")
    kwd = _get_search_engine_settings(engine, "kwd")
    search_params = {kwd: theme}
    scrape_params = _get_search_engine_settings(engine, "attrs") # do deepcopy needed?
    url_sanitizer = _get_search_engine_settings(engine, "url_sanitizer")

    LOG.debug("\turl is {}".format(url))
    LOG.debug("\tsearch_params are {}".format(search_params))
    LOG.debug("\tscrape_params are {}".format(scrape_params))
    LOG.debug("\turl_sanitizer are {}".format(url_sanitizer))
    LOG.debug("func _get_url_and_params ended")

    return url, search_params, scrape_params, url_sanitizer

def _get_response(url, params=None):
    LOG.debug("func _get_response(url='{}', params={}) started".format(url, params))

    try:
        req_log = logging.getLogger('requests.packages.urllib3')
        req_log.setLevel(DEFAULT_LOG_LEVEL)
        req_log.propagate = True

        params = params or {}

        resp = get(url, params=params)
        if resp.status_code != codes.ok:
            resp.raise_for_status()
    except RequestException as e:
        raise ErrorOnSearch(e)

    #LOG.debug("\tresponse is {}".format(resp.text))
    LOG.debug("func _get_response ended")

    return resp.text

def _print_links(links, prefix=''):
    for link in links:
        print(prefix, link)

def _get_links(url, search_params=None, scrape_params=None, url_sanitizer=None, count=DEFAULT_SEARCH_RESULTS):
    LOG.debug("func _get_links(url='{}', search_params={}, scrape_params={}, url_sanitizer={}, count={}) started".format(url, search_params, scrape_params, url_sanitizer, count))

    html = _get_response(url, search_params)

    args = {};
    if scrape_params is not None:
        args["attrs"] = scrape_params

    links = []
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all("a", **args):
        href = tag.get("href", "")
        if not href:
            continue

        LOG.debug("\tlink {}".format(href))

        if url_sanitizer is not None:
            href = url_sanitizer(href)
        
        links.append(href)
        if len(links) == count:
            break

    LOG.debug("\tfound {} links".format(len(links)))
    LOG.debug("func _get_links ended")

    return links

def search(theme, engine=SEARCH_ENGINE_YANDEX, count=DEFAULT_SEARCH_RESULTS, recursive=False):
    LOG.debug("func search started")

    _validate_args(theme, engine, count)

    url, search_params, scrape_params, url_sanitizer = _get_url_and_params(engine, theme)

    links = _get_links(url, search_params, scrape_params, url_sanitizer, count)

    if not recursive:
        _print_links(links)
    else:
        for link in links:
            print(link)

            try:
                links = _get_links(link, count=count)
                _print_links(links, prefix="\t")
            except ErrorOnSearch as e:
                print("\tgot error {}".format(e))

    LOG.debug("func search ended")

