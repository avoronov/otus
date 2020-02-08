from .constants import (
    COLUMNS_COUNT,
    MAX_NUMBER,
    MIN_NUMBER,
    NO_NUMBER,
    NUMBERS_PER_ROW,
    NUMBERS_PER_TICKET,
    ROWS_COUNT,
)
from .exceptions import NoSuchNumber, TicketDone
from .utils import check_row_and_column, get_logger, get_randomized_number

LOG = get_logger(__name__)


class Cell:
    @staticmethod
    def _check(number):
        LOG.debug("Cell::_check() started")

        if number != NO_NUMBER:
            assert number >= MIN_NUMBER, "Number less than {}".format(MIN_NUMBER)
            assert number <= MAX_NUMBER, "Number greater than {}".format(MAX_NUMBER)

        LOG.debug("Cell::_check ended")

    def __init__(self, number):
        LOG.debug("Cell::__init__(number={}) started".format(number))

        self._check(number)
        self._number = number
        self._expunged = False

        LOG.debug("Cell::__init__ended")

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self._number == other._number

    def __str__(self):
        if self.is_expunged():
            return "+{}".format(self._number)
        else:
            return "{}".format(self._number)

    def get_number(self):
        return self._number

    def is_no_number(self):
        return self._number == NO_NUMBER

    def is_expunged(self):
        return self._expunged

    def expunge(self):
        LOG.debug("Cell::expunge() started")
        LOG.debug("Cell::expunge: cell marked as expunged")
        self._expunged = True
        LOG.debug("Cell::expunge() ended")


class Cells:
    @staticmethod
    def _check(numbers):
        LOG.debug("Cells::_check(numbers={}) started".format(numbers))

        assert len(numbers) == ROWS_COUNT, "Number of rows not equal to {}".format(
            ROWS_COUNT
        )
        total_numbers = 0
        for columns in numbers:
            assert (
                len(columns) == COLUMNS_COUNT
            ), "Number of columns not equal to {}".format(COLUMNS_COUNT)
            numbers_per_row = 0
            for column, val in enumerate(columns):
                if val != NO_NUMBER:
                    if val == MAX_NUMBER:
                        _column = (val - 1) // 10
                        assert (
                            _column == column
                        ), "Incorrect column for {}: must be {} instead of {}".format(
                            val, _column, column
                        )
                    else:
                        _column = val // 10
                        assert (
                            _column == column
                        ), "Incorrect column for {}: must be {} instead of {}".format(
                            val, _column, column
                        )
                    total_numbers += 1
                    numbers_per_row += 1
            assert (
                numbers_per_row == NUMBERS_PER_ROW
            ), "Must be {} numbers per row".format(NUMBERS_PER_ROW)
        assert (
            total_numbers == NUMBERS_PER_TICKET
        ), "Must be {} numbers per ticket".format(NUMBERS_PER_TICKET)

        LOG.debug("Cells::_check ended")

    def __init__(self, numbers):
        LOG.debug("Cells::__init__() started")

        self._check(numbers)

        self._cells = []
        for columns_vals in numbers:
            row = []
            for val in columns_vals:
                cell = Cell(val)
                row.append(cell)

            self._cells.append(row)

        LOG.debug("Cells::__init__ ended")

    def __eq__(self, other):
        if not isinstance(other, Cells):
            return False

        for row in range(1, ROWS_COUNT + 1):
            for column in range(1, COLUMNS_COUNT + 1):
                if not self.cell_at(row, column) == other.cell_at(row, column):
                    return False

        return True

    def __str__(self):
        result = "\n  |"
        for column in range(0, COLUMNS_COUNT):
            result += "\t{}".format(column + 1)
        result += "\n"
        for column in range(0, COLUMNS_COUNT):
            result += "_________"
        result += "\n  |\n"

        for row, columns in enumerate(self._cells):
            result += "{} |".format(row + 1)
            for cell in columns:
                result += "\t{}".format(cell)
            result += "\n"
        return result

    def __contains__(self, item):
        for row in self._cells:
            for cell in row:
                if cell.get_number() == item:
                    return True
        return False

    def __iter__(self):
        for row in self._cells:
            for column in row:
                yield column

    def cell_at(self, row, column):
        LOG.debug("Cells::cell_at(row={}, column={}) started".format(row, column))

        assert check_row_and_column(row, column), "Incorrect row or column"
        val = self._cells[row - 1][column - 1]

        LOG.debug("Cells::cell_at ended")
        return val

    def find_row_and_column(self, number):
        LOG.debug("Cells::find_row_and_column(number={}) started".format(number))
        for row, columns in enumerate(self._cells):
            for column, cell in enumerate(columns):
                if cell.get_number() == number:
                    return row + 1, column + 1

        raise NoSuchNumber


class Ticket:
    def __init__(self, numbers=None):
        LOG.debug("Ticket::__init__(numbers={}) started".format(numbers))

        if numbers is not None:
            self._cells = Cells(numbers)
        else:
            self.fill_with_random()

        LOG.debug("Ticket::__init__ ended")

    def __eq__(self, other):
        if not isinstance(other, Ticket):
            return False
        return self._cells == other._cells

    def __str__(self):
        return str(self._cells)

    def __contains__(self, item):
        return item in self._cells

    @staticmethod
    def _get_random_numbers():
        LOG.debug("Ticket::_get_random_numbers() started")

        LOG.debug("\tfill all ticket's cells with *")
        numbers = []
        for _ in range(0, ROWS_COUNT):
            row = []
            for _ in range(0, COLUMNS_COUNT):
                row.append(NO_NUMBER)
            numbers.append(row)

        LOG.debug("\tfill some cell with random numbers")
        number_generator = get_randomized_number()
        for row in numbers:
            used_columns = []
            for _ in range(0, NUMBERS_PER_ROW):
                while True:
                    number = next(number_generator)
                    column = number // 10

                    if number == MAX_NUMBER:
                        column -= 1

                    if column not in used_columns:
                        row[column] = number
                        used_columns.append(column)
                        break

        LOG.debug("Ticket::_get_random_numbers() ended")
        return numbers

    def fill_with_random(self):
        LOG.debug("Ticket::fill_with_random() started")
        numbers = self._get_random_numbers()
        self._cells = Cells(numbers)
        LOG.debug("Ticket::fill_with_random() ended")

    def cell_at(self, row, column):
        LOG.debug("Ticket::cell_at(row=%s, column=%s) started", row, column)

        val = self._cells.cell_at(row, column)

        LOG.debug("Ticket::cell_at ended")
        return val

    def find_row_and_column(self, number):
        LOG.debug("Ticket::find_row_and_column(number=%s) started", number)

        val = self._cells.find_row_and_column(number)

        LOG.debug("Ticket::find_row_and_column ended")
        return val

    def count_of_expunged_cells(self):
        i = 0
        for cell in self._cells:
            if cell.is_expunged():
                i += 1

        return i

    def is_all_numbers_expunged(self):
        LOG.debug("Ticket::is_all_numbers_expunged() started")

        val = self.count_of_expunged_cells() == NUMBERS_PER_TICKET

        LOG.debug("Ticket::is_all_numbers_expunged ended with result %s", val)
        return val

    def expunge(self, row, column):
        LOG.debug("Ticket::expunge(row=%s, column=%s) started", row, column)
        self.cell_at(row, column).expunge()

        if self.is_all_numbers_expunged():
            raise TicketDone()

        LOG.debug("Ticket::expunge ended")

    def is_correct(self, used_numbers):
        LOG.debug("Ticket::is_correct(used_numbers=%s) started", used_numbers)

        result = True
        if not self.is_all_numbers_expunged():
            result = False
        else:
            for cell in self._cells:
                LOG.debug("Ticket::is_correct: check cell %s", cell)

                if cell.is_expunged() and cell.is_no_number():
                    result = False
                    break

                if cell.is_expunged() and cell.get_number() not in used_numbers:
                    result = False
                    break

        LOG.debug("Ticket::is_correct ended with result %s", result)
        return result
