class Locatario:
    def __init__(self, nome, tem_filhos=False):
        self.nome = nome
        self.tem_filhos = tem_filhos

    def sem_filhos(self):
        return not self.tem_filhos