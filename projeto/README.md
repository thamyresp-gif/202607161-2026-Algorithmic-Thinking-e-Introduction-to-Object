# Orçamento de Aluguel — R.M

Sistema de geração de orçamento de aluguel para a imobiliária R.M.

## Tecnologias

- **Python 3** + **Streamlit** (monolito — frontend + backend em um único app)
- **SQLite** (banco de dados, opcional para persistência)
- **Biblioteca nativa `csv`** do Python (exportação de orçamentos)

## Estrutura do Projeto

```
projeto/
├── app.py                  # Aplicação Streamlit (monolito)
├── models/
│   ├── __init__.py
│   ├── imovel.py           # Classes: Imovel, Apartamento, Casa, Estudio
│   ├── locatario.py        # Classe: Locatario
│   └── orcamento.py        # Classe: Orcamento
├── config.py
├── requirements.txt
└── README.md
```

## Por que Streamlit?

- **Monolito no deploy** — um único arquivo Python (`app.py`) contém toda a aplicação
- **Sem templates HTML/CSS** — a interface é construída inteiramente em Python
- **Deploy simples** — `streamlit run app.py` ou deploy em Streamlit Cloud
- **Ideal para 10 usuários simultâneos** — leve e eficiente para o domínio do problema

## Requisitos Funcionais Atendidos

| RF | Descrição | Status |
|----|-----------|--------|
| 4.1 | 3 tipos de locação com valores base | Implementado |
| 4.2 | Acréscimos por quartos | Implementado |
| 4.3 | Vagas de garagem | Implementado |
| 4.4 | Desconto 5% apartamento sem filhos | Implementado |
| 4.5 | Taxa de contrato R$2000 parcelável | Implementado |
| 4.6 | Resumo total mensal | Implementado |
| 4.7 | Exportação CSV com 12 parcelas | Implementado |

## Rodando o Projeto

```bash
cd projeto
pip install -r requirements.txt
streamlit run app.py
```

Acesse: http://localhost:8501