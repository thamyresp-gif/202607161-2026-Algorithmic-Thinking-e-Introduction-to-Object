from .imovel import Imovel
from .locatario import Locatario
from config import TAXA_CONTRATO, MAX_PARCELAS_CONTRATO, PARCELAS_ORCAMENTO


class Orcamento:
    def __init__(self, imovel, locatario, parcelar=False, num_parcelas=1):
        self.imovel = imovel
        self.locatario = locatario
        self.parcelar = parcelar
        self.num_parcelas = min(num_parcelas, MAX_PARCELAS_CONTRATO) if parcelar else 1
        self.aluguel_base = 0.0
        self.valor_acrescimos = 0.0
        self.valor_desconto = 0.0
        self.valor_garagem = 0.0
        self.taxa_contrato = TAXA_CONTRATO
        self.valor_total_mensal = 0.0
        self.parcela_contrato = 0.0
        self.status = "PENDENTE"

    def calcular_total(self):
        aluguel = self.imovel.calcular_total_aluguel(self.locatario.tem_filhos)
        self.aluguel_base = aluguel["valor_base"]
        self.valor_acrescimos = aluguel["valor_acrescimo_quartos"]
        self.valor_desconto = aluguel["valor_desconto"]
        self.valor_garagem = aluguel["valor_garagem"]

        if self.parcelar:
            self.parcela_contrato = round(self.taxa_contrato / self.num_parcelas, 2)
        else:
            self.parcela_contrato = self.taxa_contrato

        self.valor_total_mensal = round(
            aluguel["total_aluguel"] + self.parcela_contrato, 2
        )

        return {
            "aluguel_mensal": {
                "valor_base": self.aluguel_base,
                "valor_acrescimo_quartos": self.valor_acrescimos,
                "valor_garagem": self.valor_garagem,
                "valor_desconto": self.valor_desconto,
                "total_aluguel": aluguel["total_aluguel"],
            },
            "parcela_contrato": self.parcela_contrato,
            "total_mensal": self.valor_total_mensal,
        }

    def get_aluguel_liquido(self):
        aluguel = self.imovel.calcular_total_aluguel(self.locatario.tem_filhos)
        return aluguel["total_aluguel"]

    def gerar_parcelas_csv(self):
        self.calcular_total()
        aluguel_liquido = self.get_aluguel_liquido()
        parcelas = []
        for i in range(1, PARCELAS_ORCAMENTO + 1):
            parcela_contrato = 0.0
            if self.parcelar:
                if i <= self.num_parcelas:
                    parcela_contrato = self.parcela_contrato
            else:
                parcela_contrato = self.parcela_contrato
            valor_total = round(aluguel_liquido + parcela_contrato, 2)
            parcelas.append({
                "parcela": i,
                "valor_aluguel": aluguel_liquido,
                "valor_parcela_contrato": parcela_contrato,
                "valor_total": valor_total,
            })
        return parcelas