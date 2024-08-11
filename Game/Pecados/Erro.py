import tkinter as tk
import json

class Application:
    def __init__(self, master=None, texto=None):
        self.master = master
        self.master.title("Aplicação")
        self.master.geometry("300x200")
        
        self.widget1 = tk.Frame(self.master)
        self.widget1.pack()
        
        self.msg = tk.Label(self.widget1, text=texto)
        self.msg.pack()

# Função para criar novas janelas com textos do JSON
def criar_novas_janelas(num):
    # Dados do JSON
    textos = {
        "1": "Ei!",
        "2": "Ficou sabendo?",
        "3": "Temos mais um pecador!",
        "4": "Sim, é verdade!",
        "5": "Ele cometeu um erro!",
        "6": "Mas não se preocupe!",
        "7": "Ela ira se arrepender!",
        "8": "Como assim?",
        "9": "Mas.",
        "10": ".",
        "11": ".",
        "12": ".",
        "13": "E se ele...",
        "14": "E se ela...",
        "15": "E se...",
        "16": "Entendo!",
        "17": "Vamos ver o que acontece!",
        "18": "Isso é interessante!",
        "19": "Vamos Srª. Terazbqbe",
        "20": "Quem sabe Hoje isso mude!"
    }
    
    for i in range(1, num + 1):
        if str(i) in textos:
            root = tk.Tk()
            app = Application(master=root, texto=textos[str(i)])
            root.mainloop()

# Cria 10 janelas com texto do JSON
criar_novas_janelas(20)
