import locust
from locust import HttpUser, task, between


class BudgetUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8501"

    @task(3)
    def load_budget_form(self):
        self.client.get("/")

    @task(2)
    def submit_apartamento(self):
        self.client.post(
            "/",
            data={
                "tipo_imovel": "APARTAMENTO",
                "endereco": "Rua A, 100",
                "quartos": "2",
                "vagas": "1",
                "nome_locatario": "Maria",
                "tem_filhos": "on",
                "parcelar": "",
                "num_parcelas": "1",
            },
        )

    @task(2)
    def submit_casa(self):
        self.client.post(
            "/",
            data={
                "tipo_imovel": "CASA",
                "endereco": "Rua B, 200",
                "quartos": "3",
                "vagas": "2",
                "nome_locatario": "Carlos",
                "tem_filhos": "on",
                "parcelar": "",
                "num_parcelas": "1",
            },
        )

    @task(1)
    def submit_estudio(self):
        self.client.post(
            "/",
            data={
                "tipo_imovel": "ESTUDIO",
                "endereco": "Rua C, 300",
                "quartos": "1",
                "vagas": "0",
                "nome_locatario": "Ana",
                "tem_filhos": "",
                "parcelar": "",
                "num_parcelas": "1",
            },
        )

    @task(1)
    def submit_with_parcelar(self):
        self.client.post(
            "/",
            data={
                "tipo_imovel": "APARTAMENTO",
                "endereco": "Rua A, 100",
                "quartos": "2",
                "vagas": "1",
                "nome_locatario": "Joao",
                "tem_filhos": "",
                "parcelar": "on",
                "num_parcelas": "2",
            },
        )

    @task(1)
    def submit_empty_error(self):
        self.client.post(
            "/",
            data={
                "tipo_imovel": "APARTAMENTO",
                "endereco": "",
                "quartos": "1",
                "vagas": "0",
                "nome_locatario": "",
                "tem_filhos": "",
                "parcelar": "",
                "num_parcelas": "1",
            },
        )