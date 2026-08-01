from abc import ABC, abstractmethod


class Imovel(ABC):
    def __init__(self, tipo, endereco, quartos, vagas_garagem):
        self.tipo = tipo
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

    def calcular_total_aluguel(self, tem_filhos=False):
        base = self.calcular_valor_base()
        acrescimo = self.calcular_acrescimo_quartos()
        garagem = self.calcular_vagas_garagem()
        desconto = self.calcular_desconto(tem_filhos)
        total = base + acrescimo + garagem - desconto
        return {
            "valor_base": base,
            "valor_acrescimo_quartos": acrescimo,
            "valor_garagem": garagem,
            "valor_desconto": desconto,
            "total_aluguel": round(total, 2),
        }


class Apartamento(Imovel):
    VALOR_BASE = 700.0
    ACRESCIMO_DOIS_QUARTOS = 200.0
    VAGA_GARAGEM = 300.0
    DESCONTO_SEM_FILHOS = 0.05

    def __init__(self, endereco, quartos=1, vagas_garagem=0):
        super().__init__("APARTAMENTO", endereco, quartos, vagas_garagem)

    def calcular_valor_base(self):
        return self.VALOR_BASE

    def calcular_acrescimo_quartos(self):
        if self.quartos == 2:
            return self.ACRESCIMO_DOIS_QUARTOS
        return 0.0

    def calcular_vagas_garagem(self):
        return self.vagas_garagem * self.VAGA_GARAGEM

    def calcular_desconto(self, tem_filhos):
        if not tem_filhos:
            base = self.calcular_valor_base()
            acrescimo = self.calcular_acrescimo_quartos()
            garagem = self.calcular_vagas_garagem()
            subtotal = base + acrescimo + garagem
            return round(subtotal * self.DESCONTO_SEM_FILHOS, 2)
        return 0.0


class Casa(Imovel):
    VALOR_BASE = 900.0
    ACRESCIMO_DOIS_QUARTOS = 250.0
    VAGA_GARAGEM = 300.0

    def __init__(self, endereco, quartos=1, vagas_garagem=0):
        super().__init__("CASA", endereco, quartos, vagas_garagem)

    def calcular_valor_base(self):
        return self.VALOR_BASE

    def calcular_acrescimo_quartos(self):
        if self.quartos == 2:
            return self.ACRESCIMO_DOIS_QUARTOS
        return 0.0

    def calcular_vagas_garagem(self):
        return self.vagas_garagem * self.VAGA_GARAGEM

    def calcular_desconto(self, tem_filhos):
        return 0.0


class Estudio(Imovel):
    VALOR_BASE = 1200.0
    VAGA_DUAS = 250.0
    VAGA_ADICIONAL = 60.0

    def __init__(self, endereco, vagas_garagem=0):
        super().__init__("ESTUDIO", endereco, 0, vagas_garagem)

    def calcular_valor_base(self):
        return self.VALOR_BASE

    def calcular_acrescimo_quartos(self):
        return 0.0

    def calcular_vagas_garagem(self):
        if self.vagas_garagem <= 2:
            return self.VAGA_DUAS
        return self.VAGA_DUAS + (self.vagas_garagem - 2) * self.VAGA_ADICIONAL

    def calcular_desconto(self, tem_filhos):
        return 0.0