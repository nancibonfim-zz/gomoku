class Tabuleiro(object):
    """
    """
    
    def __init__(self, tamanhoJanela, numCasas):
        """
        
        """
        self.tamanhoJanela = tamanhoJanela
        self.numCasas = numCasas
        self.estado = [[0 for i in range(numCasas)] for j in range(numCasas)]

    def exibe(self):
        """
        (list) -> None
        Imprime o tabuleiro
        """
        print self.estado

    def getPixelsPorQuadrado(self):
        return self.tamanhoJanela / self.numCasas
        
    def getTamanhoJanela(self):
        return self.tamanhoJanela

    def getNumCasas(self):
        return self.numCasas
    
    def set_casa(self, casa, valor):
        print casa
        self.estado[casa[0]][casa[1]] = valor
        
