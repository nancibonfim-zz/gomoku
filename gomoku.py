import sys, pygame, select, socket, constantes, configuration
from tabuleiro import *
import json as serialize

class GameServer(object):
    """
    """
    def __init__(self, tamanhoTab, nCasas ):
        """
        """
        self.tabuleiro = Tabuleiro(tamanhoTab, nCasas)
        self.estabeleceServer()
        self.jogo()

    def estabeleceServer(self):
        self.servidor = socket.socket()
        self.host = socket.gethostname()
        self.porta = configuration.porta
        self.servidor.bind((self.host, self.porta))
        self.servidor.listen(2) # numero maximo de conexoes

        # o servidor aceita dois jogadores
        self.jogadores = []
        self.jogadores.append(self.servidor.accept()[0])
        self.jogadores.append(self.servidor.accept()[0])

        self.servidor.setblocking(1) # nao bloqueante
        self.servidor.settimeout(0.1)

        self.jogoEmAndamento = True
        self.indiceJogadorAtual = 0

    def getPorta(self):
      return self.porta

    def getJogoEmAndamento(self):
        return self.jogoEmAndamento
    
    def setJogoEmAndamento(self, valor):
        self.jogoEmAndamento = valor

    def jogo(self):
        print "iniciando jogo"
        jogador = self.proximo_jogador() #XXX: this should be changed inside rodada
        while self.getJogoEmAndamento():
            try:
                # ready: array com sockets dos jogadores que estao prontos para ser lidos no socket
                ready, ignore, ignore2 = select.select(self.jogadores, [], [], 0)
                for socket in ready:
                    acao = socket.recv(127)
                    if acao:
                        self.rodada(socket, serialize.loads(acao))
            finally:
                pass

    def rodada(self, jogador, jogada):
        """
        Arguments:
        - `jogador`:
        - `jogada`:
        """
        print jogada
        casa = self.tabuleiro.getCasa(jogada[1])
        if (jogada[0] == constantes.SAIR):
            self.setJogoEmAndamento(False)
            #TODO: Fazer algo pro fim do jogo
        elif (jogada[0] == constantes.CLIQUE):
            # verificar se eh o turno do jogador
            if (jogador != self.getJogadorAtual()):
                pass
            # verifica se o lugar esta vazio
            elif (casa != 0):
                pass
            else:
                try:
                    self.tabuleiro.setCasa(jogada[1], self.indiceJogadorAtual + 1)
                    self.tabuleiro.exibe()
                    msg = serialize.dumps((constantes.DESENHA, jogada[1], self.getCor()))
                    ignore, ready, ignore2 = select.select([], self.jogadores, [], 0)
                    print msg
                    if self.fim_do_jogo(jogada[1]):
                        self.setJogoEmAndamento(False)
                        print "jogo acabado"
                        # Desenha que o jogador atual ganhou
                        msg = serialize.dumps((constantes.VENCEDOR, self.getCoordenadasVencedoras(), self.getCor()))
                        ignore, ready, ignore2 = select.select([], self.jogadores, [], 0)
                        for socket in ready:
                            print "ending"
                            print socket
                            socket.sendall(msg)
                    else:
                        for socket in ready:
                            print "drawing"
                            print socket
                            socket.sendall(msg)
                        self.proximo_jogador()
                finally:
                    self.servidor.close()

    def proximo_jogador(self):
        self.indiceJogadorAtual = (self.indiceJogadorAtual + 1) % 2

    def getJogadorAtual(self):
        return self.jogadores[self.indiceJogadorAtual]

    def conta_casas_iguais(self, casaJogada, incremente_i, incremente_j):
        """
        """
        contador = 0
        i = casaJogada[0]
        j = casaJogada[1]
        coordenadas =[]

        while True:
            i = incremente_i(i)
            j = incremente_j(j)

            if (i < configuration.numCasas and j < configuration.numCasas and j >= 0 and i >= 0) and \
               (self.tabuleiro.getCasa((i, j)) == self.indiceJogadorAtual + 1):
                contador+=1
                coordenadas.append((i,j))
            else:
                break

        return contador, coordenadas

    def conta_casas_eixo(self, casaJogada, incremente_i, incremente_j, decremente_i, decremente_j):
        """
        
        Arguments:
        - `self`:
        - `casaJogada`:
        - `incremente_i`:
        - `incremente_j`:
        """
        coordenadas = []
        contador = 1
        result = self.conta_casas_iguais(casaJogada, incremente_i, incremente_j)
        contador += result[0]
        for coord in result[1]:
            coordenadas.append(coord)
        result = self.conta_casas_iguais(casaJogada, decremente_i, decremente_j)
        contador += result[0]
        for coord in result[1]:
            coordenadas.append(coord)
        print "contando casas"
        print contador
        if contador >= 5:
            coordenadas.append(casaJogada)
            self.setCoordenadasVencedoras(coordenadas)
            return True

        return False
        
    def setCoordenadasVencedoras(self, lista_coordenadas):
        self.coordenadas_vencedoras = lista_coordenadas

    def getCoordenadasVencedoras(self):
        return self.coordenadas_vencedoras      

    def fim_do_jogo(self, casaJogada):
        # Horizontal
        if self.conta_casas_eixo(casaJogada, lambda x: x + 1, lambda y: y, lambda x: x - 1, lambda y: y):
            return True
        # Vertical
        elif self.conta_casas_eixo(casaJogada, lambda x: x, lambda y: y + 1, lambda x: x, lambda y: y - 1):
            return True
        # Diagonal descendo
        elif self.conta_casas_eixo(casaJogada, lambda x: x + 1, lambda y: y - 1, lambda x: x - 1, lambda y: y + 1):
            return True
        # Diagonal subindo
        elif self.conta_casas_eixo(casaJogada, lambda x: x + 1, lambda y: y + 1, lambda x: x - 1, lambda y: y - 1):
            return True
        return False

    def getCor(self):
        if (self.indiceJogadorAtual == 0):
            cor = constantes.azul
        else:
            cor = constantes.vermelho
        return cor


gomoku = GameServer(configuration.tamanhoJanela, configuration.numCasas)
