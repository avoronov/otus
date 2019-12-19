#!/usr/bin/env python

import argparse

from searcher import (
    SEARCH_ENGINE_YANDEX,
    DEFAULT_SEARCH_RESULTS,
    SearchException,
    set_debug_log_level,
    get_logger,
    search
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("theme", type=str, help="theme for search")
    parser.add_argument("-e", "--engine", type=str, help="search engine", default=SEARCH_ENGINE_YANDEX)
    parser.add_argument("-c", "--count", type=int, help="number of results", default=DEFAULT_SEARCH_RESULTS)
    parser.add_argument("-d", "--debug", help="switch on debug output", dest="debug", action="store_true")
    parser.set_defaults(debug=False)
    parser.add_argument("-r", "--recursive", help="recursive search", dest="recursive", action="store_true")
    parser.add_argument("--no-recursive", help="not recursive search", dest="recursive", action="store_false")
    parser.set_defaults(recursive=False)

    args = parser.parse_args()

    try:
        if args.debug:
            set_debug_log_level()
        
        search(args.theme, args.engine, args.count, args.recursive)
    except SearchException as e:
        get_logger().debug(e)

