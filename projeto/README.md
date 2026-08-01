# Orçamento de Aluguel — R.M

Sistema de geração de orçamento de aluguel para a imobiliária R.M.

## Tecnologias

- **Python 3** + **Flask** (camada de controle)
- **Flask-SQLAlchemy** (persistência)
- **SQLite** (banco de dados)
- **HTML/CSS** (camada de visão)
- **Gunicorn** (servidor WSGI para produção)
- **Nginx** (reverse proxy para 10 usuários simultâneos)

## Estrutura do Projeto

```
projeto/
├── app/
│   ├── __init__.py          # Factory do Flask app
│   ├── models/
│   │   ├── __init__.py
│   │   ├── imovel.py        # Classes: Imovel, Apartamento, Casa, Estudio
│   │   ├── locatario.py     # Classe: Locatario
│   │   ├── orcamento.py     # Classe: Orcamento
│   │   ├── database.py      # SQLAlchemy instance
│   │   └── orm_models.py    # Models SQLAlchemy para o banco
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py          # Rotas Flask (controller)
│   │   └── csv_exporter.py  # Geração de CSV
│   ├── templates/
│   │   ├── index.html       # Formulário de entrada
│   │   └── resultado.html   # Página de resultado
│   └── static/
│       └── css/
│           └── style.css
├── config.py
├── requirements.txt
└── run.py
```

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
python run.py
```

Acesse: http://localhost:5000