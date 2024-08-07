# No arquivo Game/GUI/janela.py
import pygame

class Janela:
    def __init__(self, tamanho, titulo):
        # Espera-se que `tamanho` seja uma tupla (largura, altura)
        self.largura, self.altura = tamanho
        self.titulo = titulo
        self.janela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption(titulo)

    def atualizar(self):
        pygame.display.update()

    def fechar(self):
        pygame.quit()

    def get_surface(self):
        return self.janela
