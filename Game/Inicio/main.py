import pygame

def carregar(janela):
    # Limpa a tela com uma cor de fundo
    janela.janela.fill((0, 128, 0))  # Verde escuro

    # Desenha um texto na tela para representar a seção "Inicio"
    fonte = pygame.font.SysFont(None, 74)
    texto = fonte.render("Inicio", True, (255, 255, 255))
    janela.janela.blit(texto, (400 - texto.get_width() // 2, 300 - texto.get_height() // 2))

    # Atualiza a tela
    pygame.display.update()
