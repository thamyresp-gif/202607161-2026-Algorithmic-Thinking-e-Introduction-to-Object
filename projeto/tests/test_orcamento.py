import pytest
from models.imovel import Apartamento, Casa, Estudio
from models.locatario import Locatario
from models.orcamento import Orcamento


class TestOrcamento:
    def test_orcamento_apartamento_sem_filhos_sem_parcelar(self):
        apt = Apartamento("Rua A, 100", quartos=1, vagas_garagem=0)
        loc = Locatario("Joao", tem_filhos=False)
        orc = Orcamento(apt, loc, parcelar=False)
        resultado = orc.calcular_total()
        assert resultado["aluguel_mensal"]["valor_base"] == 700.0
        assert resultado["aluguel_mensal"]["valor_desconto"] == 35.0
        assert resultado["parcela_contrato"] == 2000.0
        assert resultado["total_mensal"] == 2665.0

    def test_orcamento_apartamento_com_filhos_sem_parcelar(self):
        apt = Apartamento("Rua A, 100", quartos=1, vagas_garagem=0)
        loc = Locatario("Joao", tem_filhos=True)
        orc = Orcamento(apt, loc, parcelar=False)
        resultado = orc.calcular_total()
        assert resultado["aluguel_mensal"]["valor_desconto"] == 0.0
        assert resultado["total_mensal"] == 2700.0

    def test_orcamento_casa_sem_parcelar(self):
        casa = Casa("Rua B, 200", quartos=1, vagas_garagem=1)
        loc = Locatario("Maria", tem_filhos=False)
        orc = Orcamento(casa, loc, parcelar=False)
        resultado = orc.calcular_total()
        assert resultado["aluguel_mensal"]["valor_base"] == 900.0
        assert resultado["aluguel_mensal"]["valor_garagem"] == 300.0
        assert resultado["total_mensal"] == 3200.0

    def test_orcamento_estudio_sem_parcelar(self):
        est = Estudio("Rua C, 300", vagas_garagem=2)
        loc = Locatario("Ana", tem_filhos=False)
        orc = Orcamento(est, loc, parcelar=False)
        resultado = orc.calcular_total()
        assert resultado["aluguel_mensal"]["valor_base"] == 1200.0
        assert resultado["aluguel_mensal"]["valor_garagem"] == 250.0
        assert resultado["total_mensal"] == 3450.0

    def test_orcamento_apartamento_parcelar_2x(self):
        apt = Apartamento("Rua A, 100", quartos=1, vagas_garagem=0)
        loc = Locatario("Joao", tem_filhos=False)
        orc = Orcamento(apt, loc, parcelar=True, num_parcelas=2)
        resultado = orc.calcular_total()
        assert resultado["parcela_contrato"] == 1000.0
        assert resultado["total_mensal"] == 1665.0

    def test_orcamento_apartamento_parcelar_5x(self):
        apt = Apartamento("Rua A, 100", quartos=1, vagas_garagem=0)
        loc = Locatario("Joao", tem_filhos=False)
        orc = Orcamento(apt, loc, parcelar=True, num_parcelas=5)
        resultado = orc.calcular_total()
        assert resultado["parcela_contrato"] == 400.0
        assert resultado["total_mensal"] == 1065.0

    def test_orcamento_max_parcelas_5(self):
        apt = Apartamento("Rua A, 100", quartos=1, vagas_garagem=0)
        loc = Locatario("Joao", tem_filhos=False)
        orc = Orcamento(apt, loc, parcelar=True, num_parcelas=10)
        resultado = orc.calcular_total()
        assert orc.num_parcelas == 5
        assert resultado["parcela_contrato"] == 400.0

    def test_gerar_parcelas_csv_12_parcelas(self):
        apt = Apartamento("Rua A, 100", quartos=1, vagas_garagem=0)
        loc = Locatario("Joao", tem_filhos=False)
        orc = Orcamento(apt, loc, parcelar=False)
        parcelas = orc.gerar_parcelas_csv()
        assert len(parcelas) == 12
        assert parcelas[0]["parcela"] == 1
        assert parcelas[11]["parcela"] == 12

    def test_gerar_parcelas_csv_valores_consistentes(self):
        apt = Apartamento("Rua A, 100", quartos=1, vagas_garagem=0)
        loc = Locatario("Joao", tem_filhos=False)
        orc = Orcamento(apt, loc, parcelar=False)
        parcelas = orc.gerar_parcelas_csv()
        total = orc.calcular_total()
        soma = sum(p["valor"] for p in parcelas)
        assert round(soma, 2) == total["total_mensal"]

    def test_orcamento_apartamento_2_quartos_com_garagem_sem_filhos(self):
        apt = Apartamento("Rua A, 100", quartos=2, vagas_garagem=1)
        loc = Locatario("Joao", tem_filhos=False)
        orc = Orcamento(apt, loc, parcelar=False)
        resultado = orc.calcular_total()
        assert resultado["aluguel_mensal"]["valor_base"] == 700.0
        assert resultado["aluguel_mensal"]["valor_acrescimo_quartos"] == 200.0
        assert resultado["aluguel_mensal"]["valor_garagem"] == 300.0
        assert resultado["aluguel_mensal"]["valor_desconto"] == 60.0
        assert resultado["total_mensal"] == 2140.0