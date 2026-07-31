# Modelagem de Dados — Calculadora de Orçamento de Aluguel

## Visão Geral

Este documento descreve o modelo de dados do projeto em formato **DB Diagram** (DBML). O modelo define as entidades, atributos e relacionamentos necessários para armazenar e gerenciar os orçamentos de aluguel da imobiliária R.M.

## Entidades

### `imovel`

Representa o imóvel (propriedade) que será orçado.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | int (PK) | Identificador único |
| `tipo` | tipo_imovel | APARTAMENTO, CASA ou ESTUDIO |
| `quartos` | int | Número de quartos |
| `vagas_garagem` | int | Número de vagas de garagem |

### `tabela_preco`

Configuração de preços e regras por tipo de imóvel. Permite que as regras de cálculo sejam gerenciadas como dados.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | int (PK) | Identificador único |
| `tipo` | tipo_imovel | Tipo de imóvel |
| `quartos` | int | Número de quartos vinculado à regra |
| `valor_base` | decimal(10,2) | Valor base do aluguel |
| `alcrescimo_dois_quartos` | decimal(10,2) | Acréscimo para 2 quartos |
| `desconto_sem_filhos` | decimal(3,2) | Percentual de desconto (ex: 0,05 = 5%) |
| `garagem_valor_fixo` | decimal(10,2) | Valor fixo de garagem |
| `garagem_valor_extra` | decimal(10,2) | Valor por vaga extra |
| `taxas_contrato` | decimal(10,2) | Taxa fixa de contrato (R$ 2.000) |

### `orcamento`

O orçamento gerado para um cliente. Agrega todas as informações do cálculo.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | int (PK) | Identificador único |
| `imovel_id` | int (FK) | Referência ao imóvel |
| `tabela_preco_id` | int (FK) | Referência à tabela de preços aplicada |
| `tem_filhos` | boolean | Indica se o locatário tem filhos |
| `parcelar` | boolean | Se o contrato será parcelado |
| `num_parcelas` | int | Quantidade de parcelas (máx. 5) |
| `aluguel_base` | decimal(10,2) | Valor base do aluguel |
| `valor_acrescimos` | decimal(10,2) | Total de acréscimos |
| `valor_desconto` | decimal(10,2) | Total de descontos |
| `valor_garagem` | decimal(10,2) | Custo de garagem |
| `taxa_contrato` | decimal(10,2) | Taxa de contrato |
| `valor_total_mensal` | decimal(10,2) | Total mensal (aluguel + acréscimos - descontos + garagem + parcela contrato) |
| `parcela_contrato` | decimal(10,2) | Valor da parcela do contrato |
| `status` | status_parcelamento | A_VISTA ou PARCELADO |
| `criado_em` | timestamp | Data de criação do orçamento |

### `parcela`

Representa cada uma das 12 parcelas do orçamento (exportação CSV).

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
orcamento 1 ── ∞ parcela
```

## Regras de Cálculo Resumidas

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

Ou use a CLI:

```bash
npx dbml-to-png dbdiagram/modelagem_dados.dbml -o dbdiagram/modelagem_dados.png
```