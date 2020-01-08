from .constants import COLUMNS_COUNT, NO_NUMBER, ROWS_COUNT
from .ticket import Ticket
from .utils import get_logger, get_randomized_number

LOG = get_logger(__name__)


class Host():
    def __init__(self):
        LOG.debug("Host::__init__() started")

        self._numbers_generator = get_randomized_number()
        self._used_numbers = []
        self._tickets = []
    
        LOG.debug("Host::__init__ ended")

    def get_new_ticket(self):
        LOG.debug("Host::get_new_ticket() started")

        ticket = Ticket()
        while ticket in self._tickets:
            ticket.fill_with_random()
        
        self._tickets.append(ticket)

        LOG.debug("Host::get_new_ticket() ended")
        return ticket

    def is_ticket_correct(self, ticket):
        LOG.debug("Host::is_ticket_correct(ticket={}) started".format(ticket))

        result = ticket.is_correct(self._used_numbers)
        
        LOG.debug("Host::is_ticket_correct ended with result {}".format(result))
        return result

    def get_next_number_generator(self):
        LOG.debug("Host::get_next_number_generator() started")

        for val in self._numbers_generator:
            LOG.debug("Game::get_next_number_generator: next random number is {}".format(val))
            LOG.debug("Game::get_next_number_generator: used numbers are {}".format(self._used_numbers))

            self._used_numbers.append(val)
            
            yield val
        
        LOG.debug("Host::get_next_number_generator ended")
