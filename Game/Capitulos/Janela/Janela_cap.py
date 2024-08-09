import pygame

class Janela_cap:
    def __init__(self, tamanho, titulo):
        self.tamanho = tamanho
        self.titulo = titulo
        self.tela = pygame.display.set_mode(tamanho)
        pygame.display.set_caption(titulo)
        self.fundo = None

    def definir_fundo(self, imagem):
        """Carrega e redimensiona a imagem de fundo para se ajustar ao tamanho da tela."""
        if imagem:
            try:
                # Carrega a imagem de fundo
                self.fundo = pygame.image.load(imagem)
                # Obtém o tamanho da tela
                largura, altura = self.tela.get_size()
                # Redimensiona a imagem para o tamanho da tela
                self.fundo = pygame.transform.scale(self.fundo, (largura, altura))
            except pygame.error as e:
                print(f"Erro ao carregar a imagem de fundo: {e}")
                self.fundo = None

    def atualizar(self):
        # Limpa a tela com uma cor de fundo (opcional)
        self.tela.fill((0, 0, 0))  # Cor preta para teste

        # Desenha o fundo na tela
        if self.fundo:
            self.tela.blit(self.fundo, (0, 0))
        
        # Desenha a caixa de diálogo
        if hasattr(self, 'texto_dialogo'):
            self.caixa_dialogo(self.texto_dialogo)
        
        # Atualiza a tela
        pygame.display.flip()


    def caixa_dialogo(self, texto):
        """Desenha uma caixa de diálogo na tela."""
        x = 20
        y = 20
        latura = 500
        altura = 100

        # Desenha a caixa de diálogo
        pygame.draw.rect(self.tela, (255, 255, 255), (x, y, latura, altura))
        # Desenha o texto na caixa de diálogo
        fonte = pygame.font.SysFont(None, 24)
        texto = fonte.render(texto, True, (0, 0, 0))
        self.tela.blit(texto, (x + 10, y + 10))
        


    def fechar(self):
        """Fecha o Pygame e encerra o programa."""
        pygame.quit()
        quit()
