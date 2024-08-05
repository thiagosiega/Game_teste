import pygame

class Botoes:
    def __init__(self, superficie, texto, x, y, largura, altura, cor, cor_hover, acao):
        self.janela = superficie  # Acessa a superfície diretamente
        self.texto = texto
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.cor_hover = cor_hover
        self.acao = acao
        self.rect = pygame.Rect(x, y, largura, altura)
        self.clicado = False
        self.fonte = pygame.font.SysFont(None, 24)

    def desenhar(self):
        pygame.draw.rect(self.janela, self.cor, self.rect)
        texto = self.fonte.render(self.texto, True, (255, 255, 255))
        self.janela.blit(texto, (self.x + (self.largura / 2 - texto.get_width() / 2), self.y + (self.altura / 2 - texto.get_height() / 2)))

    def hover(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(self.janela, self.cor_hover, self.rect)
            texto = self.fonte.render(self.texto, True, (255, 255, 255))
            self.janela.blit(texto, (self.x + (self.largura / 2 - texto.get_width() / 2), self.y + (self.altura / 2 - texto.get_height() / 2)))
            if pygame.mouse.get_pressed()[0] and not self.clicado:
                self.clicado = True
        else:
            self.clicado = False

    def executar(self):
        self.hover()
        if self.clicado:
            self.acao()
            self.clicado = False  # Reseta o estado de clique após a ação ser executada.
