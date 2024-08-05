import os
import subprocess

from tkinter import messagebox

python_instalado = False
dependencias_instaladas = False

def verificar_python():
    global python_instalado
    try:
        # Verifica se o Python está instalado usando subprocess
        subprocess.run(['python', '--version'], check=True)
        python_instalado = True
    except subprocess.CalledProcessError:
        python_instalado = False

def atualizar_python():
    try:
        subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
        messagebox.showinfo('Atualização', 'Python atualizado com sucesso')
    except subprocess.CalledProcessError:
        messagebox.showerror('Atualização', 'Erro ao atualizar Python')

def verificar_dependencias():
    global dependencias_instaladas
    dependencias = ['pip', 'pygame']
    for dependencia in dependencias:
        try:
            # Verifica se a dependência está instalada usando subprocess
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

def main():
    verificar_python()
    if python_instalado:
        #enquanto não tiver dependencias instaladas permanece no loop
        while not dependencias_instaladas:
            verificar_dependencias()
            if not dependencias_instaladas:
                instalar_dependencias()

        subprocess.run(['python', 'Game/Game.py'])
    else:
        try:
            subprocess.run(['python'], check=True)
            atualizar_python()
        except subprocess.CalledProcessError:
            messagebox.showerror('Erro', 'Python não está instalado')

if __name__ == '__main__':
    main()
