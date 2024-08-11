import pygame
import os
import json

from GUI.janela import Janela
from GUI.Botoes import Botoes
from Configurações.main import Configuracoes
from Inicio.main import Inicio
from Pecados.main import Pecados

pygame.init()
pygame.font.init()

# Carregar as configurações do jogo
FILE_CONFIG = "Game/Saive/Config.json"
Dados_base = {
    "Tela": "800x600",
    "Nivel": "Facil",
    "FPS": "30"
}

if os.path.exists(FILE_CONFIG):
    with open(FILE_CONFIG, "r") as file:
        Dados_base.update(json.load(file))
else:
    with open(FILE_CONFIG, "w") as file:
        json.dump(Dados_base, file)

if isinstance(Dados_base["Tela"], list):
    tamanho = tuple(Dados_base["Tela"])
elif Dados_base["Tela"] == "Full Screen":
    tamanho = (pygame.display.Info().current_w, pygame.display.Info().current_h)
else:
    tamanho = tuple(map(int, Dados_base["Tela"].split('x')))

# Cria a janela
janela = Janela(tamanho, "Game")

#imagem do fundo
fundo = pygame.image.load("Game/Fundo.jpg")
fundo = pygame.transform.scale(fundo, tamanho)

# Definindo estados do jogo
estado_atual = "Menu"
tex_btn = ["Inicio", "Configurações", "Pecados", "Sair"]

def comand(text):
    global estado_atual
    if text == "Sair":
        estado_atual = "Sair"
    else:
        estado_atual = text

# Função auxiliar para criar o comando com o texto correto
def criar_comando(text):
    return lambda: comand(text)

def desenhar_menu():
    surface = janela.get_surface()
    largura, altura = surface.get_size()
    
    # Definindo as propriedades dos botões
    largura_botao = 200
    altura_botao = 50
    espaco_entre_botoes = 20
    pos_x = (largura - largura_botao) // 10
    pos_y = (altura - (altura_botao * len(tex_btn) + espaco_entre_botoes * (len(tex_btn) - 1))) // 10
    
    for i, texto in enumerate(tex_btn):
        botao = Botoes(
            surface,
            texto,
            pos_x,
            pos_y + (altura_botao + espaco_entre_botoes) * i,
            largura_botao,
            altura_botao,
            (0, 0, 255),
            (0, 0, 128),
            criar_comando(texto)
        )
        botao.desenhar()
        botao.executar()

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                janela.fechar()
                pygame.quit()
                exit()

        if estado_atual == "Menu":
            janela.get_surface().blit(fundo, (0, 0))
            desenhar_menu()

        elif estado_atual == "Configurações":
            config = Configuracoes(janela.get_surface())
            config.executar()
            estado_atual = "Menu"
        
        elif estado_atual == "Inicio":
            menu_inicio = Inicio(janela)
            menu_inicio.executar()
            estado_atual = "Menu"

        elif estado_atual == "Sair":
            janela.fechar()
            pygame.quit()
            exit()

        elif estado_atual == "Pecados":
            pecados = Pecados(janela.get_surface())
            pecados.executar()
            estado_atual = "Menu"
        else:
            print("Estado inválido")
            estado_atual = "Menu"

       
        # Atualiza a tela
        pygame.display.update()

except Exception as e:
    print(e)
    janela.fechar()
    pygame.quit()
    exit()
