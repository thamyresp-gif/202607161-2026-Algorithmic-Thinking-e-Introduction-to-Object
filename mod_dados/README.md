# Modelagem de Dados — Orçamento de Aluguel R.M

## Visão Geral

Modelo de dados do projeto em formato **DB Diagram** (DBML). Define as entidades, atributos e relacionamentos para armazenar e gerenciar os orçamentos de aluguel da imobiliária R.M.

## Entidades

### `imovel`

Representa o imóvel que será orçado.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | int (PK) | Identificador único |
| `tipo` | tipo_imovel | APARTAMENTO, CASA ou ESTUDIO |
| `endereco` | varchar(255) | Endereço do imóvel |
| `quartos` | int | Número de quartos |
| `vagas_garagem` | int | Número de vagas de garagem |

### `tabela_preco`

Configuração de preços e regras por tipo de imóvel.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | int (PK) | Identificador único |
| `tipo` | tipo_imovel | Tipo de imóvel |
| `valor_base` | decimal(10,2) | Valor base do aluguel |
| `alcrescimo_dois_quartos` | decimal(10,2) | Acréscimo para 2 quartos |
| `desconto_sem_filhos` | decimal(3,2) | Percentual de desconto |
| `garagem_valor_fixo` | decimal(10,2) | Valor fixo de garagem |
| `garagem_valor_extra` | decimal(10,2) | Valor por vaga extra |
| `taxa_contrato` | decimal(10,2) | Taxa fixa de contrato (R$ 2.000) |

### `orcamento`

O orçamento gerado para um cliente.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | int (PK) | Identificador único |
| `imovel_id` | int (FK) | Referência ao imóvel |
| `tabela_preco_id` | int (FK) | Referência à tabela de preços |
| `tem_filhos` | boolean | Locatário tem filhos |
| `parcelar` | boolean | Contrato parcelado |
| `num_parcelas_contrato` | int | Quantidade de parcelas (máx. 5) |
| `aluguel_base` | decimal(10,2) | Valor base do aluguel |
| `valor_acrescimos` | decimal(10,2) | Total de acréscimos |
| `valor_desconto` | decimal(10,2) | Total de descontos |
| `valor_garagem` | decimal(10,2) | Custo de garagem |
| `taxa_contrato` | decimal(10,2) | Taxa de contrato |
| `valor_total_mensal` | decimal(10,2) | Total mensal |
| `parcela_contrato` | decimal(10,2) | Valor da parcela do contrato |
| `status` | status_parcelamento | A_VISTA ou PARCELADO |
| `criado_em` | timestamp | Data de criação |

### `parcela_orcamento`

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

### `status_parcelamento`
- `A_VISTA`
- `PARCELADO`

## Relacionamentos

```
imovel 1 ── ∞ orcamento
tabela_preco 1 ── ∞ orcamento
orcamento 1 ── ∞ parcela_orcamento
```