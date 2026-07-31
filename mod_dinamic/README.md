# Modelagem Dinâmica — Diagrama de Sequência

Este diretório contém os diagramas de interação (modelagem dinâmica) da aplicação Calculadora de Orçamento de Aluguel.

## Arquivos

| Arquivo | Descrição | Saída |
|---------|-----------|-------|
| `diagrama_sequencia.puml` | Diagrama de sequência da arquitetura de camadas | `diagrama_sequencia.png` |
| `diagrama_sequencia.png` | Renderização do diagrama de sequência | — |

## Camadas Representadas

| Camada | Participante |
|--------|-------------|
| **View** | `Camada de Visão (CLI/HTML)` — interface com o usuário |
| **Control** | `Camada de Controle (Orcamento)` — orquestra o fluxo |
| **Model** | `Camada de Modelo (Imovel, Calculadoras)` — regras de negócio |
| **Persistence** | `Camada de Persistência (GeradorCSV)` — exportação de dados |

## Regenerar Diagrama

```bash
plantuml diagrama_sequencia.puml -o .
```