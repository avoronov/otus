from loto.constants import COLUMNS_COUNT, MAX_NUMBER, ROWS_COUNT
from loto.utils import check_row_and_column, get_randomized_number


def test_check_row_and_column():
    assert check_row_and_column(0, COLUMNS_COUNT) is False
    assert check_row_and_column(ROWS_COUNT + 1, COLUMNS_COUNT) is False
    assert check_row_and_column(ROWS_COUNT, 0) is False
    assert check_row_and_column(ROWS_COUNT, COLUMNS_COUNT + 1) is False
    assert check_row_and_column(ROWS_COUNT, COLUMNS_COUNT) is True


def test_get_randomized_number(sorted_numbers, randomized_numbers):
    assert len(list(get_randomized_number())) == MAX_NUMBER

    actual = list(get_randomized_number())
    actual.sort()
    assert actual == sorted_numbers

    numbers = list(get_randomized_number(numbers=randomized_numbers))
    assert numbers == randomized_numbers
