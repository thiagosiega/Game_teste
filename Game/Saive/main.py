# Game/Saive/main.py
import pygame

def carregar(janela):
    janela.janela.fill((150, 150, 150))  # Limpa a tela com cinza mais escuro
    fonte = pygame.font.SysFont(None, 48)
    texto = fonte.render("Tela de Save", True, (0, 0, 0))
    janela.janela.blit(texto, (100, 100))
    pygame.display.update()
