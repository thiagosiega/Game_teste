import pygame
import sys
import os
import json

class Janela:
    def __init__(self, size, title):
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.background_image = None
        self.dialog_text = ""
        self.font = pygame.font.SysFont(None, 36)
        self.text_box_position = (50, 500)  # Posição da caixa de texto

    def update(self):
        """Atualiza os elementos da janela (se necessário)."""
        pass

    def draw(self):
        """Desenha o conteúdo da janela."""
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        # Desenha a caixa de texto com o texto dentro dela
        if self.dialog_text:
            self.desenha_caixa_texto(*self.text_box_position, (0, 0, 0), (255, 255, 255), self.dialog_text, (255, 255, 255))

    def desenha_caixa_texto(self, x, y, cor_fundo, cor_borda, texto, cor_texto):
        """Desenha uma caixa de texto com um texto fixo na tela."""
        altura = 40
        largura = 200
        fonte = pygame.font.SysFont(None, 32)

        # Desenhar a caixa de texto
        pygame.draw.rect(self.screen, cor_fundo, (x, y, largura, altura))
        pygame.draw.rect(self.screen, cor_borda, (x, y, largura, altura), 2)

        # Desenhar o texto dentro da caixa de texto
        text_surface = fonte.render(texto, True, cor_texto)
        self.screen.blit(text_surface, (x + 5, y + 5))


def load_config():
    """Carrega as configurações do arquivo JSON ou usa as configurações padrão."""
    FILE_CONFIG = "Game/Saive/Config.json"
    DEFAULT_SETTINGS = {
        "Tela": "800x600",
        "Nivel": "Facil",
        "FPS": "30"
    }
    if os.path.exists(FILE_CONFIG):
        with open(FILE_CONFIG, "r") as file:
            config = json.load(file)
    else:
        config = DEFAULT_SETTINGS
        with open(FILE_CONFIG, "w") as file:
            json.dump(config, file)
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
    with open(file_script, "r") as file:
        scenes = json.load(file)
        return scenes.get(scene_name, {})

def main():
    if len(sys.argv) != 3:
        print("Número incorreto de argumentos!")
        print("Uso: python main.py <Capitulo> <Tex_vex>")
        return

    pygame.init()
    
    try:
        config = load_config()
        screen_size = get_screen_size(config["Tela"])

        janela = Janela(screen_size, f"Capitulo {sys.argv[1]}")
        
        # Carregar a cena inicial
        scene_name = "Cena_1"  # Você pode mudar isso conforme necessário
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
                    return
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

            janela.update()
            janela.draw()
            pygame.display.flip()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
