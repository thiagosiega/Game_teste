#file = Game\Game.py

import pygame
from GUI.janela import Janela
from GUI.Botoes import Botoes

from Configurações.main import Configuracoes
from Inicio.main import Inicio

pygame.init()
pygame.font.init()

# Definindo estados do jogo
estado_atual = "Menu"
tex_btn = ["Inicio", "Configurações", "Saive", "Sair"]

def comand(text):
    global estado_atual
    if text == "Sair":
        estado_atual = "Sair"
    else:
        estado_atual = text

# Função auxiliar para criar o comando com o texto correto
def criar_comando(text):
    return lambda: comand(text)

# Inicializa a janela
janela = Janela(800, 600, "Game")

try:
    while True:
        janela.atualizar()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                janela.fechar()
                pygame.quit()
                exit()

        # Verifica o estado atual e desenha a tela correspondente
        if estado_atual == "Menu":
            #pinta a tela de preto
            janela.janela.fill((0, 0, 0))
            for i in range(4):
                botao = Botoes(janela.janela, tex_btn[i], 100, 100 + 60 * i, 200, 50, (0, 0, 255), (0, 0, 128), criar_comando(tex_btn[i]))
                botao.desenhar()
                botao.executar()

        elif estado_atual == "Configurações":
            config = Configuracoes(janela.janela)
            config.executar()
            estado_atual = "Menu"  # Volta ao menu principal ao sair das configurações

        elif estado_atual == "Inicio":
            menu_inicio = Inicio(janela)
            menu_inicio.executar()
            estado_atual = "Menu"

        # Atualiza a tela
        pygame.display.update()
except Exception as e:
    print(e)
    janela.fechar()
    pygame.quit()
    exit()