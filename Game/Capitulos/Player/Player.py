class player:
    def __init__(self, nome, vida, mana, Capitulo, Tex_vex):
        self.nome = nome
        self.vida = vida
        self.mana = mana
        self.Capitulo = Capitulo
        self.Tex_vex = Tex_vex

    def salvar(self):
        return {
            "nome": self.nome,
            "vida": self.vida,
            "mana": self.mana,
            "Itens": [],  # ou adicione a lista de itens, se necessário
            "Capitulo": self.Capitulo,
            "Tex_vex": self.Tex_vex
        }
