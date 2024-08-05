import pygame
import json  # Adicione esta linha

class Inicio:
    def __init__(self, janela):
        self.janela = janela
        self.fonte = pygame.font.SysFont(None, 24)
        self.cor_texto = (255, 255, 255)
        self.cor_selecionada = (0, 255, 0)
        self.opcoes = ["Novo Jogo", "Sair"]
        self.selecao_opcao = 0  # Inicialize com 0
        self.seives = []
    
    def desenhar_opcoes(self):
        self.janela.fill((0, 0, 0))
        pos_x = 100
        pos_y = 100
        for i, opcao in enumerate(self.opcoes):
            cor = self.cor_texto if self.selecao_opcao != i else self.cor_selecionada
            texto_opcao = self.fonte.render(opcao, True, cor)
            self.janela.blit(texto_opcao, (pos_x, pos_y + 60 * i))
        
        pygame.display.update()  # Atualize a tela após desenhar
    
    def Novo_jogo(self, nome):  # Corrigido para receber nome como argumento
        self.nome = nome
        self.infor = [
            "Nome: " + self.nome,
            "Vida: 100",
            "Dano: 10",
            "Defesa: 5",
            "Capitulo: 1", 
            "Nivel: 1",
            "Experiencia: 0",
            "Texto: 0"
        ]
        self.salvar()

    def salvar(self):
        self.seives.append(self.infor)
        with open("Game/Saive/Config.json", "w") as file:
            json.dump(self.seives, file)

    def exibir_seive(self):
        with open("Game/Saive/Config.json", "r") as file:
            self.seives = json.load(file)
        for i, seive in enumerate(self.seives):
            print(f"Seive {i}")
            for info in seive:
                print(info)
            print()

    def executar(self):
        try:
            while True:
                self.desenhar_opcoes()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.selecao_opcao = (self.selecao_opcao - 1) % len(self.opcoes)
                        elif event.key == pygame.K_DOWN:
                            self.selecao_opcao = (self.selecao_opcao + 1) % len(self.opcoes)
                        elif event.key == pygame.K_RETURN:
                            if self.selecao_opcao == 0:
                                nome = "Jogador"  # Substitua pelo nome real ou obtenha de outra forma
                                self.Novo_jogo(nome)
                            elif self.selecao_opcao == 1:
                                pygame.quit()
                                exit()
        except Exception as e:
            print(e)
            pygame.quit()
            exit()
