import pygame
import json
import argparse


from Janela.Janela_cap import Janela_cap
from Player.Player import player
from tkinter import messagebox

FILE_CONFIG = "Game/Saive/Config.json"

def parse_arguments():
    parser = argparse.ArgumentParser(description="Executa o jogo com os parâmetros fornecidos.")
    parser.add_argument('capitulo', type=str, help="Número do capítulo")
    parser.add_argument('tex_vex', type=str, help="Texto do vex")
    parser.add_argument('nome', type=str, help="Nome do jogador")
    return parser.parse_args()

def leitura_json(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("O arquivo não foi encontrado.")
    except json.JSONDecodeError:
        raise ValueError("Erro ao decodificar o arquivo JSON.")

def player_atribuicao(config):
    try:
        nome = config["nome"]
        vida = config["vida"]
        mana = config["mana"]
        itens = config["Itens"]
        Capitulo = config["Capitulo"]
        Tex_vex = config["Tex_vex"]
        return player(nome, vida, mana, Capitulo, Tex_vex)
    except KeyError as e:
        raise KeyError(f"Chave ausente no arquivo de configuração: {e}")

def leitura_script(tex_vex, file_script):
    try:
        with open(file_script, "r", encoding="utf-8") as f:
            script = json.load(f)
        chave_cena = f"Cena_{tex_vex}"
        if chave_cena in script:
            text_vex = script[chave_cena]["dialog"]["text"]
            background = script[chave_cena]["background"]
            return text_vex, background
        else:
            raise ValueError(f"A cena {chave_cena} não existe no script.")
    except FileNotFoundError:
        messagebox.showerror("Erro", "O arquivo não foi encontrado,Script faltando ou corrompido.")
    except json.JSONDecodeError:
        raise ValueError("Erro ao decodificar o arquivo JSON.")
    except KeyError as e:
        raise KeyError(f"Chave ausente no script: {e}")

def salvar_player(player_obj, arquivo):
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(player_obj.salvar(), f, indent=4)
    except FileNotFoundError:
        raise FileNotFoundError("O arquivo não foi encontrado.")
    except ValueError:
        raise ValueError("Erro ao codificar os dados para JSON.")

def carregar_fundo(imagem):
    try:
        fundo = pygame.image.load(imagem)
        # Redimensiona a imagem para o tamanho da tela
        fundo = pygame.transform.scale(fundo, (800, 600))
        return fundo
    except pygame.error as e:
        print(f"Erro ao carregar a imagem de fundo: {e}")
        return None

def caixa_dialogo(janela, texto):
    """Desenha uma caixa de diálogo com o texto fornecido."""
    fonte = pygame.font.Font(None, 36)
    cor = (38, 182, 137)
    texto_surface = fonte.render(texto, True, cor)
    largura, altura = janela.tela.get_size()
    posicao = (largura // 2 - texto_surface.get_width() // 2, altura - texto_surface.get_height() - 20)
    janela.tela.blit(texto_surface, posicao)

def Criar_janela(capitulo, tex_vex, nome):
    pygame.init()
    infro_player = f"Game/Save/{nome}.json"
    
    FILE_SCRIPT = f"Game/Capitulos/Cap_{capitulo}/Cap_{capitulo}.json"
    
    player_config = leitura_json(infro_player)
    jogador = player_atribuicao(player_config)
    
    config = leitura_json(FILE_CONFIG)
    
    tamanho = tuple(map(int, config["Tela"].split("x")))
    titulo = config["Nivel"]
    janela = Janela_cap(tamanho, titulo)

    texto_vex, imagem_fundo = leitura_script(tex_vex, FILE_SCRIPT)
    janela.fundo = carregar_fundo(imagem_fundo)
    janela.definir_texto_dialogo(texto_vex)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salvar_player(jogador, infro_player)
                janela.fechar()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Atualiza o texto e a imagem de fundo para o próximo
                    tex_vex = str(int(tex_vex) + 1)
                    try:
                        texto_vex, imagem_fundo = leitura_script(tex_vex, FILE_SCRIPT)
                        janela.fundo = carregar_fundo(imagem_fundo)
                        janela.definir_texto_dialogo(texto_vex)
                    except (ValueError, FileNotFoundError, KeyError) as e:
                        # Altera o capítulo e o texto do vex do jogador
                        jogador.Capitulo = str(int(capitulo) + 1)
                        jogador.Tex_vex = 1
                        # Salva as informações do jogador
                        infor_player = jogador.salvar()
                        FILE_SAVE = f"Game/Save/{nome}.json"
                        try:
                            with open(FILE_SAVE, "w", encoding="utf-8") as f:
                                json.dump(infor_player, f, indent=4)
                        except (FileNotFoundError, ValueError) as save_error:
                            print(f"Erro ao salvar o arquivo: {save_error}")
                        
                        # Fecha o jogo
                        salvar_player(jogador, infro_player)
                        janela.fechar()
                        return
                
                elif event.key == pygame.K_s:
                    # Atualiza o capítulo e o texto do vex
                    jogador.Capitulo = capitulo
                    jogador.Tex_vex = tex_vex
                    # Salva as informações do jogador
                    infor_player = jogador.salvar()
                    FILE_SAVE = f"Game/Save/{nome}.json"
                    try:
                        with open(FILE_SAVE, "w", encoding="utf-8") as f:
                            json.dump(infor_player, f, indent=4)
                    except (FileNotFoundError, ValueError) as save_error:
                        print(f"Erro ao salvar o arquivo: {save_error}")

        janela.atualizar()
        caixa_dialogo(janela, janela.texto_dialogo)
        pygame.time.delay(100)

if __name__ == "__main__":
    args = parse_arguments()
    Criar_janela(args.capitulo, args.tex_vex, args.nome)
