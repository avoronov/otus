class SearchException(Exception):
    pass

class NoThemeToSearch(SearchException):
    pass

class NotSupportedSearchEngine(SearchException):
    pass

class ErrorOnSearch(SearchException):
    pass

class InvalidResultsCount(SearchException):
    pass