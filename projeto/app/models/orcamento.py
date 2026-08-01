from .imovel import Imovel
from .locatario import Locatario


TAXA_CONTRATO = 2000.0
MAX_PARCELAS_CONTRATO = 5
PARCELAS_ORCAMENTO = 12


class Orcamento:
    def __init__(self, imovel: Imovel, locatario: Locatario, parcelar=False, num_parcelas=1):
        self.imovel = imovel
        self.locatario = locatario
        self.parcelar = parcelar
        self.num_parcelas = min(num_parcelas, MAX_PARCELAS_CONTRATO) if parcelar else 1
        self._resultado_aluguel = None
        self._parcela_contrato = None
        self._total = None

    def calcular_aluguel(self):
        self._resultado_aluguel = self.imovel.calcular_total_aluguel(
            tem_filhos=self.locatario.tem_filhos
        )
        return self._resultado_aluguel

    def calcular_parcela_contrato(self):
        if self.parcelar and self.num_parcelas > 0:
            self._parcela_contrato = round(TAXA_CONTRATO / self.num_parcelas, 2)
        else:
            self._parcela_contrato = TAXA_CONTRATO
        return self._parcela_contrato

    def calcular_total(self):
        aluguel = self.calcular_aluguel()
        parcela = self.calcular_parcela_contrato()
        self._total = round(aluguel["total_aluguel"] + parcela, 2)
        return {
            "aluguel_mensal": aluguel,
            "parcela_contrato": parcela,
            "total_mensal": self._total,
            "parcelar": self.parcelar,
            "num_parcelas": self.num_parcelas,
        }

    def gerar_parcelas_csv(self):
        total = self.calcular_total()
        parcela_mensal = round(total["total_mensal"] / PARCELAS_ORCAMENTO, 2)
        parcelas = []
        for i in range(1, PARCELAS_ORCAMENTO + 1):
            valor = parcela_mensal
            if i == PARCELAS_ORCAMENTO:
                valor = round(total["total_mensal"] - parcela_mensal * (PARCELAS_ORCAMENTO - 1), 2)
            parcelas.append({"parcela": i, "valor": valor})
        return parcelas