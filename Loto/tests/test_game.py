import pytest

from loto.exceptions import NotEnoughPlayers
from loto.game import Game
from loto.host import Host
from loto.player import ComputerPlayer
from loto.ticket import Ticket


class TestGame:
    def test_init(self):
        game = Game()

        assert isinstance(game._host, Host)
        assert game._players == []
        assert game._winners == []

    def test_add_player(self, human, robot):
        game = Game()

        game.add_player(human)
        game.add_player(robot)

        assert len(game._players) == 2
        for player in game._players:
            ticket = player.get_ticket()
            assert isinstance(ticket, Ticket)
            assert ticket in game._host._tickets

    def test_players_count(self, human, robot):
        game = Game()

        game.add_player(human)
        game.add_player(robot)

        assert game._players_count() == 2

    def test_start(self, human_name, robot_name):
        game = Game()

        with pytest.raises(NotEnoughPlayers):
            game.start()

        game.add_player(ComputerPlayer(human_name))
        game.add_player(ComputerPlayer(robot_name))

        game.start()

        assert game._has_winners is not False
