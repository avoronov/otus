class LotoException(Exception):
    pass

class NotEnoughPlayers(LotoException):
    pass

class GameOver(LotoException):
    pass

class TicketDone(LotoException):
    pass

class NoSuchNumber(LotoException):
    pass