import os
import shutil
import subprocess
import urllib.request
import zipfile
from tkinter import messagebox

python_instalado = False
dependencias_instaladas = False

def verificar_python():
    global python_instalado
    try:
        subprocess.run(['python', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        python_instalado = True
    except subprocess.CalledProcessError:
        python_instalado = False

def atualizar_python():
    try:
        subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
        messagebox.showinfo('Atualização', 'Pip atualizado com sucesso')
    except subprocess.CalledProcessError:
        messagebox.showerror('Atualização', 'Erro ao atualizar Pip')

def verificar_dependencias():
    global dependencias_instaladas
    dependencias = ['pygame']  # Inclua outras dependências, se necessário
    for dependencia in dependencias:
        try:
            subprocess.run(['pip', 'show', dependencia], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            dependencias_instaladas = False
            return
    dependencias_instaladas = True

def instalar_dependencias():
    try:
        subprocess.run(['pip', 'install', 'pygame'], check=True)
        messagebox.showinfo('Instalação', 'Dependências instaladas com sucesso')
    except subprocess.CalledProcessError:
        messagebox.showerror('Instalação', 'Erro ao instalar dependências')

def verificar_versao_game():
    file = "Game/V.txt"
    if os.path.exists(file):
        with open(file, 'r') as f:
            versao = f.read().strip()
        url = "https://github.com/thiagosiega/Game_teste/raw/main/Game/V.txt"
        try:
            with urllib.request.urlopen(url) as f:
                versao_online = f.read().decode('utf-8').strip()
            if versao != versao_online:
                return versao_online
        except Exception as e:
            print(f'Erro ao verificar versão: {e}')
            return None
    return None

def remover_diretorio(diretorio):
    if os.path.exists(diretorio):
        try:
            shutil.rmtree(diretorio)
            print(f'Diretório {diretorio} removido com sucesso.')
        except Exception as e:
            print(f'Erro ao remover diretório {diretorio}: {e}')
    else:
        print(f'Diretório {diretorio} não encontrado.')

def main():
    verificar_python()
    if python_instalado:
        while not dependencias_instaladas:
            verificar_dependencias()
            if not dependencias_instaladas:
                instalar_dependencias()
        versao = verificar_versao_game()
        if versao:
            resposta = messagebox.askyesno('Atualização', 'Nova versão disponível. Deseja atualizar?')
            if resposta:
                # Remove a pasta Game
                remover_diretorio('Game')
                
                # Baixa o repositório como ZIP
                url = "https://github.com/thiagosiega/Game_teste/archive/refs/heads/main.zip"
                arquivo_zip = 'Game_teste.zip'
                urllib.request.urlretrieve(url, arquivo_zip)
                
                # Extrai o conteúdo do ZIP
                with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
                    zip_ref.extractall('Game_teste')
                
                # Substitui a pasta Game
                caminho_game_extraido = 'Game_teste/Game_teste-main/Game'
                if os.path.exists(caminho_game_extraido):
                    shutil.move(caminho_game_extraido, 'Game')
                
                # Remove arquivos e pastas temporárias
                remover_diretorio('Game_teste')
                os.remove(arquivo_zip)
                
                # Atualiza a versão
                with open('Game/V.txt', 'w') as f:
                    f.write(versao)
                    
                subprocess.run(['python', 'Game/Game.py'])
            else:
                subprocess.run(['python', 'Game/Game.py'])
        else:
            messagebox.showerror('Erro', 'Erro ao verificar versão')
            subprocess.run(['python', 'Game/Game.py'])
    else:
        messagebox.showerror('Erro', 'Python não está instalado. Por favor, instale o Python.')

if __name__ == '__main__':
    main()
