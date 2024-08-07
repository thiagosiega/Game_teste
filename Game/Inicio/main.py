import pygame
import json
import os
import subprocess

class Inicio:
    def __init__(self, janela):
        self.janela = janela.get_surface()
        self.largura, self.altura = self.janela.get_size()
        self.cor_fundo = (0, 0, 0)
        self.cor_texto = (255, 255, 255)
        self.cor_botao = (0, 0, 255)
        self.cor_botao_hover = (0, 0, 180)
        self.fonte = pygame.font.SysFont(None, 24)
        self.btns = [
            {"texto": "Novo Jogo", "rect": pygame.Rect(400, 100, 200, 40)},
            {"texto": "Sair", "rect": pygame.Rect(400, 220, 200, 40)}
        ]
        self.input_ativo = False
        self.nome_jogador = ""

        # Carregar configurações de save
        self.carregar_save()

    def desenhar_botoes(self):
        for btn in self.btns:
            cor = self.cor_botao_hover if btn["rect"].collidepoint(pygame.mouse.get_pos()) else self.cor_botao
            pygame.draw.rect(self.janela, cor, btn["rect"])
            texto = self.fonte.render(btn["texto"], True, self.cor_texto)
            self.janela.blit(texto, (btn["rect"].x + 10, btn["rect"].y + 10))

        if self.input_ativo:
            pygame.draw.rect(self.janela, (200, 200, 200), pygame.Rect(300, 300, 200, 40))
            texto_entrada = self.fonte.render(self.nome_jogador, True, (0, 0, 0))
            self.janela.blit(texto_entrada, (310, 310))
            label = self.fonte.render("Digite o nome do jogador:", True, self.cor_texto)
            self.janela.blit(label, (300, 270))

    def novo_jogo(self):
        FILE_SAVE = "Game/Save/Save.json"
        dados = {
            "nome": self.nome_jogador,
            "vida": 100,
            "mana": 100,
            "Itens": [],
            "Capitulo": 1,
            "Tex_vex": 0
        }
        os.makedirs(os.path.dirname(FILE_SAVE), exist_ok=True)
        with open(FILE_SAVE, "w") as file:
            json.dump(dados, file)
        print("Jogo salvo com sucesso!")

    def carregar_save(self):
        FILE_SAVE = "Game/Save/Save.json"
        if os.path.exists(FILE_SAVE):
            with open(FILE_SAVE, "r") as file:
                dados = json.load(file)
                # Verificar e corrigir tipos dos dados
                if isinstance(dados["Capitulo"], str):
                    dados["Capitulo"] = int(dados["Capitulo"])
                if isinstance(dados["Tex_vex"], str):
                    dados["Tex_vex"] = int(dados["Tex_vex"])
                self.btns[0]["texto"] = f"Continuar: {dados['nome']}"
        else:
            self.btns[0]["texto"] = "Novo Jogo"

    def lidar_com_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.btns:
                    if btn["rect"].collidepoint(event.pos):
                        if btn["texto"].startswith("Continuar"):
                            with open("Game/Save/Save.json", "r") as file:
                                dados = json.load(file)
                                # Iniciar o jogo com dados carregados
                                subprocess.Popen(["python", "Game/Capitulos/main.py", str(dados["Capitulo"]), str(dados["Tex_vex"])])
                        elif btn["texto"] == "Novo Jogo":
                            self.input_ativo = True
                        elif btn["texto"] == "Sair":
                            return False

            elif event.type == pygame.KEYDOWN:
                if self.input_ativo:
                    if event.key == pygame.K_RETURN:
                        if self.nome_jogador:
                            self.novo_jogo()
                            self.input_ativo = False
                            self.nome_jogador = ""
                            self.carregar_save()  # Atualizar o texto do botão após salvar
                        else:
                            print("Nome do jogador não pode estar vazio!")
                    elif event.key == pygame.K_BACKSPACE:
                        self.nome_jogador = self.nome_jogador[:-1]
                    else:
                        if len(self.nome_jogador) < 20:  # Limite de caracteres
                            self.nome_jogador += event.unicode

        return True

    def executar(self):
        running = True
        while running:
            self.janela.fill(self.cor_fundo)
            self.desenhar_botoes()
            if not self.lidar_com_eventos():
                break
            pygame.display.update()
