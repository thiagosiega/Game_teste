import pygame

class Janela_cap:
    def __init__(self, tamanho, titulo):
        self.tamanho = tamanho
        self.titulo = titulo
        self.fundo = None
        self.texto_dialogo = ""
        self.fonte = pygame.font.Font(None, 36)
        self.cor_texto = (38, 182, 137)
        self.tela = pygame.display.set_mode(tamanho)
        pygame.display.set_caption(titulo)

    def definir_texto_dialogo(self, texto):
        """Define o texto do diálogo e atualiza a tela."""
        self.texto_dialogo = texto
        self.atualizar()

    def atualizar(self):
        """Atualiza a tela com a caixa de diálogo e o fundo."""
        # Limpa a tela com uma cor de fundo
        self.tela.fill((0, 0, 0))  # Cor preta para teste

        # Desenha o fundo na tela
        if self.fundo:
            self.tela.blit(self.fundo, (0, 0))
        
        # Desenha a caixa de diálogo
        if self.texto_dialogo:
            self.desenhar_caixa_dialogo(self.texto_dialogo)
        
        # Atualiza a tela
        pygame.display.flip() 

    def quebrar_texto(self, texto, largura_max):
        """Quebra o texto em várias linhas para se ajustar à largura máxima."""
        palavras = texto.split(" ")
        linhas = []
        linha_atual = ""
        for palavra in palavras:
            nova_linha = f"{linha_atual} {palavra}".strip()
            if self.fonte.size(nova_linha)[0] <= largura_max:
                linha_atual = nova_linha
            else:
                if linha_atual:
                    linhas.append(linha_atual)
                linha_atual = palavra
        if linha_atual:
            linhas.append(linha_atual)
        return linhas

    def desenhar_caixa_dialogo(self, texto):
        """Desenha uma caixa de diálogo com o texto fornecido."""
        largura, altura = self.tela.get_size()
        largura_max = largura - 20
        altura_max = 100

        # Desenha a caixa de diálogo
        pygame.draw.rect(self.tela, (255, 255, 255), (10, altura - altura_max - 10, largura_max, altura_max))
        
        # Quebra o texto em linhas
        linhas = self.quebrar_texto(texto, largura_max)
        
        # Renderiza e desenha cada linha do texto
        y = altura - altura_max + 10
        for linha in linhas:
            texto_surface = self.fonte.render(linha, True, self.cor_texto)
            self.tela.blit(texto_surface, (15, y))
            y += self.fonte.get_linesize()

    def fechar(self):
        """Fecha o Pygame e encerra o programa."""
        pygame.quit()
        quit()
