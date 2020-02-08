from random import shuffle

import pytest

from loto.constants import MAX_NUMBER, MIN_NUMBER, NO_NUMBER
from loto.player import ComputerPlayer, HumanPlayer
from loto.ticket import Ticket


def get_numbers():
    return [x for x in range(MIN_NUMBER, MAX_NUMBER + 1)]


@pytest.fixture()
def sorted_numbers():
    numbers = get_numbers()
    numbers.sort()
    return numbers


@pytest.fixture()
def randomized_numbers(sorted_numbers):
    numbers = get_numbers()
    shuffle(numbers)
    return numbers


@pytest.fixture()
def ticket_numbers():
    return [
        [1, 11, 21, 31, 41, NO_NUMBER, NO_NUMBER, NO_NUMBER, NO_NUMBER],
        [2, 12, 22, 32, 42, NO_NUMBER, NO_NUMBER, NO_NUMBER, NO_NUMBER],
        [3, 13, 23, 33, 43, NO_NUMBER, NO_NUMBER, NO_NUMBER, NO_NUMBER],
    ]


@pytest.fixture()
def used_values(ticket_numbers):
    result = []

    for columns in ticket_numbers:
        for value in columns:
            if value != NO_NUMBER:
                result.append(value)

    return result


@pytest.fixture()
def indexes_of_numbers(ticket_numbers):
    result = []

    for row, columns in enumerate(ticket_numbers):
        for column, value in enumerate(columns):
            if value != NO_NUMBER:
                result.append((row + 1, column + 1))

    return result


@pytest.fixture()
def ticket(ticket_numbers):
    return Ticket(ticket_numbers)


@pytest.fixture()
def human_name():
    return "Alex"


@pytest.fixture()
def robot_name():
    return "Bender"


@pytest.fixture()
def human(human_name, ticket):
    player = HumanPlayer(human_name)
    player.set_ticket(ticket)
    return player


@pytest.fixture()
def robot(robot_name, ticket):
    player = ComputerPlayer(robot_name)
    player.set_ticket(ticket)
    return player
