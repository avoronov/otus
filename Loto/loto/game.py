import os
import logging

from .constants import MIN_PLAYERS
from .exceptions import GameOver, NotEnoughPlayers, TicketDone
from .host import Host
from .player import ComputerPlayer, HumanPlayer
from .ticket import Ticket
from .utils import get_logger

LOG = get_logger(__name__)


class Game():
    def __init__(self):
        LOG.debug("Game::__init__() started")
        
        self._host = Host()
        self._players = []
        self._winners = []

        LOG.debug("Game::__init__ ended")

    def add_player(self, player):
        LOG.debug("Game::add_player(player={}) started".format(player))
        ticket = self._host.get_new_ticket()
        player.set_ticket(ticket)
        self._players.append(player)
        LOG.debug("Game::add_player ended")

    def _players_count(self):
        return len(self._players)

    def _has_winners(self):
        LOG.debug("Game::_has_winners() started")
        val = len(self._winners) > 0
        LOG.debug("Game::_has_winners ended and return {}".format(val))
        return val

    def _make_turn(self, number):
        LOG.debug("Game::_make_turn(number={}) started".format(number))

        for player in self._players:
            try:
                player.expunge_number(number)
            except TicketDone:
                LOG.debug("Game::_make_turn: caught TicketDone from {}".format(player))
                self._winners.append(player)
            
            if LOG.getEffectiveLevel() != logging.DEBUG:
                os.system('clear')
        
        LOG.debug("Game::_make_turn ended")

    def start(self):
        LOG.debug("Game::start() started")

        if self._players_count() < MIN_PLAYERS:
            raise NotEnoughPlayers()

        host = self._host
        for number in host.get_next_number_generator():
            self._make_turn(number)
            if self._has_winners():
                break

        for player in self._winners:
            ticket = player.get_ticket()
            if not host.is_ticket_correct(ticket):
                self._winners.remove(player)
                print("Player {} loose due to incorrect ticket {}".format(player.get_name(), ticket))

        if self._winners:
            # names = ", ".join(map(lambda player: player.get_name(), self._winners))
            # print("And we get the winner(s): {}!".format(names))
            print("And we get the winner(s):")
            for player in self._winners:
                print("\t{} with ticket {}".format(player, player.get_ticket()))
        else:
            print("There are no winner(s) so far!")
        
        LOG.debug("Game::start ended")

    @staticmethod
    def test_game():
        human = HumanPlayer("Alex")
        robot = ComputerPlayer("MacBook")
        game = Game()
        game.add_player(human)
        game.add_player(robot)
        game.start()
