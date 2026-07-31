# Modelagem de Dados — Diagrama Mermaid

Diagrama de modelagem de dados no formato **Mermaid** (ER Diagram), equivalente ao arquivo `dbdiagram/modelagem_dados.dbml`.

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `modelagem_dados.mmd` | Diagrama ER em sintaxe Mermaid |

## Visualização

Para renderizar o diagrama, use o [Mermaid Live Editor](https://mermaid.live):

1. Acesse [mermaid.live](https://mermaid.live)
2. Cole o conteúdo de `modelagem_dados.mmd`
3. O diagrama ER será renderizado automaticamente

Ou use a CLI:

```bash
mmdc -i mod_dados/modelagem_dados.mmd -o mod_dados/modelagem_dados.png
```

## Entidades

- **imovel** — propriedade being orçada
- **tabela_preco** — configuração de preços por tipo de imóvel
- **orcamento** — orçamento gerado para o cliente
- **parcela** — parcelas do orçamento (12 parcelas para CSV)