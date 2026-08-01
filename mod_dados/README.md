# Modelagem de Dados — Orçamento de Aluguel R.M

## Visão Geral

Modelo de dados do projeto em formato **DB Diagram** (DBML). Define as entidades, atributos e relacionamentos para armazenar e gerenciar os orçamentos de aluguel da imobiliária R.M.

## Entidades

### `imovel`

Representa o imóvel cadastrado na imobiliária.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | int (PK) | Identificador único |
| `tipo` | tipo_imovel | APARTAMENTO, CASA ou ESTUDIO |
| `endereco` | varchar(255) | Endereço completo do imóvel |
| `quartos` | int | Número de quartos |
| `banheiros` | int | Número de banheiros |
| `metragem` | decimal(10,2) | Metragem em m² |
| `vagas_garagem` | int | Número de vagas de garagem |
| `descricao` | text | Descrição do imóvel |

### `locatario`

Pessoa ou entity que loca o imóvel.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | int (PK) | Identificador único |
| `nome` | varchar(255) | Nome do locatário |
| `email` | varchar(255) | E-mail de contato |
| `telefone` | varchar(20) | Telefone de contato |
| `tem_filhos` | boolean | Indica se possui filhos (aciona desconto) |

### `corretor`

Corretor responsável pela negociação.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | int (PK) | Identificador único |
| `nome` | varchar(255) | Nome do corretor |
| `creci` | varchar(20) | Número do CRECI |
| `email` | varchar(255) | E-mail de contato |
| `telefone` | varchar(20) | Telefone de contato |

### `orcamento`

O orçamento gerado para um cliente. Agrega todas as informações do cálculo.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | int (PK) | Identificador único |
| `imovel_id` | int (FK) | Referência ao imóvel |
| `locatario_id` | int (FK) | Referência ao locatário |
| `corretor_id` | int (FK) | Referência ao corretor |
| `parcelar` | boolean | Contrato será parcelado |
| `num_parcelas_contrato` | int | Quantidade de parcelas (máx. 5) |
| `aluguel_base` | decimal(10,2) | Valor base do aluguel |
| `valor_acrescimos` | decimal(10,2) | Total de acréscimos |
| `valor_desconto` | decimal(10,2) | Total de descontos |
| `valor_garagem` | decimal(10,2) | Custo de garagem |
| `taxa_contrato` | decimal(10,2) | Taxa de contrato (R$ 2.000) |
| `valor_total_mensal` | decimal(10,2) | Total mensal |
| `parcela_contrato` | decimal(10,2) | Valor da parcela do contrato |
| `status` | status_orcamento | PENDENTE, APROVADO, REJEITADO, CONCLUIDO |
| `criado_em` | timestamp | Data de criação |

### `parcela`

As 12 parcelas do orçamento para exportação CSV.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | int (PK) | Identificador único |
| `orcamento_id` | int (FK) | Referência ao orçamento |
| `numero` | int | Número da parcela (1 a 12) |
| `valor` | decimal(10,2) | Valor da parcela |

## Enums

### `tipo_imovel`
- `APARTAMENTO`
- `CASA`
- `ESTUDIO`

### `status_orcamento`
- `PENDENTE`
- `APROVADO`
- `REJEITADO`
- `CONCLUIDO`

### `status_parcelamento`
- `A_VISTA`
- `PARCELADO`

## Relacionamentos

```
imovel 1 ── ∞ orcamento
locatario 1 ── ∞ orcamento
corretor 1 ── ∞ orcamento
orcamento 1 ── ∞ parcela
```

## Regras de Cálculo

| Regra | Condição | Valor |
|-------|----------|-------|
| Aluguel base — Apartamento | qualquer | R$ 700,00 |
| Aluguel base — Casa | qualquer | R$ 900,00 |
| Aluguel base — Estúdio | qualquer | R$ 1.200,00 |
| Acrescimo 2 quartos — Apartamento | quartos == 2 | +R$ 200,00 |
| Acrescimo 2 quartos — Casa | quartos == 2 | +R$ 250,00 |
| Garagem — Casa/Apartamento | vagas > 0 | +R$ 300,00/vaga |
| Garagem — Estúdio | vagas == 2 | +R$ 250,00 total |
| Garagem — Estúdio | vagas > 2 | +R$ 250,00 + R$ 60,00/vaga extra |
| Desconto — Apartamento sem filhos | tipo == APARTAMENTO AND filhos == false | -5% |
| Taxa de contrato | fixo | R$ 2.000,00 |
| Parcelamento | parcelar == true | Até 5x |

## Geração do Diagrama

Para renderizar este modelo como imagem, use o [DB Diagram](https://dbdiagram.io):

1. Acesse [dbdiagram.io](https://dbdiagram.io)
2. Cole o conteúdo de `modelagem_dados.dbml`
3. O diagrama será renderizado automaticamente