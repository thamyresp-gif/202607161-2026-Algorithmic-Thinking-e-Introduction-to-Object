# Diagramas PlantUML

## Arquivos disponíveis

| Arquivo | Descrição | Saída |
|---------|-----------|-------|
| `diagrama_classes.puml` | Diagrama de classes UML simplificado | `diagrama_classes.png` |
| `arquitetura_classes.puml` | Diagrama de classes completo (modelagem estática) | `arquitetura_classes.png` |
| `fluxograma.puml` | Fluxograma do fluxo principal | `fluxograma.png` |
| `calculadora-orcamento.puml` | Diagrama geral do projeto na raiz | `calculadora-orcamento.png` |

## Regenerar diagramas

```bash
plantuml diagrama_classes.puml -o .
plantuml arquitetura_classes.puml -o .
plantuml fluxograma.puml -o .
```

ou diretamente da raiz do projeto:

```bash
plantuml calculadora-orcamento.puml -o .
```

## Criar novo diagrama

```bash
plantuml novo_diagrama.puml -o .
```

Isso gera `novo_diagrama.png` no mesmo diretório.