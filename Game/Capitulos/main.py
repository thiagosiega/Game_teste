import pygame
import sys
import os
import json

class Janela:
    BUTTONS = [
        {"rect": pygame.Rect(50, 550, 100, 50), "texto": "Salvar"},
        {"rect": pygame.Rect(200, 550, 130, 50), "texto": "Carregar"},
        {"rect": pygame.Rect(350, 550, 100, 50), "texto": "Sair"}
    ]
    
    def __init__(self, size, title):
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.background_image = None
        self.dialog_text = ""
        self.font = pygame.font.SysFont(None, 36)
        self.text_box_position = (50, 500)  # Posição da caixa de texto

    def update(self):
        """Limpa a tela e redesenha."""
        self.screen.fill((0, 0, 0))
        self.draw()

    def draw(self):
        """Desenha o conteúdo da janela."""
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))

        if self.dialog_text:
            self.desenha_caixa_texto(self.dialog_text)

        self.desenha_botoes()

    def desenha_caixa_texto(self, texto):
        """Desenha uma caixa de texto com um texto fixo na tela."""
        fonte = pygame.font.SysFont(None, 32)
        
        # Limites
        MAX_WIDTH = self.screen.get_width() - 20  # Margem
        MAX_HEIGHT = 100

        # Quebra o texto em linhas que cabem na largura máxima
        words = texto.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            if fonte.size(test_line)[0] > MAX_WIDTH:
                lines.append(current_line)
                current_line = word + ' '
            else:
                current_line = test_line
        lines.append(current_line)

        # Verifica se o texto excede a altura máxima
        if len(lines) * fonte.get_height() > MAX_HEIGHT:
            lines = lines[:MAX_HEIGHT // fonte.get_height()]

        # Calcula a posição da caixa de texto
        screen_size = self.screen.get_size()
        largura_caixa = MAX_WIDTH + 20  # Adiciona padding
        altura_caixa = min(len(lines) * fonte.get_height() + 20, MAX_HEIGHT)  # Adiciona padding e limita a altura

        x = (screen_size[0] - largura_caixa) // 2
        y = screen_size[1] - altura_caixa - 60  # Ajuste a posição vertical para não sobrepor os botões

        # Desenha a caixa de texto
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, largura_caixa, altura_caixa))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, largura_caixa, altura_caixa), 2)

        # Desenhar o texto dentro da caixa de texto
        y_offset = y + 10
        for line in lines:
            text_surface = fonte.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (x + 10, y_offset))
            y_offset += fonte.get_height()

    def desenha_botoes(self):
        """Desenha os botões na tela."""
        for btn in self.BUTTONS:
            cor = (0, 0, 255) if btn["rect"].collidepoint(pygame.mouse.get_pos()) else (0, 0, 180)
            pygame.draw.rect(self.screen, cor, btn["rect"])
            texto = self.font.render(btn["texto"], True, (255, 255, 255))
            self.screen.blit(texto, (btn["rect"].x + 10, btn["rect"].y + 10))

    def salvar_jogo(self):
        """Salva o jogo."""
        dados = self.gerar_dados_jogo()
        FILE_SAVE = f"Game/Save/{sys.argv[3]}.json"
        self.salvar_dados_em_arquivo(dados, FILE_SAVE)
        
    def gerar_dados_jogo(self):
        """Gera os dados do jogo para salvar."""
        """
        {"nome": "thiago", "vida": 100, "mana": 100, "Itens": [], "Capitulo": 1, "Tex_vex": 1}
        """
        return {
            "Capitulo": sys.argv[1],
            "Tex_vex": sys.argv[2]
        }
        
    def salvar_dados_em_arquivo(self, dados, caminho_arquivo):
        """atualiza o json."""
        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
        try:
            with open(caminho_arquivo, "w") as file:
                json.dump(dados, file)
            print("Jogo salvo com sucesso!")
        except IOError as e:
            print(f"Erro ao salvar o jogo: {e}")
        
        
    def carregar_save(self):
        """Carrega o arquivo de save do jogador."""
        FILE_SAVE = f"Game/Save/{sys.argv[3]}.json"
        if os.path.exists(FILE_SAVE):
            with open(FILE_SAVE, "r") as file:
                self.arquivo_salvo = json.load(file)
                # Atualizando o estado
                sys.argv[1] = self.arquivo_salvo["Capitulo"]
                sys.argv[2] = self.arquivo_salvo["Tex_vex"]
                self.draw()
        else:
            print(f"Arquivo de save não encontrado: {FILE_SAVE}")

    def handle_button_click(self):
        """Detecta e lida com cliques nos botões."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        if mouse_click[0]:  # Botão esquerdo do mouse
            for btn in self.BUTTONS:
                if btn["rect"].collidepoint(mouse_pos):
                    if btn["texto"] == "Salvar":
                        self.salvar_jogo()
                    elif btn["texto"] == "Carregar":
                        self.carregar_save()
                    elif btn["texto"] == "Sair":
                        pygame.quit()
                        sys.exit()

def load_config():
    """Carrega as configurações do arquivo JSON ou usa as configurações padrão."""
    FILE_CONFIG = "Game/Saive/Config.json"
    DEFAULT_SETTINGS = {
        "Tela": "800x600",
        "Nivel": "Facil",
        "FPS": "30"
    }
    if os.path.exists(FILE_CONFIG):
        with open(FILE_CONFIG, "r", encoding='utf-8') as file:
            config = json.load(file)
    else:
        print(f"Arquivo de configuração não encontrado: {FILE_CONFIG}")
        config = DEFAULT_SETTINGS
    return config

def get_screen_size(tela_config):
    """Retorna o tamanho da tela com base na configuração fornecida."""
    if tela_config == "Full Screen":
        return (pygame.display.Info().current_w, pygame.display.Info().current_h)
    else:
        return tuple(map(int, tela_config.split('x')))

def load_scene(scene_name):
    """Carrega as informações da cena a partir do arquivo JSON."""
    file_script = f"Game/Capitulos/Cap_{sys.argv[1]}/Cap_{sys.argv[1]}.json"
    if not os.path.exists(file_script):
        print(f"Arquivo da cena não encontrado: {file_script}")
        return {}
    try:
        with open(file_script, "r", encoding='utf-8') as file:
            scenes = json.load(file)
            return scenes.get(scene_name, {})
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar o JSON: {e}")
        return {}
    except IOError as e:
        print(f"Erro ao abrir o arquivo: {e}")
        return {}

def main():
    if len(sys.argv) != 4:
        print("Número incorreto de argumentos!")
        print("Uso: python main.py <Capitulo> <Cena> <Nome>")
        return

    pygame.init()
    
    try:
        config = load_config()
        screen_size = get_screen_size(config["Tela"])

        janela = Janela(screen_size, f"Capitulo {sys.argv[1]}")
        scene_name = f"Cena_{sys.argv[2]}"
        scene = load_scene(scene_name)
        if scene:
            background_path = scene.get("background")
            if background_path:
                try:
                    background_image = pygame.image.load(background_path)
                    background_image = pygame.transform.scale(background_image, screen_size)
                    janela.background_image = background_image
                except pygame.error as e:
                    print(f"Erro ao carregar a imagem: {e}")
                    janela.background_image = None
            janela.dialog_text = scene.get("dialog", {}).get("text", "")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    scene_name = f"Cena_{int(scene_name.split('_')[1]) + 1}"
                    scene = load_scene(scene_name)
                    if scene:
                        background_path = scene.get("background")
                        if background_path:
                            try:
                                background_image = pygame.image.load(background_path)
                                background_image = pygame.transform.scale(background_image, screen_size)
                                janela.background_image = background_image
                            except pygame.error as e:
                                print(f"Erro ao carregar a imagem: {e}")
                                janela.background_image = None
                        janela.dialog_text = scene.get("dialog", {}).get("text", "")
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            janela.update()
            janela.draw()
            janela.handle_button_click()  # Lida com cliques nos botões
            pygame.display.flip()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
