import pytest

from loto.exceptions import TicketDone
from loto.host import Host

# @pytest.fixture()


class TestHost:
    def test_init(self, sorted_numbers):
        host = Host()

        assert host._tickets == []
        assert host._used_numbers == []

        numbers = list(host._numbers_generator)
        assert numbers != sorted_numbers
        numbers.sort()
        assert numbers == sorted_numbers

    def test_get_new_ticket(self):
        host = Host()

        expected = []
        expected.append(host.get_new_ticket())
        expected.append(host.get_new_ticket())

        assert host._tickets == expected

    def test_is_ticket_correct(self, used_values, ticket_numbers):
        host = Host(numbers=used_values)

        ticket = host.get_new_ticket(numbers=ticket_numbers)

        for val in host.get_next_number_generator():
            try:
                row, column = ticket.find_row_and_column(val)
                ticket.expunge(row, column)
            except TicketDone:
                pass

        assert host.is_ticket_correct(ticket) is True

        ticket2 = host.get_new_ticket()
        assert host.is_ticket_correct(ticket2) is False

        with pytest.raises(AssertionError, match="Duplicate ticket"):
            host.get_new_ticket(numbers=ticket_numbers)

    def test_get_next_number_generator(self, sorted_numbers):
        host = Host(numbers=sorted_numbers)

        actual = list(host.get_next_number_generator())
        assert actual == sorted_numbers
        assert host._used_numbers == sorted_numbers
