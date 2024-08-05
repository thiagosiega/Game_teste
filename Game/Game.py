import pygame
import subprocess

from tkinter import messagebox

from GUI.janela import Janela
from GUI.Botoes import Botoes

pygame.init()
pygame.font.init()

tex_btn =["Inicio","Configurações","Saive","Sair"]

def comand(text):
    if (text != "Sair"):
        subprocess.run(["python", f"Game/{text}/main.py"])
    else:
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            janela.fechar()    

#inicializa a janela
janela = Janela(800, 600, "Game")
while True:
    janela.atualizar()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            janela.fechar()
            break
    #desenha o botão
    #botao = Botoes(janela, "Clique", 100, 100, 200, 50, (0, 0, 255), (0, 0, 128), lambda: print("Clicou"))
    for i in range(4):
        botao = Botoes(janela, tex_btn[i], 100, 100 + 60 * i, 200, 50, (0, 0, 255), (0, 0, 128), lambda: comand(tex_btn[i]))
        botao.desenhar()
        botao.executar()
    #atualiza a tela
    janela.atualizar()
