import pygame, sys, socket, select, configuration, constantes
from tabuleiro import *
import json as serialize

class Jogador(object):
    """
    """
    
    def __init__(self):
        """
        """
        self.sock = socket.socket()
        self.sock.setblocking(1)
        self.sock.settimeout(0.1)
        self.host = socket.gethostname()
        self.porta = configuration.porta
        self.sock.connect((self.host, self.porta))
        pygame.init()
        pygame.display.set_mode((configuration.tamanhoJanela, configuration.tamanhoJanela))
        pygame.display.set_caption("5 numa linha")
        self.tela = pygame.display.get_surface()
        self.desenha_tabuleiro()
        pygame.display.update()   
                

    def desenha_tabuleiro(self):
        limiteX = self.tela.get_size()[0]
        limiteY = self.tela.get_size()[1]

        y = 0
        # linhas horizontais
        for i in range(configuration.numCasas):
            pygame.draw.line(self.tela, constantes.amarelo, (0, y), (limiteX, y), 2)
            y += configuration.pixelsPorQuadrado
            
        # linhas verticais:
        x = y = 0
        for i in range(configuration.numCasas):
            pygame.draw.line(self.tela, constantes.amarelo, (x, 0), (x, limiteY), 2)
            x += configuration.pixelsPorQuadrado
            y += configuration.pixelsPorQuadrado           

    def desenha_jogador(self, casa, cor):
        quadrado = configuration.pixelsPorQuadrado
        raio = (int(quadrado - quadrado * 0.4))/2
        x = casa[0] * quadrado + (quadrado/2)
        y = casa[1] * quadrado + (quadrado/2)
        pygame.draw.circle(self.tela, cor, (x,y), raio, 0)
        pygame.display.update()

    def pinta_vencedor(self, lista_coordenadas, cor):
        quadrado = configuration.pixelsPorQuadrado
        for coord in lista_coordenadas:
            x = coord[0] * quadrado
            y = coord[1] * quadrado
            pygame.draw.rect(self.tela, constantes.branco, (x, y, quadrado, quadrado), 0)
            self.desenha_jogador(coord, cor)
        pygame.display.update()


    def mapeia_casa(self, posicaoClique):
        x = (int)(posicaoClique[0]) / configuration.pixelsPorQuadrado
        y = (int)(posicaoClique[1]) / configuration.pixelsPorQuadrado
        return (x,y)

    def envia_clique(self, posicaoClique, jogador):
        """
        """
        casa = self.mapeia_casa(posicaoClique)
        acao = constantes.CLIQUE
        msg = (acao, casa)
        self.escrever_no_servidor(serialize.dumps(msg))

    def ler_do_servidor(self):
        try:
            ready, ignore, ignore2 = select.select([self.sock], [], [], 0)
            for socket in ready:
                return socket.recv(127)
        finally:
            pass

    def escrever_no_servidor(self, msg):
        """
        """
        try:
            ignore2, ready, ignore = select.select([], [self.sock], [], 0)
            for socket in ready:
                return socket.sendall(msg)
        finally:
            pass        

    def run(self):
        while True:
            #PyGame
            for evento in pygame.event.get():
                # para sair do jogo
                if evento.type == pygame.QUIT:
                    self.sock.sendall(serialize.dumps(constantes.SAIR, []))
                    pygame.quit()
                    sys.exit()

                # jogador pressionou uma area
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    self.envia_clique(evento.pos, 0)

            #Network
            data = self.ler_do_servidor()
            if data:
                print data
                msg = serialize.loads(data)
                print msg
                self.processa_mensagem(msg)

    def processa_mensagem(self, msg):
        if (msg[0] == constantes.DESENHA):
            self.desenha_jogador(msg[1], msg[2])
        elif (msg[0 == constantes.VENCEDOR]):
            print 'tem um vencedor'
            self.pinta_vencedor(msg[1], msg[2])                
        else:
            print 'nao processei a mensagem ' + msg

jogador = Jogador()
jogador.run()
