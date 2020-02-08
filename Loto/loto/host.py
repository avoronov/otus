from .ticket import Ticket
from .utils import get_logger, get_randomized_number

LOG = get_logger(__name__)


class Host:
    def __init__(self, numbers=None):
        LOG.debug("Host::__init__() started")

        self._numbers_generator = get_randomized_number(numbers=numbers)
        self._used_numbers = []
        self._tickets = []

        LOG.debug("Host::__init__ ended")

    def get_new_ticket(self, numbers=None):
        LOG.debug("Host::get_new_ticket() started")

        if numbers is not None:
            ticket = Ticket(numbers=numbers)
            print("Tickets:")
            for t in self._tickets:
                print(t)
            print("Ticket {}".format(ticket))
            assert ticket not in self._tickets, 'Duplicate ticket'
        else:
            ticket = Ticket()
            while ticket in self._tickets:
                ticket.fill_with_random()

        self._tickets.append(ticket)

        LOG.debug("Host::get_new_ticket() ended")
        return ticket

    def is_ticket_correct(self, ticket):
        LOG.debug("Host::is_ticket_correct(ticket={}) started".format(ticket))

        result = ticket.is_correct(self._used_numbers)

        LOG.debug("Host::is_ticket_correct ended, result {}".format(result))
        return result

    def get_next_number_generator(self):
        LOG.debug("Host::get_next_number_generator() started")

        for val in self._numbers_generator:
            LOG.debug(
                "Game::get_next_number_generator: next number is {}"
                .format(val)
            )
            LOG.debug(
                "Game::get_next_number_generator: used numbers are {}".format(
                    self._used_numbers
                )
            )

            self._used_numbers.append(val)

            yield val

        LOG.debug("Host::get_next_number_generator ended")
