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
        self.cor_botao = (0, 0, 255)  # Cor azul para o fundo do botão
        self.fonte = pygame.font.SysFont(None, 24)
        self.opcoes = {
            "Tela": ["800x600", "1024x768", "1280x720", "1920x1080", "Full Screen"],
            "Nivel": ["Facil", "Medio", "Dificil", "Insano", "Faça seu pior"],
            "FPS": ["10", "20", "30", "60"]
        }
        self.estado_expansao = {key: False for key in self.opcoes}
        self.selecao_opcao = {key: None for key in self.opcoes}
        self.fundo = pygame.image.load("Game/Fundo.jpg")

    def desenhar_fundo(self):
        self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))
        self.janela.blit(self.fundo, (0, 0))

    def desenhar_opcoes(self):
        pos_x = self.largura // 10
        pos_y = self.altura // 10
        
        for opcao, valores in self.opcoes.items():
            self._desenhar_texto(opcao, pos_x, pos_y)
            pos_y += 40

            if self.estado_expansao[opcao]:
                pos_y = self._desenhar_opcoes_expandidas(opcao, valores, pos_x, pos_y)

    def _desenhar_opcoes_expandidas(self, opcao, valores, pos_x, pos_y):
        for valor in valores:
            cor = self.cor_selecionada if valor == self.selecao_opcao.get(opcao) else self.cor_texto
            self._desenhar_texto(valor, pos_x + 20, pos_y, cor)
            pos_y += 30
        return pos_y + 10

    def _desenhar_texto(self, texto, x, y, cor=None):
        cor = cor or self.cor_texto
        renderizado = self.fonte.render(texto, True, cor)
        self.janela.blit(renderizado, (x, y))

    def desenhar_botoes(self):
        btns_text = ["Voltar", "Salvar", "Carregar"]
        largura_botao = 120
        altura_botao = 40
        margem_x = (self.largura - largura_botao) // 2
        pos_y = self.altura - (3 * altura_botao + 40)

        for i, text in enumerate(btns_text):
            pos_y_atual = pos_y + i * (altura_botao + 10)
            self._desenhar_botao(text, margem_x, pos_y_atual, largura_botao, altura_botao)

    def _desenhar_botao(self, texto, x, y, largura, altura):
        retangulo = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(self.janela, self.cor_botao, retangulo)
        texto_renderizado = self.fonte.render(texto, True, self.cor_texto)
        texto_rect = texto_renderizado.get_rect(center=retangulo.center)
        self.janela.blit(texto_renderizado, texto_rect)

    def salvar_opcoes(self):
        FILE_SAVE = "Game/Saive/Config.json"
        dados = {key: self.selecao_opcao[key] for key in self.selecao_opcao if self.selecao_opcao[key] is not None}
        
        if len(dados) < len(self.opcoes):
            messagebox.showinfo("Atenção", "Algumas opções não foram selecionadas.")
            return
        
        os.makedirs(os.path.dirname(FILE_SAVE), exist_ok=True)
        try:
            with open(FILE_SAVE, "w") as file:
                json.dump(dados, file)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar as opções: {e}")
            return
        
        self._exibir_mensagem("Opções salvas com sucesso!")

    def carregar_configuracoes(self):
        FILE_SAVE = "Game/Saive/Config.json"
        if not os.path.exists(FILE_SAVE):
            return
        try:
            with open(FILE_SAVE, "r") as file:
                dados = json.load(file)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar as opções: {e}")
            return

        for key in dados:
            if key in self.opcoes:
                self.selecao_opcao[key] = dados[key]
        
        tela = dados.get("Tela", "Não definido")
        nivel = dados.get("Nivel", "Não definido")
        fps = dados.get("FPS", "Não definido")
        mensagem = f"Tela: {tela} \nNivel: {nivel} \nFPS: {fps}"
        self._exibir_mensagem(mensagem)

    def _exibir_mensagem(self, mensagem):
        self.janela.fill(self.cor_fundo)
        label = self.fonte.render(mensagem, True, self.cor_texto)
        self.janela.blit(label, (100, 500))
        pygame.display.update()
        pygame.time.wait(3000)

    def executar(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self._verificar_botao(mouse_x, mouse_y, "Voltar"):
                        running = False
                    elif self._verificar_botao(mouse_x, mouse_y, "Salvar"):
                        self.salvar_opcoes()
                    elif self._verificar_botao(mouse_x, mouse_y, "Carregar"):
                        self.carregar_configuracoes()
                    else:
                        self._verificar_opcao(mouse_x, mouse_y)

            self.desenhar_fundo()
            self.desenhar_opcoes()
            self.desenhar_botoes()
            pygame.display.update()

    def _verificar_botao(self, mouse_x, mouse_y, texto_botao):
        largura_botao = 120
        altura_botao = 40
        margem_x = (self.largura - largura_botao) // 2
        pos_y = self.altura - (3 * altura_botao + 40)
        btns_text = ["Voltar", "Salvar", "Carregar"]
        for i, text in enumerate(btns_text):
            if text == texto_botao:
                pos_y_atual = pos_y + i * (altura_botao + 10)
                return pygame.Rect(margem_x, pos_y_atual, largura_botao, altura_botao).collidepoint(mouse_x, mouse_y)
        return False

    def _verificar_opcao(self, mouse_x, mouse_y):
        pos_x = self.largura // 10
        pos_y = self.altura // 10
        for opcao, valores in self.opcoes.items():
            rect = pygame.Rect(pos_x, pos_y, 200, 30)
            if rect.collidepoint(mouse_x, mouse_y):
                self.estado_expansao[opcao] = not self.estado_expansao[opcao]
            
            if self.estado_expansao[opcao]:
                for valor in valores:
                    rect_sub = pygame.Rect(pos_x + 20, pos_y + valores.index(valor) * 30 + 40, 200, 30)
                    if rect_sub.collidepoint(mouse_x, mouse_y):
                        self.selecao_opcao[opcao] = valor
                pos_y += len(valores) * 30
            
            pos_y += 40
