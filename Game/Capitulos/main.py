import pygame
import subprocess
import json

class Preparar_game:
    def __init__(self, janela, dados):
        self.janela = janela
        self.dados = dados

    def cap_carregar(self):
        cap = self.dados.get("Capitulo", "default_capitulo")  # Pega o capítulo ou um valor padrão
        tex_vex = self.dados.get("Tex_vex", "default_tex_vex")  # Pega o texto ou um valor padrão
        # Aqui você pode fazer o que precisar com cap e tex_vex, como configurar variáveis ou preparar a tela

    def chamar_cap(self):
        cap = self.dados.get("Capitulo", "default_capitulo")  # Pega o capítulo ou um valor padrão
        # Passar os dados para o script do capítulo
        with open("Game/Capitulos/dados.json", "w") as file:
            json.dump(self.dados, file)

        subprocess.run(["python", f"Game/Capitulos/Cap_{cap}.py"])
