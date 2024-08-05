# File= Game\Configurações\main.py

import pygame
import json
import os
from tkinter import messagebox

class Configuracoes:
    def __init__(self, janela):
        self.janela = janela
        self.largura, self.altura = janela.get_size()
        self.cor_fundo = (0, 0, 0)
        self.cor_texto = (255, 255, 255)
        self.cor_selecionada = (0, 255, 0)
        self.fonte = pygame.font.SysFont(None, 24)
        self.opcoes = {
            "Tela": ["800x600", "1024x768", "1280x720", "1920x1080", "Full Screen"],
            "Nivel": ["Facil", "Medio", "Dificil", "Insano", "Faça seu pior"],
            "FPS": ["10", "20", "30", "60"]
        }
        self.estado_expansao = {key: False for key in self.opcoes}
        self.selecao_opcao = {key: None for key in self.opcoes}

    def desenhar_opcoes(self):
        self.janela.fill(self.cor_fundo)
        pos_x = 100
        pos_y = 100
        for opcao, valores in self.opcoes.items():
            texto_opcao = self.fonte.render(opcao, True, self.cor_texto)
            self.janela.blit(texto_opcao, (pos_x, pos_y))

            if self.estado_expansao[opcao]:
                for i, valor in enumerate(valores):
                    cor = self.cor_texto if self.selecao_opcao[opcao] != valor else self.cor_selecionada
                    texto_valor = self.fonte.render(f"- {valor}", True, cor)
                    self.janela.blit(texto_valor, (pos_x + 20, pos_y + (i + 1) * 30))
                pos_y += len(valores) * 30

            pos_y += 40

        # Desenha os botões (Voltar, Salvar, Carregar)
        self.desenhar_botoes()

        pygame.display.flip()

    def desenhar_botoes(self):
        # Botões
        btns_text = ["Voltar", "Salvar", "Carregar"]
        pos_x = 400
        for i, text in enumerate(btns_text):
            texto = self.fonte.render(text, True, self.cor_texto)
            pos_y = 100 + 60 * i
            self.janela.blit(texto, (pos_x, pos_y))

    def salvar_opcoes(self):
        FILE_SEIVE = "Game/Saive/Config.json"
        dados = {key: self.selecao_opcao[key] for key in self.selecao_opcao if self.selecao_opcao[key] is not None}
        
        # Verifica se algumas opções não foram selecionadas
        if len(dados) < len(self.opcoes):
            messagebox.showinfo("Atenção", "Algumas opções não foram selecionadas.")
            return
        
        os.makedirs(os.path.dirname(FILE_SEIVE), exist_ok=True)
        with open(FILE_SEIVE, "w") as file:
            json.dump(dados, file)
        #exibe uma mensagem com as opções salvas por 10s
        label = self.fonte.render("Opções salvas com sucesso!", True, self.cor_texto)
        self.janela.blit(label, (100, 500))
        pygame.display.flip()
        pygame.time.wait(5000)

    def carregar_configuracoes(self):
        FILE_SEIVE = "Game/Saive/Config.json"
        if not os.path.exists(FILE_SEIVE):
            return
        with open(FILE_SEIVE, "r") as file:
            dados = json.load(file)
        for key in dados:
            if key in self.opcoes:
                self.selecao_opcao[key] = dados[key]
        #exibe uma mensagem com as opções carregadas por 10s
        tela = dados["Tela"]
        nivel = dados["Nivel"]
        fps = dados["FPS"]

        lavel = self.fonte.render(f"Tela: {tela} \nNivel: {nivel} \nFPS: {fps}", True, self.cor_texto)
        self.janela.blit(lavel, (100, 500))
        pygame.display.flip()
        pygame.time.wait(5000)

    def executar(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    pos_y = 100
                    for opcao in self.opcoes.keys():
                        rect = pygame.Rect(100, pos_y, 200, 30)
                        if rect.collidepoint(mouse_x, mouse_y):
                            self.estado_expansao[opcao] = not self.estado_expansao[opcao]
                        if self.estado_expansao[opcao]:
                            for i, valor in enumerate(self.opcoes[opcao]):
                                rect_sub = pygame.Rect(120, pos_y + (i + 1) * 30, 200, 30)
                                if rect_sub.collidepoint(mouse_x, mouse_y):
                                    self.selecao_opcao[opcao] = valor
                            pos_y += len(self.opcoes[opcao]) * 30
                        pos_y += 40

                    rect_back = pygame.Rect(400, 100, 100, 30)  # Botão Voltar
                    if rect_back.collidepoint(mouse_x, mouse_y):
                        running = False  # Sai das configurações e volta ao menu
                    
                    rect_save = pygame.Rect(400, 160, 100, 30)  # Botão Salvar
                    if rect_save.collidepoint(mouse_x, mouse_y):
                        self.salvar_opcoes()
                    
                    rect_load = pygame.Rect(400, 220, 100, 30)  # Botão Carregar
                    if rect_load.collidepoint(mouse_x, mouse_y):
                        self.carregar_configuracoes()

            self.desenhar_opcoes()
