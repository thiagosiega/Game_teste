import pygame
import json
import subprocess

class Pecados:
    def __init__(self, janela):
        self.janela = janela
        self.fonte = pygame.font.SysFont(None, 48)
        self.titulo = self.fonte.render("Tela de Pecados", True, (0, 0, 0))
        self.file = "Game/Pecados/Pecados.json"
        self.dados = self.carregar_dados()
        self.pagina = 1
        self.imagem_fundo = pygame.image.load("Game/Fundo1.png")
        self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, self.janela.get_size())
        self.condicao_falsa = False

    def carregar_dados(self):
        try:
            with open(self.file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"Pecados": []}
    
    def desenhar_pagina(self):
        # Exibe o fundo
        self.janela.fill((255, 255, 255))
        self.janela.blit(self.imagem_fundo, (0, 0))
        # Exibe o título
        self.janela.blit(self.titulo, (200, 100))

        # Exibe os pecados
        pecados = self.dados.get("Pecados", [])
        pecado_info = next((p["Infor"] for p in pecados if p["ID"] == self.pagina), None)
        
        if pecado_info:
            if pecado_info["Status"]:
                # Desenha nome e descrição do pecado
                nome_texto = self.fonte.render(f"Nome: {pecado_info['Name']}", True, (0, 0, 0))
                descricao_texto = self.fonte.render(f"Descrição: {pecado_info['Description']}", True, (0, 0, 0))
                self.janela.blit(nome_texto, (100, 200))
                self.janela.blit(descricao_texto, (100, 250))

                # Carregar e exibir a imagem do pecado
                imagem_path = pecado_info.get("Image")
                if imagem_path:
                    try:
                        imagem = pygame.image.load(imagem_path)
                        imagem = pygame.transform.scale(imagem, (200, 200))
                        self.janela.blit(imagem, (100, 300))
                    except pygame.error:
                        print(f"Não foi possível carregar a imagem: {imagem_path}")
            else:
                # Mensagem se o status for falso
                mensagem = self.fonte.render("Não há nada por aqui", True, (255, 0, 0))
                self.janela.blit(mensagem, (100, 200))
        else:
            # Mensagem se não houver informação para a página atual
            erro_texto = self.fonte.render("Nenhum pecado encontrado para esta página.", True, (255, 0, 0))
            self.janela.blit(erro_texto, (100, 200))

    def verificar_estado_total(self):
        pecados = self.dados.get("Pecados", [])
        todos_falsos = all(p["Infor"].get("Status") == False for p in pecados)
        if todos_falsos and not self.condicao_falsa:
            self.chamar_codigo_externo()
            self.condicao_falsa = True  # Marcar que o código externo foi chamado
    
    def chamar_codigo_externo(self):
        File = "Game/Pecados/Erro.py"
        try:
            # Chama o código externo e aguarda sua execução
            subprocess.run(["python", File], check=True)
            print("Código externo executado com sucesso.")
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {File}")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o código externo: {e}")
        
        # Atualiza o status do pecado com ID 1 para True
        self.atualizar_status_pecado(1, True)

    def atualizar_status_pecado(self, id_pecado, novo_status):
        for pecado in self.dados.get("Pecados", []):
            if pecado["ID"] == id_pecado:
                pecado["Infor"]["Status"] = novo_status

        # Salva as alterações no arquivo JSON
        with open(self.file, "w") as file:
            json.dump(self.dados, file, indent=4)

    def iniciar_conexao(self):
        self.condicao_falsa = True
        self.verificar_estado_total()

    def executar(self):
        clock = pygame.time.Clock()
        rodando = True
        while rodando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        rodando = False
                    elif event.key == pygame.K_SPACE:
                        self.pagina += 1
                        if self.pagina > len(self.dados.get("Pecados", [])):
                            self.pagina = 1

            self.desenhar_pagina()
            self.verificar_estado_total()  # Verifica o estado total dos pecados
            pygame.display.update()
            clock.tick(30)
