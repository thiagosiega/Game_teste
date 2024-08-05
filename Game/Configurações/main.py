# Game/Configuracoes/main.py
import pygame

def carregar(janela):
    janela.janela.fill((200, 200, 200))  # Limpa a tela com cinza
    fonte = pygame.font.SysFont(None, 48)
    texto = fonte.render("Configurações", True, (0, 0, 0))
    janela.janela.blit(texto, (100, 100))
    pygame.display.update()
