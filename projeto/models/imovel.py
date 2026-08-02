from abc import ABC, abstractmethod


class Imovel(ABC):
    def __init__(self, endereco, quartos=1, vagas_garagem=0):
        self.tipo = None
        self.endereco = endereco
        self.quartos = quartos
        self.vagas_garagem = vagas_garagem

    @abstractmethod
    def calcular_valor_base(self):
        pass

    @abstractmethod
    def calcular_acrescimo_quartos(self):
        pass

    @abstractmethod
    def calcular_vagas_garagem(self):
        pass

    @abstractmethod
    def calcular_desconto(self, tem_filhos):
        pass

    def calcular_total_aluguel(self, tem_filhos):
        valor_base = self.calcular_valor_base()
        valor_acrescimo_quartos = self.calcular_acrescimo_quartos()
        valor_garagem = self.calcular_vagas_garagem()
        valor_desconto = self.calcular_desconto(tem_filhos)
        total_aluguel = valor_base + valor_acrescimo_quartos + valor_garagem - valor_desconto
        return {
            "valor_base": valor_base,
            "valor_acrescimo_quartos": valor_acrescimo_quartos,
            "valor_garagem": valor_garagem,
            "valor_desconto": valor_desconto,
            "total_aluguel": total_aluguel,
        }


class Apartamento(Imovel):
    VALOR_BASE = 700.0
    ACRESCIMO_QUARTO = 200.0
    VAGA_GARAGEM = 300.0
    DESCONTO_SEM_FILHOS = 0.05

    def __init__(self, endereco, quartos=1, vagas_garagem=0):
        super().__init__(endereco, quartos=quartos, vagas_garagem=vagas_garagem)
        self.tipo = "APARTAMENTO"

    def calcular_valor_base(self):
        return self.VALOR_BASE

    def calcular_acrescimo_quartos(self):
        if self.quartos == 2:
            return self.ACRESCIMO_QUARTO
        return 0.0

    def calcular_vagas_garagem(self):
        return self.VAGA_GARAGEM * self.vagas_garagem

    def calcular_desconto(self, tem_filhos):
        if not tem_filhos:
            total = self.calcular_valor_base() + self.calcular_acrescimo_quartos() + self.calcular_vagas_garagem()
            return round(total * self.DESCONTO_SEM_FILHOS, 2)
        return 0.0


class Casa(Imovel):
    VALOR_BASE = 900.0
    ACRESCIMO_QUARTO = 250.0
    VAGA_GARAGEM = 300.0

    def __init__(self, endereco, quartos=1, vagas_garagem=0):
        super().__init__(endereco, quartos=quartos, vagas_garagem=vagas_garagem)
        self.tipo = "CASA"

    def calcular_valor_base(self):
        return self.VALOR_BASE

    def calcular_acrescimo_quartos(self):
        if self.quartos == 2:
            return self.ACRESCIMO_QUARTO
        return 0.0

    def calcular_vagas_garagem(self):
        return self.VAGA_GARAGEM * self.vagas_garagem

    def calcular_desconto(self, tem_filhos):
        return 0.0


class Estudio(Imovel):
    VALOR_BASE = 1200.0
    VAGA_DUAS = 250.0
    VAGA_ADICIONAL = 60.0

    def __init__(self, endereco, vagas_garagem=0):
        super().__init__(endereco, quartos=0, vagas_garagem=vagas_garagem)
        self.tipo = "ESTUDIO"

    def calcular_valor_base(self):
        return self.VALOR_BASE

    def calcular_acrescimo_quartos(self):
        return 0.0

    def calcular_vagas_garagem(self):
        if self.vagas_garagem == 0:
            return 0.0
        if self.vagas_garagem <= 2:
            return self.VAGA_DUAS
        return self.VAGA_DUAS + self.VAGA_ADICIONAL * (self.vagas_garagem - 2)

    def calcular_desconto(self, tem_filhos):
        return 0.0
