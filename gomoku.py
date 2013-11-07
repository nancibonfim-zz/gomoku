import pygame
import sys
import socket
import select
import configuration
import constants
from game_board import *
import json as serialize

class GameServer(object):

    def __init__(self, board_length, nSquares):
        self.board = Board(board_length, nSquares)
        self.set_server()
        self.game()

    def set_server(self):
        self.server = socket.socket()
        self.host = ""
        self.door = configuration.door
        self.server.bind((self.host, self.door))
        self.server.listen(2) # max number of conections

        # a server accepts 2 players
        self.players = []
        self.players.append(self.server.accept()[0])
        self.players.append(self.server.accept()[0])

        self.server.setblocking(1)
        self.server.settimeout(0.1)

        self.game_in_progress = True
        self.player_indice = 0

    def getDoor(self):
      return self.door

    def set_game_in_progress(self, valor):
        self.game_in_progress = valor

    def game(self):
        print "initializing game"
        player = self.next_player()
        while self.game_in_progress:
            try:
                # ready: sockets of the players ready to be read in the socket
                ready, ignore, ignore2 = select.select(self.players, [], [], 0)
                for socket in ready:
                    action = socket.recv(127)
                    if action:
                        self.round(socket, serialize.loads(action))
            finally:
                pass

    def round(self, player, move):
        """ """
        if (move[0] == constants.QUIT):
            self.set_game_in_progress(False)
            #TODO: make something to the end of the game
        elif (move[0] == constants.CLICK):
            # verifies if is the player's turn
            if (player != self.get_player()):
                pass
            # verifies if is a empty square
            elif (self.board.getSquare(move[1]) != 0):
                pass
            else:
                try:
                    self.board.setSquare(move[1], self.player_indice + 1)
                    self.board.display()
                    msg = serialize.dumps((constants.DRAW, move[1], self.get_color()))
                    ignore, ready, ignore2 = select.select([], self.players, [], 0)

                    # checks if we have a winner
                    if self.end_game(move[1]):
                        self.set_game_in_progress(False)
                        print "end of the game"
                        # Draws the winner
                        msg = serialize.dumps((constants.WINNER, self.get_winner_coordinates(), self.get_color()))
                        ignore, ready, ignore2 = select.select([], self.players, [], 0)
                        for socket in ready:
                            socket.sendall(msg)
                    else:
                        for socket in ready:
                            socket.sendall(msg)
                        self.next_player()
                finally:
                    self.server.close()

    def next_player(self):
        self.player_indice = (self.player_indice + 1) % 2

    def get_player(self):
        return self.players[self.player_indice]

    def count_squares(self, played_square, next_i, next_j):
        """
        """
        counter = 0
        i = played_square[0]
        j = played_square[1]
        coord =[]

        while True:
            i = next_i(i)
            j = next_j(j)

            if (i < configuration.nSquares and j < configuration.nSquares and j >= 0 and i >= 0) and \
               (self.board.getSquare((i, j)) == self.player_indice + 1):
                counter += 1
                coord.append((i,j))
            else:
                break

        return counter, coord

    def count_squares_axis(self, played_square, next_i, next_j, previous_i, previous_j):
        coord = []
        counter = 1
        result = self.count_squares(played_square, next_i, next_j)
        counter += result[0]
        for crd in result[1]:
            coord.append(crd)
        result = self.count_squares(played_square, previous_i, previous_j)
        counter += result[0]
        for crd in result[1]:
            coord.append(crd)
        if counter >= 5:
            coord.append(played_square)
            self.set_winner_coordinates(coord)
            return True

        return False

    def set_winner_coordinates(self, coordinates):
        self.winner_coordinates = coordinates

    def get_winner_coordinates(self):
        return self.winner_coordinates

    def end_game(self, played_square):
        # Horizontal
        if self.count_squares_axis(played_square, lambda x: x + 1, lambda y: y, lambda x: x - 1, lambda y: y):
            return True
        # Vertical
        elif self.count_squares_axis(played_square, lambda x: x, lambda y: y + 1, lambda x: x, lambda y: y - 1):
            return True
        # Down diagonal
        elif self.count_squares_axis(played_square, lambda x: x + 1, lambda y: y - 1, lambda x: x - 1, lambda y: y + 1):
            return True
        # Up diagonal
        elif self.count_squares_axis(played_square, lambda x: x + 1, lambda y: y + 1, lambda x: x - 1, lambda y: y - 1):
            return True
        return False

    def get_color(self):
        if (self.player_indice == 0):
            color = constants.blue
        else:
            color = constants.red
        return color


gomoku = GameServer(configuration.windowLength, configuration.nSquares)
