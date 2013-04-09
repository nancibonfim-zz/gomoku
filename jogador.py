import pygame, sys, socket, select, configuration, constantes
from tabuleiro import *
import pickle as serialize

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

    def mapeia_casa(self, posicaoClique):
        x = (int)(posicaoClique[0]) / configuration.pixelsPorQuadrado
        y = (int)(posicaoClique[1]) / configuration.pixelsPorQuadrado
        return (x,y)

    def envia_clique(self, posicaoClique, jogador):
        """
        """
        casa = self.mapeia_casa(posicaoClique)
        self.sock.sendall(serialize.dumps(casa))
        self.desenha_jogador(casa, constantes.azul) #XXXremove

    def logicaNotHere(self):
        if jogador == 0:
            self.desenha_jogador(casa, constantes.azul)
        else:
            self.desenha_jogador(casa, constantes.vermelho)
            self.tabuleiro.set_casa(casa, 1)
            self.tabuleiro.exibe()

    def read_from_server(self):
        try:
            #XXX: weird ugly fucking shit of hack
            ready, ignore, ignore2 = select.select([self.sock], [], [], 0)
            for s in ready:
                return s.recv(127)
        finally:
            pass

    def run(self):
        print "pracatum"
        while True:
            #PyGame
            for evento in pygame.event.get():
                # para sair do jogo
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # jogador pressionou uma area
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    self.envia_clique(evento.pos, 0)

            #Network
            data = self.read_from_server()
            if data:
                print data
                print serialize.loads(data)

# try:
#     # Enviar dados
#     message = 'This is the message.  It will be repeated.'
#     print >>sys.stderr, 'sending "%s"' % message
#     sock.sendall(message)

#     # Aguarda resposta
#     amount_received = 0
#     amount_expected = len(message)
                    
#     while amount_received < amount_expected:
#         data = sock.recv(16)
#         amount_received += len(data)
#         print >>sys.stderr, 'received "%s"' % data

# finally:
#     print >>sys.stderr, 'closing socket'
#     sock.close()

jogador = Jogador()
jogador.run()
