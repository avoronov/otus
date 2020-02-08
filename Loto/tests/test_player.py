from io import StringIO

import pytest

from loto.player import ComputerPlayer, HumanPlayer, Player
from loto.ticket import Ticket


@pytest.fixture()
def modified_ticket(ticket):
    ticket.expunge(1, 1)
    return ticket


class TestPlayer:
    def test_init(self, human_name):
        player = Player(human_name)
        assert player._name == human_name

    def test_set_name(self, human_name):
        player = Player(human_name)
        assert player.get_name() == human_name

    def test_set_ticket(self, human_name, ticket_numbers):
        player = Player(human_name)
        ticket = Ticket(ticket_numbers)
        player.set_ticket(ticket)
        assert player._ticket == ticket

    def test_get_ticket(self, human_name, ticket_numbers):
        player = Player(human_name)
        ticket = Ticket(ticket_numbers)
        player.set_ticket(ticket)
        assert player.get_ticket() == ticket

    def test_expunge_number(self, human_name):
        player = Player(human_name)
        with pytest.raises(NotImplementedError):
            player.expunge_number(1)


class TestHumanPlayer:
    def test_init(self, human_name):
        player = HumanPlayer(human_name)
        assert player._name == human_name

    def test_str(self, human_name):
        player = HumanPlayer(human_name)
        assert str(player) == f"<human {human_name}>"

    def test_expunge_number_not_such_number(self, human, ticket, monkeypatch):
        monkeypatch.setattr("sys.stdin", StringIO("n\n"))
        human.expunge_number(1)
        assert human.get_ticket() == ticket

    def test_expunge_number_bad_row(self, human, modified_ticket, monkeypatch):
        monkeypatch.setattr("sys.stdin", StringIO("y\n-1\n1\n1\n1\n"))
        human.expunge_number(1)
        assert human.get_ticket() == modified_ticket

    def test_expunge_number_bad_column(self, human, modified_ticket, monkeypatch):
        monkeypatch.setattr("sys.stdin", StringIO("y\n1\n-1\n1\n1\n"))
        human.expunge_number(1)
        assert human.get_ticket() == modified_ticket

    def test_expunge_number_got_such_number(self, human, modified_ticket, monkeypatch):
        monkeypatch.setattr("sys.stdin", StringIO("y\n1\n1\n"))
        human.expunge_number(1)
        assert human.get_ticket() == modified_ticket


class TestComputerPlayer:
    def test_init(self, robot_name):
        player = ComputerPlayer(robot_name)
        assert player._name == robot_name

    def test_str(self, robot_name):
        player = ComputerPlayer(robot_name)
        assert str(player) == f"<robot {robot_name}>"

    def test_expunge_number_not_such_number(self, robot, ticket):
        robot.expunge_number(100)
        assert robot.get_ticket() == ticket

    def test_expunge_number_got_such_number(self, robot, modified_ticket):
        robot.expunge_number(1)
        assert robot.get_ticket() == modified_ticket
