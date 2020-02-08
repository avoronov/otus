from .constants import COLUMNS_COUNT, ROWS_COUNT
from .utils import check_row_and_column, get_logger

LOG = get_logger(__name__)


class Player:
    def __init__(self, name):
        LOG.debug("Player::__init__() started")
        self._name = name
        LOG.debug("Player::__init__ ended")

    def get_name(self):
        return self._name

    def set_ticket(self, ticket):
        LOG.debug("Player::set_ticket(ticket={}) started".format(ticket))
        self._ticket = ticket
        LOG.debug("Player::set_ticket ended")

    def get_ticket(self):
        return self._ticket

    def expunge_number(self, number):
        raise NotImplementedError()


class HumanPlayer(Player):
    def __init__(self, name):
        LOG.debug("HumanPlayer::__init__(name={}) started".format(name))
        super().__init__(name)
        LOG.debug("HumanPlayer::__init__ ended")

    def __str__(self):
        return "<human {}>".format(self._name)

    def expunge_number(self, number):
        LOG.debug("HumanPlayer::expunge_number(number=%s) started", number)

        print("Your ticket is:")
        print(self._ticket)

        print("Next number is {}".format(number))

        while True:
            ans = input("Do you have such a number? (y/n) ")
            if ans == "y" or ans == "n":
                break

        print(f"{ans}")

        if ans == "y":
            while True:
                row = input(f"Enter row (from 1 till {ROWS_COUNT}) ")
                print(f"{row}")

                column = input(f"Enter column (from 1 till {COLUMNS_COUNT}) ")
                print(f"{column}")

                row = int(row)
                column = int(column)

                if check_row_and_column(row, column):
                    break

            self._ticket.expunge(row, column)

        LOG.debug("HumanPlayer::expunge_number ended")


class ComputerPlayer(Player):
    def __init__(self, name):
        LOG.debug("ComputerPlayer::__init__(name={}) started".format(name))
        super().__init__(name)
        LOG.debug("ComputerPlayer::__init__ ended")

    def __str__(self):
        return "<robot {}>".format(self._name)

    def expunge_number(self, number):
        LOG.debug(f"ComputerPlayer::expunge_number(number={number}) started")

        if number in self._ticket:
            row, column = self._ticket.find_row_and_column(number)
            self._ticket.expunge(row, column)

        LOG.debug("ComputerPlayer::expunge_number ended")
