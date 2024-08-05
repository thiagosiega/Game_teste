import pygame

class Janela:
    def __init__(self, largura, altura, titulo):
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.janela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption(titulo)

    def atualizar(self):
        pygame.display.update()

    def fechar(self):
        pygame.quit()
