import pygame
import sys
import socket
import select
import configuration
import constants
from game_board import *
import json as serialize

class Player(object):
   
    def __init__(self, host=socket.gethostname()):
        """ (Player, str) -> NoneType

        A player with a host and a screen
        """
        # create a socket
        self.sock = socket.socket()
        self.host = host
        self.door = configuration.door

        print self.host
        self.sock.settimeout(10)

        self.sock.connect((self.host, self.door))
        self.sock.setblocking(1)
        self.sock.settimeout(0.1)

        # initialize pygame
        pygame.init()
        pygame.display.set_mode((configuration.windowLength, configuration.windowLength))
        pygame.display.set_caption("5 in a row")
        self.screen = pygame.display.get_surface()
        self.draw_board()
        pygame.display.update()   
                

    def draw_board(self):
        """ (Player) -> NoneType 
        
        Draws the game board
        """
        
        boundX = self.screen.get_size()[0]
        boundY = self.screen.get_size()[1]

        y = 0
        # draw horizontal lines
        for i in range(configuration.nSquares):
            pygame.draw.line(self.screen, constants.yellow, (0, y), (boundX, y), 2)
            y += configuration.pixelsPerSquare
            
        # draw vertical lines
        x = y = 0
        for i in range(configuration.nSquares):
            pygame.draw.line(self.screen, constants.yellow, (x, 0), (x, boundY), 2)
            x += configuration.pixelsPerSquare
            y += configuration.pixelsPerSquare           

    def draw_move(self, casa, cor):
        """ (Player, str, str) -> NoneType 
        
        Draws a circle representing the move of a player on the board
        """
        square = configuration.pixelsPerSquare
        raio = (int(square - square * 0.4))/2
        x = casa[0] * square + (square/2)
        y = casa[1] * square + (square/2)
        pygame.draw.circle(self.screen, cor, (x,y), raio, 0)
        pygame.display.update()

    def draw_winner(self, coordinates_list, cor):
        """ (Player, list of list of int, list of int) -> NoneType 
        
        Draws the sequence of the 5 circles of the winner
        """
        square = configuration.pixelsPerSquare
        for coord in coordinates_list:
            x = coord[0] * square
            y = coord[1] * square
            pygame.draw.rect(self.screen, constants.white, 
                             (x, y, square, square), 0)
            self.draw_move(coord, cor)
        pygame.display.update()


    def map_square(self, clickPosition):
        """ (Player, list of float)

        Maps the clicks of the player to a square of the board
        """
        x = (int)(clickPosition[0]) / configuration.pixelsPerSquare
        y = (int)(clickPosition[1]) / configuration.pixelsPerSquare
        return (x, y)

    def send_click(self, clickPosition, player):
        """
        """
        square = self.map_square(clickPosition)
        action = constants.CLICK
        msg = (action, square)
        self.send_to_server(serialize.dumps(msg))

    def read_from_server(self):
        try:
            ready, ignore, ignore2 = select.select([self.sock], [], [], 0)
            for socket in ready:
                return socket.recv(127)
        finally:
            pass

    def send_to_server(self, msg):
        try:
            ignore2, ready, ignore = select.select([], [self.sock], [], 0)
            for socket in ready:
                return socket.sendall(msg)
        finally:
            pass        

    def run(self):
        while True:
            # PyGame
            for event in pygame.event.get():
                # quit event
                if event.type == pygame.QUIT:
                    self.sock.sendall(serialize.dumps((constants.QUIT, [])))
                    pygame.quit()
                    sys.exit()

                # the player press a area
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.send_click(event.pos, 0)

            # Network
            # read and process a received message from the server
            data = self.read_from_server()
            if data:
                msg = serialize.loads(data)
                self.process_message(msg)

    def process_message(self, msg):
        if (msg[0] == constants.DRAW):
            self.draw_move(msg[1], msg[2])
        elif (msg[0 == constants.WINNER]):
            print 'we have a winner'
            self.draw_winner(msg[1], msg[2])                
        else:
            print 'message unprocessed: ' + msg


player = None
if len(sys.argv) > 1:
    player = Player(sys.argv[1])
else:
    player = Player()

player.run()
