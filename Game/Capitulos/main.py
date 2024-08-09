import argparse
import pygame
import json

# Importa as classes
from Janela.Janela_cap import Janela_cap
from Player.Player import player

FILE_SCRIPT = "Game/Capitulos/Cap_1/Cap_1.json"
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

def leitura_script(tex_vex):
    try:
        with open(FILE_SCRIPT, "r", encoding="utf-8") as f:
            script = json.load(f)
        chave_cena = f"Cena_{tex_vex}"
        if chave_cena in script:
            text_vex = script[chave_cena]["dialog"]["text"]
            background = script[chave_cena]["background"]
            return text_vex, background
        else:
            raise ValueError(f"A cena {chave_cena} não existe no script.")
    except FileNotFoundError:
        raise FileNotFoundError("O arquivo de script não foi encontrado.")
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
        return fundo
    except pygame.error as e:
        print(f"Erro ao carregar a imagem de fundo: {e}")
        return None
    

def Criar_janela(capitulo, tex_vex, nome):
    pygame.init()
    infro_player = f"Game/Save/{nome}.json"
    
    player_config = leitura_json(infro_player)
    jogador = player_atribuicao(player_config)
    
    config = leitura_json(FILE_CONFIG)
    
    tamanho = tuple(map(int, config["Tela"].split("x")))
    titulo = config["Nivel"]
    janela = Janela_cap(tamanho, titulo)
    try:
        infor = leitura_script(tex_vex)
        imagem = infor[1]
        janela.definir_fundo(imagem)
        janela.caixa_dialogo(infor[0])
    except (ValueError, KeyError) as e:
        print(e)
    
    cena = int(capitulo)  # Converte o capítulo para um inteiro
    
    while True:
        janela.atualizar()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                janela.fechar()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cena += 1
                    try:
                        infor = leitura_script(cena)
                        janela.caixa_dialogo(infor[0])
                    except (ValueError, KeyError) as e:
                        print(e)
                elif event.key == pygame.K_ESCAPE:
                    janela.fechar()
                    return
                elif event.key == pygame.K_s:
                    try:
                        if cena >= 5:
                            jogador.vida = 10
                            jogador.mana = 10
                            jogador.Capitulo = 2
                            jogador.Tex_vex = 0
                        else:
                            jogador.Capitulo = 1
                            jogador.Tex_vex = cena
                        salvar_player(jogador, infro_player)
                        print("Jogo salvo com sucesso!")
                    except (FileNotFoundError, ValueError) as e:
                        print(e)

if __name__ == "__main__":
    args = parse_arguments()
    Criar_janela(args.capitulo, args.tex_vex, args.nome)

