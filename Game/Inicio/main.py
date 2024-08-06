import pygame
import os
import json
from GUI.Botoes import Botoes

class Inicio:
    def __init__(self, janela):
        pygame.init()  # Inicialize o pygame
        self.janela = janela
        self.nome = ""
        self.font = pygame.font.Font(None, 36)
        self.input_active = False
        self.comando_ativo = None

    def textos(self):
        text = ["Escolha um save ou crie um novo"]
        text_surface = self.font.render(text[0], True, (255, 255, 255))
        self.janela.janela.blit(text_surface, (100, 100))

    def criar_comando(self, comando):
        if comando == "Novo":
            self.janela.janela.fill((0, 0, 0))  # Limpa a tela para entrada do nome
            self.input_active = True
            self.comando_ativo = comando

    def salvar(self):
        if self.comando_ativo == "Novo" and self.nome:
            infor_base = {
                "Nome": self.nome,
                "Infor": {
                    "Vida": 100,
                    "Mana": 100,
                    "Capitulo": 1,
                    "Text": 0,
                    "Itens": {
                        "Espada": 1,
                        "Pocao": 1
                    }
                }
            }
            FILE_SAVES = "Game/Saive/Saive.json"
            if os.path.exists(FILE_SAVES):
                with open(FILE_SAVES, "r", encoding='utf-8') as file:
                    saves = json.load(file)
            else:
                saves = []
            saves.append(infor_base)
            with open(FILE_SAVES, "w", encoding='utf-8') as file:
                json.dump(saves, file, indent=4)
            self.input_active = False
            self.comando_ativo = None

    def exibir_saves(self):
        FILE_SAVES = "Game/Saive/Saive.json"
        if os.path.exists(FILE_SAVES):
            with open(FILE_SAVES, "r", encoding='utf-8') as file:
                saves = json.load(file)

            num_saves_to_display = min(len(saves), 5)
            for i in range(num_saves_to_display):
                nome = saves[i].get("Nome", f"Save {i+1}")
                botao = Botoes(
                    self.janela.janela,
                    nome,
                    100,
                    200 + 60 * i,
                    200,
                    50,
                    (0, 0, 255),
                    (0, 0, 128),
                    lambda nome=nome: self.criar_comando(nome)
                )
                botao.desenhar()
                botao.executar()
        else:
            label = self.font.render("Nenhum save encontrado", True, (255, 255, 255))
            self.janela.janela.blit(label, (100, 200))

    def btn_novo(self):
        botao = Botoes(
            self.janela.janela,
            "Novo",
            100,
            300 + 60 * 4,
            200,
            50,
            (0, 0, 255),
            (0, 0, 128),
            lambda: self.criar_comando("Novo")
        )
        botao.desenhar()
        botao.executar()

    def atualizar_nome(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.nome = self.nome[:-1]
        elif event.key == pygame.K_RETURN:
            self.salvar()
        else:
            self.nome += event.unicode

    def executar(self):
        clock = pygame.time.Clock()  # Para controlar o FPS
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and self.input_active:
                    self.atualizar_nome(event)

            self.janela.janela.fill((0, 0, 0))  # Preenche a tela com a cor de fundo
            self.textos()
            self.exibir_saves()
            self.btn_novo()

            if self.input_active:
                nome_surface = self.font.render(self.nome, True, (255, 255, 255))
                self.janela.janela.blit(nome_surface, (100, 150))

            self.janela.atualizar()  # Atualiza a tela
            pygame.display.flip()  # Usa flip() para evitar piscar
            clock.tick(30)  # Limita o FPS para 30
