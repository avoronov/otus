#!/usr/bin/env python

from bs4 import BeautifulSoup
import logging
import re
from requests import get, codes
from requests.exceptions import RequestException
import sys

from .constants import *
from .exceptions import *


DEFAULT_LOG_LEVEL = logging.CRITICAL
#DEFAULT_LOG_LEVEL = logging.DEBUG


def _get_logger():
    log = logging.getLogger(__name__)
    log.setLevel(DEFAULT_LOG_LEVEL)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(DEFAULT_LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') # %(name)s - 
    sh.setFormatter(formatter)
    log.addHandler(sh)
    return log

LOG = _get_logger()

def _validate_args(theme, engine, count):
    LOG.debug("func _validate_args(theme='{}', engine='{}', count={}) started".format(theme, engine, count))

    if theme is None or len(theme) < 1:
        raise NoThemeToSearch("No theme to search given")

    if engine not in ALLOWED_SEARCH_ENGINES:
        msg = "Unsupported search engine {engine}!".format(engine=engine)
        msg += " Supported engins are {engines}".format(engines=", ".join(ALLOWED_SEARCH_ENGINES))
        raise NotSupportedSearchEngine(msg)

    if count > MAX_SEARCH_RESULTS:
        raise InvalidResultsCount("Max allowed count of search results is {count}".format(count=MAX_SEARCH_RESULTS))

    LOG.debug("\targs look apropriate")

    LOG.debug("func _validate_args ended")

def _get_url_and_params(engine, theme):
    LOG.debug("func _get_url_and_params(engine='{}', theme='{}') started".format(engine, theme))

    settings = ALLOWED_SEARCH_ENGINES[engine]

    url = settings["url"]
    search_params = {settings["kwd"]: theme}
    scrape_params = settings["attrs"]

    LOG.debug("\turl is {}".format(url))
    LOG.debug("\tsearch_params are {}".format(search_params))
    LOG.debug("\tscrape_params are {}".format(scrape_params))

    LOG.debug("func _get_url_and_params ended")

    return url, search_params, scrape_params

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

def _get_links(url, search_params=None, scrape_params=None, count=DEFAULT_SEARCH_RESULTS):
    LOG.debug("func _get_links(url='{}', search_params={}, scrape_params={}, count={}) started".format(url, search_params, scrape_params, count))

    html = _get_response(url, search_params)

    args = {};
    if scrape_params is not None:
        args["attrs"] = scrape_params

    links = []

    soup = BeautifulSoup(html, 'lxml')
    for tag in soup.find_all("a", **args):
        LOG.debug("\tlink {}".format(tag["href"]))

        href = tag["href"]
        # remove google shit
        href = re.sub('^(.*)(?=https?\:\/\/)', '', href)

        links.append(href)
        
        if len(links) == count:
            break

    LOG.debug("\tfound {} links".format(len(links)))

    LOG.debug("func _get_links ended")

    return links


def search(theme, engine=SEARCH_ENGINE_YANDEX, count=DEFAULT_SEARCH_RESULTS, recursive=False):
    LOG.debug("func search started")

    _validate_args(theme, engine, count)

    url, search_params, scrape_params = _get_url_and_params(engine, theme)

    links = _get_links(url, search_params, scrape_params, count)

    if not recursive:
        for link in links:
            print(link)
    else:
        for link in links:
            print(link)

            links = _get_links(link, count=count)
            for _link in links:
                print("\t", _link)

    LOG.debug("func search ended")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("theme", type=str, help="theme for search")
    parser.add_argument("-e", "--engine", type=str, help="search engine", default="yandex")
    parser.add_argument("-c", "--count", type=int, help="number of results", default=DEFAULT_SEARCH_RESULTS)
    parser.add_argument("-r", "--recursive", help="recursive search", dest="recursive", action="store_true")
    parser.add_argument("--no-recursive", help="not recursive search", dest="recursive", action="store_false")
    parser.set_defaults(recursive=False)

    args = parser.parse_args()
    
    search(args.theme, args.engine, args.count, args.recursive)
