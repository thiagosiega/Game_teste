import pygame
from tkinter import messagebox
from GUI.janela import Janela
from GUI.Botoes import Botoes
import subprocess

pygame.init()
pygame.font.init()

estado_atual = "Menu"
tex_btn = ["Inicio", "Configurações", "Saive", "Sair"]

def comand(text):
    global estado_atual
    if text == "Sair":
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            janela.fechar()
    else:
        try:
            # Executa o script principal correspondente ao botão clicado
            subprocess.run(["python", f"Game/{text}/main.py"], check=True)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: Game/{text}/main.py")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o script: {e}")

# Função auxiliar para criar o comando com o texto correto
def criar_comando(text):
    return lambda: comand(text)

# Inicializa a janela
janela = Janela(800, 600, "Game")

while True:
    janela.atualizar()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            janela.fechar()
            break

    # Desenha o menu
    if estado_atual == "Menu":
        for i in range(4):
            botao = Botoes(janela.janela, tex_btn[i], 100, 100 + 60 * i, 200, 50, (0, 0, 255), (0, 0, 128), criar_comando(tex_btn[i]))
            botao.desenhar()
            botao.executar()

    # Atualiza a tela
    pygame.display.update()
