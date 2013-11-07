class Board(object):
    """ A game board of gomoku """
    
    def __init__(self, windowLength, nSquares):
        """ (Board, int, int) -> NoneType
        
        A board with your length and the number of squares

        >>> board = Board(100, 10)
        >>> board.windowLength
        100
        >>> board.nSquares
        10
        >>> board.state[[0][0]]
        0
        >>> board.state[[9][9]]
        0
        """
        self.windowLength = windowLength
        self.nSquares = nSquares
        self.state = [[0 for i in range(nSquares)] for j in range(nSquares)]

    def display(self):
        """
        (Board) -> NoneType
        
        Displays the game board
        """
        print self.state

    def getPixelsPerSquare(self):
        """ (Board) -> int 
        
        Returns the length of a square of the board

        >>> board = Board(100, 10)
        >>> board.getPixelsPerSquare
        10
        """
        return self.windowLength / self.nSquares

    def setSquare(self, square, value):
        """ (Board, ) -> NoneType 
        
        Set a value to a square of the game board
        """
        self.state[square[0]][square[1]] = value
        
    def getSquare(self, coordenada):
        """ (Board, list of int) -> int 
        
        Returns the value of the space on the game board
        """
        return self.state[coordenada[0]][coordenada[1]]
