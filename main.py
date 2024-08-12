import os
import shutil
import subprocess
import urllib.request
import zipfile
from tkinter import messagebox

def verificar_python():
    try:
        subprocess.run(['python', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def atualizar_pip():
    try:
        subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
        messagebox.showinfo('Atualização', 'Pip atualizado com sucesso')
    except subprocess.CalledProcessError:
        messagebox.showerror('Atualização', 'Erro ao atualizar Pip')

def verificar_dependencias(dependencias):
    for dependencia in dependencias:
        try:
            subprocess.run(['pip', 'show', dependencia], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            return False
    return True

def instalar_dependencias(dependencias):
    try:
        for dependencia in dependencias:
            subprocess.run(['pip', 'install', dependencia], check=True)
        messagebox.showinfo('Instalação', 'Dependências instaladas com sucesso')
    except subprocess.CalledProcessError:
        messagebox.showerror('Instalação', 'Erro ao instalar dependências')

def verificar_versao_game(arquivo_versao, url_versao):
    if os.path.exists(arquivo_versao):
        with open(arquivo_versao, 'r') as f:
            versao_local = f.read().strip()
        try:
            with urllib.request.urlopen(url_versao) as f:
                versao_online = f.read().decode('utf-8').strip()
            return versao_online if versao_local != versao_online else None
        except Exception as e:
            print(f'Erro ao verificar versão: {e}')
    return None

def remover_diretorio(diretorio):
    if os.path.exists(diretorio):
        try:
            shutil.rmtree(diretorio)
            print(f'Diretório {diretorio} removido com sucesso.')
        except Exception as e:
            print(f'Erro ao remover diretório {diretorio}: {e}')

def atualizar_game(url_zip, pasta_extraida, pasta_game):
    arquivo_zip = 'Game_teste.zip'
    try:
        # Baixa o repositório como ZIP
        urllib.request.urlretrieve(url_zip, arquivo_zip)
        
        # Extrai o conteúdo do ZIP
        with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
            zip_ref.extractall(pasta_extraida)
        
        # Verifica se a pasta de destino já existe e a remove
        if os.path.exists(pasta_game):
            remover_diretorio(pasta_game)
        
        # Move a nova pasta para o destino
        caminho_game_extraido = os.path.join(pasta_extraida, 'Game_teste-main', 'Game')
        if os.path.exists(caminho_game_extraido):
            shutil.move(caminho_game_extraido, pasta_game)
        
        # Remove arquivos e pastas temporárias
        remover_diretorio(pasta_extraida)
        os.remove(arquivo_zip)
        # apaga a pasta Game_teste e o arquivo zip
        Files = ['Game_teste', 'Game_teste.zip']
        for file in Files:
            if os.path.exists(file):
                os.remove(file)
                
        print('Atualização do jogo concluída com sucesso.')
    except Exception as e:
        print(f'Erro ao atualizar o jogo: {e}')

def main():
    dependencias = ['pygame']
    url_versao = "https://github.com/thiagosiega/Game_teste/raw/main/Game/V.txt"
    url_zip = "https://github.com/thiagosiega/Game_teste/archive/refs/heads/main.zip"
    arquivo_versao = "Game/V.txt"
    pasta_extraida = 'Game_teste'
    pasta_game = 'Game'
    
    if verificar_python():
        if not verificar_dependencias(dependencias):
            instalar_dependencias(dependencias)
        
        versao = verificar_versao_game(arquivo_versao, url_versao)
        if versao:
            resposta = messagebox.askyesno('Atualização', 'Nova versão disponível. Deseja atualizar?')
            if resposta:
                atualizar_game(url_zip, pasta_extraida, pasta_game)
                with open(arquivo_versao, 'w') as f:
                    f.write(versao)
                subprocess.run(['python', 'Game/Game.py'])
            else:
                subprocess.run(['python', 'Game/Game.py'])
        elif versao is None:
            subprocess.run(['python', 'Game/Game.py'])
    else:
        messagebox.showerror('Erro', 'Python não está instalado. Por favor, instale o Python.')

if __name__ == '__main__':
    main()
