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
        self.btns = []
        self.input_ativo = False
        self.nome_jogador = ""
        self.arquivo_salvo = None
        self.img_fundo = pygame.image.load("Game/Fundo1.png")

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
        FILE_SAVE = f"Game/Save/{self.nome_jogador}.json"
        dados = {
            "nome": self.nome_jogador,
            "vida": 100,
            "mana": 100,
            "Itens": [],
            "Capitulo": 1,
            "Tex_vex": 1
        }
        os.makedirs(os.path.dirname(FILE_SAVE), exist_ok=True)
        try:
            with open(FILE_SAVE, "w") as file:
                json.dump(dados, file)
            print("Jogo salvo com sucesso!")
        except IOError as e:
            print(f"Erro ao salvar o jogo: {e}")

    def apagar_save(self):
        self.janela.fill(self.cor_fundo)
        label = self.fonte.render("Escolha o save a ser apagado:", True, self.cor_texto)
        self.janela.blit(label, (100, 50))
        
        y_offset = 100
        file_rects = []
        for file in os.listdir("Game/Save"):
            if file.endswith(".json"):
                with open(os.path.join("Game/Save", file), "r") as f:
                    dados = json.load(f)
                    btn = pygame.Rect(100, y_offset, 200, 40)
                    pygame.draw.rect(self.janela, self.cor_botao, btn)
                    texto = self.fonte.render(f"{dados['nome']}", True, self.cor_texto)
                    self.janela.blit(texto, (btn.x + 10, btn.y + 10))
                    file_rects.append((btn, os.path.join("Game/Save", file)))
                    y_offset += 60

        pygame.display.update()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, filepath in file_rects:
                        if rect.collidepoint(pygame.mouse.get_pos()):
                            os.remove(filepath)
                            self.carregar_save()
                            return True  # Retorna para o loop principal

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True  # Retorna ao menu principal

        pygame.display.update()

    def carregar_save(self):
        self.janela.fill(self.cor_fundo)
        FILE_SAVE = "Game/Save/"
        if not os.path.exists(FILE_SAVE):
            os.makedirs(FILE_SAVE)
        self.btns = [
            {"texto": "Novo Jogo", "rect": pygame.Rect(400, 100, 200, 40)},
            {"texto": "Sair", "rect": pygame.Rect(400, 220, 200, 40)},
            {"texto": "Apagar", "rect": pygame.Rect(400, 340, 200, 40)}
        ]
        y_offset = 50
        for file in os.listdir(FILE_SAVE):
            if file.endswith(".json"):
                with open(os.path.join(FILE_SAVE, file), "r") as f:
                    dados = json.load(f)
                    self.btns.append({
                        "texto": f"Continuar - {dados['nome']}",
                        "rect": pygame.Rect(100, y_offset, 200, 40),
                        "arquivo": os.path.join(FILE_SAVE, file)
                    })
                    y_offset += 60

    def continuar_jogo(self, arquivo_salvo):
        self.arquivo_salvo = arquivo_salvo
        #le o arquivo
        with open(arquivo_salvo, "r") as file:
            dados = json.load(file)
            capitulo = dados["Capitulo"]
            tex_vex = dados["Tex_vex"]
            nome = dados["nome"]
            print(f"Continuando o jogo de {nome} no capítulo {capitulo} com {tex_vex} tex_vex")
            subprocess.run(["python", "Game/Capitulos/main.py", str(capitulo), str(tex_vex), nome])


    def lidar_com_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.btns:
                    if btn["rect"].collidepoint(pygame.mouse.get_pos()):
                        if btn["texto"] == "Novo Jogo":
                            self.input_ativo = True
                        elif btn["texto"].startswith("Continuar"):
                            self.continuar_jogo(btn.get("arquivo"))
                        elif btn["texto"] == "Apagar":
                            if self.apagar_save() is False:
                                return False
                        elif btn["texto"] == "Sair":
                            return False

            elif event.type == pygame.KEYDOWN:
                if self.input_ativo:
                    if event.key == pygame.K_RETURN:
                        if self.nome_jogador:
                            self.novo_jogo()
                            self.input_ativo = False
                            self.nome_jogador = ""
                            self.carregar_save()
                        else:
                            print("Nome do jogador não pode estar vazio!")
                    elif event.key == pygame.K_BACKSPACE:
                        self.nome_jogador = self.nome_jogador[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        self.input_ativo = False
                    else:
                        if len(self.nome_jogador) < 20:
                            self.nome_jogador += event.unicode

        return True

    def executar(self):
        clock = pygame.time.Clock()  # Controle de taxa de atualização
        running = True
        while running:
            fundo = pygame.transform.scale(self.img_fundo, (self.largura, self.altura))
            self.janela.blit(fundo, (0, 0))
            self.desenhar_botoes()
            if not self.lidar_com_eventos():
                break
            pygame.display.update()
            clock.tick(60)  # Atualiza a 60 FPS
