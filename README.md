# Calculadora de Orçamento de Aluguel

Projeto acadêmico — Algoritmos e Programação Orientada a Objetos (POO).

## Ferramentas instaladas

| Ferramenta | Versão | Comando |
|-----------|--------|---------|
| Java | 25.0.2 | `java -version` |
| PlantUML | 1.2025.7 | `plantuml -version` |
| Graphviz | 2.43.0 | `dot -V` |

## Estrutura do Projeto

```
├── README.md                     # Este arquivo
├── modelagem-problema.md         # Documento de modelagem do problema
├── calculadora-orcamento.puml    # Diagrama principal do projeto
├── calculadora-orcamento.png     # Renderização do diagrama principal
├── plantuml/
│   ├── README.md                 # Guia dos diagrams PlantUML
│   ├── diagrama_classes.puml     → diagrama_classes.png
│   ├── diagrama_classes.png
│   ├── arquitetura_classes.puml  → arquitetura_classes.png
│   ├── arquitetura_classes.png
│   ├── fluxograma.puml           → fluxograma.png
│   └── fluxograma.png
└── mod_dinamic/
    ├── README.md                 # Guia de modelagem dinâmica
    ├── diagrama_sequencia.puml  → diagrama_sequencia.png
    └── diagrama_sequencia.png
```

## Gerar Diagramas

Para regenerar todas as imagens:

```bash
plantuml calculadora-orcamento.puml -o .
plantuml plantuml/diagrama_classes.puml -o plantuml/
plantuml plantuml/arquitetura_classes.puml -o plantuml/
plantuml plantuml/fluxograma.puml -o plantuml/
```

## Licença

Projeto acadêmico.

