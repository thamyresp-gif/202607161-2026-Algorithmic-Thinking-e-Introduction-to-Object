import pytest
from models.imovel import Apartamento, Casa, Estudio


class TestApartamento:
    def test_apartamento(self):
        apt = Apartamento("Rua A, 100", quartos=2, vagas_garagem=1)
        assert apt.tipo == "APARTAMENTO"
        assert apt.endereco == "Rua A, 100"
        assert apt.quartos == 2
        assert apt.vagas_garagem == 1
        assert apt.calcular_valor_base() == 700.0
        assert apt.calcular_acrescimo_quartos() == 200.0
        assert apt.calcular_vagas_garagem() == 300.0

    def test_valor_base_apartamento(self):
        apt = Apartamento("Rua A, 100")
        resultado = apt.calcular_valor_base()
        assert resultado == 700.0

    def test_acrescimo_dois_quartos_apartamento(self):
        apt = Apartamento("Rua A, 100", quartos=2)
        resultado = apt.calcular_acrescimo_quartos()
        assert resultado == 200.0

    def test_sem_acrescimo_um_quarto_apartamento(self):
        apt = Apartamento("Rua A, 100", quartos=1)
        resultado = apt.calcular_acrescimo_quartos()
        assert resultado == 0.0

    def test_vaga_garagem_apartamento(self):
        apt = Apartamento("Rua A, 100", vagas_garagem=1)
        resultado = apt.calcular_vagas_garagem()
        assert resultado == 300.0

    def test_vaga_garagem_apartamento_multiplas(self):
        apt = Apartamento("Rua A, 100", vagas_garagem=3)
        resultado = apt.calcular_vagas_garagem()
        assert resultado == 900.0

    def test_desconto_apartamento_sem_filhos(self):
        apt = Apartamento("Rua A, 100", quartos=1, vagas_garagem=0)
        desconto = apt.calcular_desconto(tem_filhos=False)
        assert desconto == 35.0

    def test_desconto_apartamento_com_filhos(self):
        apt = Apartamento("Rua A, 100", quartos=1, vagas_garagem=0)
        desconto = apt.calcular_desconto(tem_filhos=True)
        assert desconto == 0.0

    def test_total_aluguel_apartamento_sem_filhos(self):
        apt = Apartamento("Rua A, 100", quartos=1, vagas_garagem=0)
        resultado = apt.calcular_total_aluguel(tem_filhos=False)
        assert resultado["valor_base"] == 700.0
        assert resultado["valor_acrescimo_quartos"] == 0.0
        assert resultado["valor_garagem"] == 0.0
        assert resultado["valor_desconto"] == 35.0
        assert resultado["total_aluguel"] == 665.0


class TestCasa:
    def test_valor_base_casa(self):
        casa = Casa("Rua B, 200")
        resultado = casa.calcular_valor_base()
        assert resultado == 900.0

    def test_acrescimo_dois_quartos_casa(self):
        casa = Casa("Rua B, 200", quartos=2)
        resultado = casa.calcular_acrescimo_quartos()
        assert resultado == 250.0

    def test_sem_acrescimo_um_quarto_casa(self):
        casa = Casa("Rua B, 200", quartos=1)
        resultado = casa.calcular_acrescimo_quartos()
        assert resultado == 0.0

    def test_vaga_garagem_casa(self):
        casa = Casa("Rua B, 200", vagas_garagem=1)
        resultado = casa.calcular_vagas_garagem()
        assert resultado == 300.0

    def test_vaga_garagem_casa_multiplas(self):
        casa = Casa("Rua B, 200", vagas_garagem=2)
        resultado = casa.calcular_vagas_garagem()
        assert resultado == 600.0

    def test_desconto_casa_sem_filhos(self):
        casa = Casa("Rua B, 200", quartos=1, vagas_garagem=0)
        desconto = casa.calcular_desconto(tem_filhos=False)
        assert desconto == 0.0

    def test_desconto_casa_com_filhos(self):
        casa = Casa("Rua B, 200", quartos=1, vagas_garagem=0)
        desconto = casa.calcular_desconto(tem_filhos=True)
        assert desconto == 0.0

    def test_total_aluguel_casa(self):
        casa = Casa("Rua B, 200", quartos=1, vagas_garagem=1)
        resultado = casa.calcular_total_aluguel(tem_filhos=False)
        assert resultado["valor_base"] == 900.0
        assert resultado["valor_acrescimo_quartos"] == 0.0
        assert resultado["valor_garagem"] == 300.0
        assert resultado["valor_desconto"] == 0.0
        assert resultado["total_aluguel"] == 1200.0


class TestEstudio:
    def test_valor_base_estudio(self):
        est = Estudio("Rua C, 300")
        resultado = est.calcular_valor_base()
        assert resultado == 1200.0

    def test_acrescimo_quartos_estudio(self):
        est = Estudio("Rua C, 300", vagas_garagem=0)
        resultado = est.calcular_acrescimo_quartos()
        assert resultado == 0.0

    def test_vaga_garagem_estudio_duas(self):
        est = Estudio("Rua C, 300", vagas_garagem=2)
        resultado = est.calcular_vagas_garagem()
        assert resultado == 250.0

    def test_vaga_garagem_estudio_tres(self):
        est = Estudio("Rua C, 300", vagas_garagem=3)
        resultado = est.calcular_vagas_garagem()
        assert resultado == 310.0

    def test_vaga_garagem_estudio_uma(self):
        est = Estudio("Rua C, 300", vagas_garagem=1)
        resultado = est.calcular_vagas_garagem()
        assert resultado == 250.0

    def test_desconto_estudio(self):
        est = Estudio("Rua C, 300", vagas_garagem=0)
        desconto = est.calcular_desconto(tem_filhos=False)
        assert desconto == 0.0

    def test_total_aluguel_estudio(self):
        est = Estudio("Rua C, 300", vagas_garagem=2)
        resultado = est.calcular_total_aluguel(tem_filhos=False)
        assert resultado["valor_base"] == 1200.0
        assert resultado["valor_acrescimo_quartos"] == 0.0
        assert resultado["valor_garagem"] == 250.0
        assert resultado["valor_desconto"] == 0.0
        assert resultado["total_aluguel"] == 1450.0