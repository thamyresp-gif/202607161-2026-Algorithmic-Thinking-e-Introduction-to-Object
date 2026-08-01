from models.locatario import Locatario


class TestLocatario:
    def test_locatario_com_filhos(self):
        loc = Locatario("Joao", tem_filhos=True)
        assert loc.nome == "Joao"
        assert loc.tem_filhos is True

    def test_locatario_sem_filhos(self):
        loc = Locatario("Maria", tem_filhos=False)
        assert loc.nome == "Maria"
        assert loc.tem_filhos is False

    def test_locatario_sem_filhos_default(self):
        loc = Locatario("Ana")
        assert loc.nome == "Ana"
        assert loc.tem_filhos is False

    def test_sem_filhos_retorna_true(self):
        loc = Locatario("Carlos", tem_filhos=False)
        assert loc.sem_filhos() is True

    def test_sem_filhos_retorna_false(self):
        loc = Locatario("Pedro", tem_filhos=True)
        assert loc.sem_filhos() is False