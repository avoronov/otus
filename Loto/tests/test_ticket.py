from copy import deepcopy

import pytest

from loto.constants import (COLUMNS_COUNT, MAX_NUMBER, MIN_NUMBER, NO_NUMBER,
                            NUMBERS_PER_ROW, ROWS_COUNT)
from loto.exceptions import NoSuchNumber, TicketDone
from loto.ticket import Cell, Cells, Ticket


@pytest.fixture()
def indexes_of_not_numbers(ticket_numbers):
    result = []

    for row, columns in enumerate(ticket_numbers):
        for column, value in enumerate(columns):
            if value == NO_NUMBER:
                result.append((row + 1, column + 1))

    return result


@pytest.fixture()
def indexes_and_vals_of_numbers(ticket_numbers):
    result = []

    for row, columns in enumerate(ticket_numbers):
        for column, value in enumerate(columns):
            if value != NO_NUMBER:
                result.append((row + 1, column + 1, value))

    return result


@pytest.fixture()
def stringified_ticket_numbers():
    return """
  |\t1\t2\t3\t4\t5\t6\t7\t8\t9
_________________________________________________________________________________
  |
1 |\t1\t11\t21\t31\t41\t*\t*\t*\t*
2 |\t2\t12\t22\t32\t42\t*\t*\t*\t*
3 |\t3\t13\t23\t33\t43\t*\t*\t*\t*
"""


@pytest.fixture()
def other_ticket_numbers():
    return [
        [3, 13, 23, 33, 43, NO_NUMBER, NO_NUMBER, NO_NUMBER, NO_NUMBER],
        [2, 12, 22, 32, 42, NO_NUMBER, NO_NUMBER, NO_NUMBER, NO_NUMBER],
        [1, 11, 21, 31, 41, NO_NUMBER, NO_NUMBER, NO_NUMBER, NO_NUMBER],
    ]


class TestCell:
    def test_check(self):
        with pytest.raises(AssertionError, match="Number less than 1"):
            Cell._check(MIN_NUMBER - 1)

        with pytest.raises(AssertionError, match="Number greater than 90"):
            Cell._check(MAX_NUMBER + 1)

        try:
            Cell._check(NO_NUMBER)
        except AssertionError:
            pytest.fail("Unexpected AssertionError!")

    def test_init(self):
        with pytest.raises(AssertionError, match="Number less than 1"):
            Cell(MIN_NUMBER - 1)

        c = Cell(MIN_NUMBER)
        assert c.get_number() == MIN_NUMBER
        assert c.is_expunged() is False

    def test_get_number(self):
        assert Cell(MIN_NUMBER).get_number() == MIN_NUMBER
        assert Cell(MAX_NUMBER).get_number() == MAX_NUMBER

    def test_is_no_number(self):
        assert Cell(MAX_NUMBER).is_no_number() is False
        assert Cell(NO_NUMBER).is_no_number() is True

    def test_is_expunged(self):
        c = Cell(MAX_NUMBER)
        assert c.is_expunged() is False

        c.expunge()
        assert c.is_expunged() is True

    def test_expunge(self):
        c = Cell(MAX_NUMBER)
        assert c.is_expunged() is False

        c.expunge()
        assert c.is_expunged() is True

    def test_eq(self):
        a = Cell(MIN_NUMBER)
        assert a != 1

        b = Cell(MAX_NUMBER)
        assert a != b

        c = Cell(MIN_NUMBER)
        assert a == c

    def test_str(self):
        a = Cell(MIN_NUMBER)
        assert str(a) == str(MIN_NUMBER)

        b = Cell(MAX_NUMBER)
        b.expunge()
        assert str(b) == "+" + str(MAX_NUMBER)


class TestCells:
    def test_check(self, ticket_numbers):

        with pytest.raises(AssertionError, match="Number of rows not equal to 3"):
            Cells._check([])

        with pytest.raises(AssertionError, match="Number of columns not equal to 9"):
            Cells._check([[], [], []])

        with pytest.raises(
            AssertionError, match="Incorrect column for 10: must be 1 instead of 0"
        ):
            _numbers = [
                [
                    10,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                ],
                [],
                [],
            ]
            Cells._check(_numbers)

        with pytest.raises(
            AssertionError, match="Incorrect column for 90: must be 8 instead of 7"
        ):
            _numbers = [
                [
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    90,
                    NO_NUMBER,
                ],
                [],
                [],
            ]
            Cells._check(_numbers)

        with pytest.raises(AssertionError, match="Must be 5 numbers per row"):
            _numbers = [
                [
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                    NO_NUMBER,
                ],
                [],
                [],
            ]
            Cells._check(_numbers)

        with pytest.raises(AssertionError, match="Must be 5 numbers per row"):
            _numbers = [
                [1, 10, 20, 30, 40, NO_NUMBER, NO_NUMBER, NO_NUMBER, NO_NUMBER],
                [2, 11, 21, 31, 41, NO_NUMBER, NO_NUMBER, NO_NUMBER, NO_NUMBER],
                [3, 12, 22, 32, NO_NUMBER, NO_NUMBER, NO_NUMBER, NO_NUMBER, NO_NUMBER],
            ]
            Cells._check(_numbers)

        try:
            Cells._check(ticket_numbers)
        except AssertionError:
            pytest.fail("Unexpected AssertionError!")

    def test_init(self, ticket_numbers):
        # ensure _check is called
        with pytest.raises(AssertionError, match="Number of rows not equal to 3"):
            Cells._check([])

        # ensure Cell::__init__ is called
        with pytest.raises(AssertionError, match="Number less than 1"):
            _numbers = [
                [0, 10, 20, 30, 40, NO_NUMBER, NO_NUMBER, NO_NUMBER, NO_NUMBER],
                [2, 11, 21, 31, 41, NO_NUMBER, NO_NUMBER, NO_NUMBER, NO_NUMBER],
                [3, 12, 22, 32, 42, NO_NUMBER, NO_NUMBER, NO_NUMBER, NO_NUMBER],
            ]
            Cells(_numbers)

        try:
            cells = Cells(ticket_numbers)
            for i, row in enumerate(ticket_numbers):
                for j, column in enumerate(row):
                    assert column == cells._cells[i][j].get_number()
        except AssertionError:
            pytest.fail("Unexpected AssertionError!")

    def test_eq(self, ticket_numbers, other_ticket_numbers):
        assert Cells(ticket_numbers) != Cell(MIN_NUMBER)
        assert Cells(ticket_numbers) != Cells(other_ticket_numbers)
        assert Cells(ticket_numbers) == Cells(ticket_numbers)

    def test_str(self, ticket_numbers, stringified_ticket_numbers):
        assert str(Cells(ticket_numbers)) == stringified_ticket_numbers

    def test_contains(self, ticket_numbers):
        cells = Cells(ticket_numbers)
        assert (33 in cells) is True
        assert (100 in cells) is False

    def test_iter(self, ticket_numbers):
        cells = Cells(ticket_numbers)
        expected = [
            Cell(1),
            Cell(11),
            Cell(21),
            Cell(31),
            Cell(41),
            Cell("*"),
            Cell("*"),
            Cell("*"),
            Cell("*"),
            Cell(2),
            Cell(12),
            Cell(22),
            Cell(32),
            Cell(42),
            Cell("*"),
            Cell("*"),
            Cell("*"),
            Cell("*"),
            Cell(3),
            Cell(13),
            Cell(23),
            Cell(33),
            Cell(43),
            Cell("*"),
            Cell("*"),
            Cell("*"),
            Cell("*"),
        ]

        assert list(cells) == expected

    def test_сell_at(self, ticket_numbers):
        cells = Cells(ticket_numbers)

        with pytest.raises(AssertionError, match="Incorrect row or column"):
            cells.cell_at(0, 1)

        cells.cell_at(1, 1) == Cell(1)

    def test_find_row_and_column(self, ticket_numbers):
        cells = Cells(ticket_numbers)

        cells.find_row_and_column(1) == (1, 1)
        cells.find_row_and_column(43) == (3, 5)

        with pytest.raises(NoSuchNumber):
            cells.find_row_and_column(100)


class TestTicket:
    def test_init(self, ticket_numbers):
        assert Ticket()._cells is not None
        assert Ticket()._cells != ticket_numbers
        assert Ticket(ticket_numbers)._cells == Cells(ticket_numbers)

    def test_eq(self, ticket_numbers, other_ticket_numbers):
        assert Ticket(ticket_numbers) != Cells(ticket_numbers)
        assert Ticket(ticket_numbers) != Ticket(other_ticket_numbers)
        assert Ticket(ticket_numbers) == Ticket(ticket_numbers)

    def test_str(self, ticket_numbers, stringified_ticket_numbers):
        assert str(Cells(ticket_numbers)) == stringified_ticket_numbers

    def test_contains(self, ticket_numbers):
        cells = Cells(ticket_numbers)
        assert (33 in cells) is True
        assert (100 in cells) is False

    def test_get_random_numbers(self):
        ticket_numbers = Ticket._get_random_numbers()

        assert len(ticket_numbers) == ROWS_COUNT
        for row in ticket_numbers:
            assert len(row) == COLUMNS_COUNT
            cnt_in_row = 0
            for column, value in enumerate(row):
                if value != NO_NUMBER:
                    cnt_in_row += 1

                    if value == MAX_NUMBER:
                        value -= 1

                    _col = value // 10

                    assert _col == column
            assert cnt_in_row == NUMBERS_PER_ROW

    def test_fill_with_random(self, ticket_numbers):
        ticket1 = Ticket()
        ticket1.fill_with_random()

        ticket2 = Ticket()
        ticket2.fill_with_random()

        assert ticket1 != ticket2

    def test_сell_at(self, ticket_numbers):
        ticket = Ticket(ticket_numbers)

        with pytest.raises(AssertionError, match="Incorrect row or column"):
            ticket.cell_at(0, 1)

        ticket.cell_at(1, 1) == Cell(1)

    def test_find_row_and_column(
        self, ticket_numbers, indexes_and_vals_of_numbers
    ):
        ticket = Ticket(ticket_numbers)

        for (row, column, value) in indexes_and_vals_of_numbers:
            ticket.find_row_and_column(value) == (row, column)

        with pytest.raises(NoSuchNumber):
            ticket.find_row_and_column(100)

    def test_count_of_expunged_cells(self, ticket_numbers, indexes_of_numbers):
        ticket = Ticket(ticket_numbers)

        assert ticket.count_of_expunged_cells() == 0

        for (row, column) in indexes_of_numbers:
            ticket.cell_at(row, column).expunge()

        assert ticket.count_of_expunged_cells() == len(indexes_of_numbers)

    def test_is_all_numbers_expunged(self, ticket_numbers, indexes_of_numbers):
        ticket = Ticket(ticket_numbers)

        assert ticket.is_all_numbers_expunged() is False

        for (row, column) in indexes_of_numbers:
            ticket.cell_at(row, column).expunge()

        assert ticket.is_all_numbers_expunged() is True

    def test_expunge(self, ticket_numbers, indexes_of_numbers):
        ticket = Ticket(ticket_numbers)

        last_element = indexes_of_numbers.pop()
        _row, _column = last_element

        for (row, column) in indexes_of_numbers:
            ticket.expunge(row, column)
            assert ticket.cell_at(row, column).is_expunged() is True

        with pytest.raises(TicketDone):
            ticket.expunge(_row, _column)

        assert ticket.cell_at(row, column).is_expunged() is True

    def test_is_correct(
        self, ticket_numbers, indexes_of_not_numbers, indexes_of_numbers,
        used_values
    ):
        ticket = Ticket(ticket_numbers)
        assert (
            ticket.is_correct([]) is False
        ), "Ticket with less then 15 expunged cells is not correct"

        ticket1 = Ticket(ticket_numbers)
        not_number_idx = indexes_of_not_numbers.pop()
        ticket1.expunge(*not_number_idx)
        assert (
            ticket1.is_correct([]) is False
        ), "Ticket with not-number cell expunged is not correct"

        ticket2 = Ticket(ticket_numbers)
        for (row, column) in indexes_of_numbers:
            try:
                ticket2.expunge(row, column)
            except TicketDone:
                pass

        used_values1 = deepcopy(used_values)
        used_values1.pop()
        assert (
            ticket2.is_correct(used_values1) is False
        ), "Ticket with with expunged value, not presented in used values, is not correct"

        assert ticket2.is_correct(used_values) is True
