# Revisão Completa de Arquitetura — Orçamento de Aluguel R.M

**Data:** 2026-08-01
**Projeto:** Algorithmic Thinking & Introduction to Object-Oriented Programming
**Autor da Revisão:** Aria (Architect Agent)

---

## 1. Resumo Executivo

O projeto implementa um sistema de geração de orçamento de aluguel para a imobiliária R.M, utilizando Python com Streamlit como interface. A arquitetura segue o padrão **MVC em camadas** (Model-View-Controller) com camadas adicionais de serviço e persistência.

**Pontos fortes:** Uso correto de POO (herança, abstração, polimorfismo), boa cobertura de testes unitários na camada de modelos, exportação CSV funcional, diagramas de arquitetura bem elaborados.

**Problemas críticos:** Inconsistências entre a arquitetura documentada e a implementada, duplicação de código significativa, camadas mortas (database, controllers, views não utilizados), constantes duplicadas entre `config.py` e `models/orcamento.py`.

---

## 2. Estrutura do Projeto

```
projeto/
├── app.py                    # Aplicação Streamlit (monolito UI + lógica)
├── config.py                 # Constantes globais
├── requirements.txt
├── models/
│   ├── __init__.py
│   ├── imovel.py             # Imovel (ABC), Apartamento, Casa, Estudio
│   ├── locatario.py          # Locatario
│   └── orcamento.py          # Orcamento
├── controllers/
│   ├── __init__.py           # VAZIO
│   └── orcamento_controller.py  # NÃO UTILIZADO por app.py
├── services/
│   ├── __init__.py           # VAZIO
│   └── csv_service.py        # DUPLICADO em app.py
├── views/
│   ├── __init__.py           # VAZIO
│   └── console_view.py       # NÃO UTILIZADO por app.py
├── database/
│   ├── __init__.py           # VAZIO
│   ├── models.py             # OrcamentoModel — NÃO UTILIZADO
│   └── db_setup.py           # init_db() — NUNCA CHAMADO
└── tests/
    ├── test_imovel.py        # 28 testes — OK
    ├── test_orcamento.py     # 9 testes — OK
    ├── test_locatario.py     # 5 testes — OK
    ├── test_controllers.py   # VAZIO
    └── test_models.py        # VAZIO
```

---

## 3. Análise por Camada

### 3.1 Camada de Modelo (models/) — ✅ Bem Implementada

- `Imovel` (ABC) define a interface correta com métodos abstratos
- `Apartamento`, `Casa`, `Estudio` implementam herança polimórfica
- `Orcamento` orquestra cálculos com boas práticas de arredondamento
- `Locatario` é simples e correto

**Problemas encontrados:**
- `Imovel` possui atributos (`banheiros`, `metragem`, `descricao`) que nunca são utilizados nos cálculos — acoplamento desnecessário
- `Estudio.__init__` sobrescreve `quartos=0` mas o pai `Imovel` default é `quartos=1` — inconsistência sutil
- `Locatario.sem_filhos()` é redundante com o atributo `tem_filhos`
- `calcular_total_aluguel()` retorna um dict sem tipagem — frágil e propenso a erros de chave

### 3.2 Camada de Controlador (controllers/) — ❌ Morta

- `orcamento_controller.py` existe com funções `criar_imovel`, `criar_locatario`, `gerar_orcamento`, `exportar_orcamento`
- **Nunca é importado nem utilizado** por `app.py`
- `app.py` contém a mesma lógica de orquestração inline
- A controller layer é completamente redundante na prática

### 3.3 Camada de Serviço (services/) — ⚠️ Duplicada

- `csv_service.py` contém `exportar_csv()` — funcionalidade idêntica à função `exportar_csv()` em `app.py` (linhas 87-109)
- Ambas as versões geram o mesmo CSV com a mesma lógica
- `app.py` importa do `services.csv_service` na controller, mas **não usa** a função do serviço diretamente

### 3.4 Camada de Visão (views/) — ❌ Morta

- `console_view.py` existe com `exibir_resumo()` e `exibir_parcelas()`
- **Nunca é importado** por `app.py` ou qualquer outro módulo
- A aplicação usa Streamlit como UI, tornando a view de console obsoleta

### 3.5 Camada de Persistência (database/) — ❌ Morta

- `db_setup.py` com `init_db()` e `get_connection()` — **nunca chamados**
- `database/models.py` com `OrcamentoModel` — **nunca utilizado**
- O SQLite está definido mas não integrado ao fluxo de execução
- O `OrcamentoModel` espelha `Orcamento` mas sem lógica de negócio

### 3.6 Aplicação Principal (app.py) — ⚠️ Monolito

- `app.py` contém UI (Streamlit), lógica de orquestração E exportação CSV
- Viola o Princípio de Responsabilidade Única (SRP)
- A função `exportar_csv` em `app.py` é duplicata de `services/csv_service.py`
- `config.py` é importado mas **não utilizado** — constantes como `TAXA_CONTRATO`, `MAX_PARCELAS_CONTRATO` estão duplicadas em `models/orcamento.py`

---

## 4. Problemas Identificados

### 4.1 Críticos

| # | Problema | Impacto | Arquivo |
|---|----------|---------|---------|
| C1 | `exportar_csv` duplicado em `app.py` e `services/csv_service.py` | Manutenção quebrada — duas fontes de verdade | `app.py:87-109`, `services/csv_service.py:6-27` |
| C2 | Constantes duplicadas: `TAXA_CONTRATO`, `MAX_PARCELAS_CONTRATO`, `PARCELAS_ORCAMENTO` em `config.py` E `models/orcamento.py` | Risco de divergência se atualizado em apenas um lugar | `config.py`, `models/orcamento.py:5-6` |
| C3 | `controllers/orcamento_controller.py` nunca é usado | Código morto, confunde novos desenvolvedores | `controllers/orcamento_controller.py` |
| C4 | `database/` nunca é usado | Código morto, camada de persistência fantasma | `database/` inteiro |
| C5 | `views/console_view.py` nunca é usado | Código morto | `views/console_view.py` |

### 4.2 Altos

| # | Problema | Impacto | Arquivo |
|---|----------|---------|---------|
| H1 | `app.py` mistura UI, lógica de negócio e exportação | Difícil de testar, refatorar e manter | `app.py` |
| H2 | `Imovel` tem atributos não utilizados (`banheiros`, `metragem`, `descricao`) | Acoplamento desnecessário, confusão semântica | `models/imovel.py:10-12` |
| H3 | `config.py` não é importado por nenhum módulo | Código morto | `config.py` |
| H4 | `STATUS_ORCAMENTO` em `config.py` nunca é usado | Código morto | `config.py:7` |
| H5 | `OrcamentoModel` em `database/models.py` duplica `Orcamento` sem funcionalidade | Código morto, confusão de modelos | `database/models.py` |

### 4.3 Médios

| # | Problema | Impacto | Arquivo |
|---|----------|---------|---------|
| M1 | Imports relativos sem `__init__.py` re-export | Fragilidade no caminho de importação | Todos os `__init__.py` vazios |
| M2 | Sem tratamento de erros (try/except) em nenhum lugar | Falhas silenciosas ou crashes sem mensagem útil | Todos |
| M3 | `test_controllers.py` e `test_models.py` vazios | Cobertura de teste incompleta | `tests/` |
| M4 | `Estudio` hardcoda `quartos=0` no `__init__` mas o pai default é `1` | Inconsistência de inicialização | `models/imovel.py:103` |
| M5 | Sem newline final em 5 arquivos | Padrão de código inconsistente | `config.py`, `controllers/orcamento_controller.py`, `services/csv_service.py`, `database/db_setup.py`, `database/models.py` |

### 4.4 Baixos

| # | Problema | Impacto | Arquivo |
|---|----------|---------|---------|
| L1 | `Locatario.sem_filhos()` é redundante | Código desnecessário | `models/locatario.py:6-8` |
| L2 | `Imovel.tipo` é `None` até ser sobrescrito pelo subclasse | Design poderia ser mais limpo | `models/imovel.py:6` |
| L3 | `Orcamento` recalcula `calcular_total()` duas vezes em `gerar_parcelas_csv()` | Performance menor que o necessário | `models/orcamento.py:53` |

---

## 5. Aderência à Arquitetura Documentada

| Aspecto | Documentado (`MODELAGEM_DO_PROBLEMA.md`) | Implementado | Divergência |
|---------|------------------------------------------|-------------|-------------|
| Camadas | 3 (Model, View, Controller/Persistence) | 5+ (models, controllers, services, views, database) | Camadas extras não documentadas |
| Controller | Camada de controle orquestrando fluxo | Existe mas não é usado | Código morto |
| View | CLI ou HTML/CSS | Streamlit (monolito) | UI não planejada no documento |
| Persistência | Geração de CSV | CSV + SQLite (não usado) | DB camada morta |
| POO | Obrigatório | Implementado corretamente | ✅ Aderente |
| Monolito | Não mencionado | Streamlit monolito | Fora do escopo do documento |

---

## 6. Diagrama de Arquitetura Real vs. Documentada

### Arquitetura Documentada (3 camadas):
```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   View       │────▶│   Controller     │────▶│   Model         │
│ (CLI/HTML)   │     │   (Orquestra)    │     │   (Regras)      │
└─────────────┘     └──────────────────┘     └────────┬────────┘
                                                       │
                                              ┌────────▼────────┐
                                              │  Persistência   │
                                              │  (CSV export)   │
                                              └─────────────────┘
```

### Arquitetura Real (implantação):
```
┌──────────────────────────────────────────────────────────────┐
│  app.py (Streamlit) — UI + Orquestração + Exportação CSV    │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ models/      │  │ controllers/ │  │ services/        │  │
│  │ (usado ✓)    │  │ (morto ✗)    │  │ (duplicado ⚠️)   │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ views/       │  │ database/    │                         │
│  │ (morto ✗)    │  │ (morto ✗)    │                         │
│  └──────────────┘  └──────────────┘                         │
└──────────────────────────────────────────────────────────────┘
```

---

## 7. Recomendações de Correção

### Prioridade 1 — Eliminar Duplicação e Código Morto

1. **Remover `exportar_csv` de `app.py`** e usar exclusivamente `services/csv_service.py`
2. **Unificar constantes** em `config.py` e remover as duplicatas de `models/orcamento.py`
3. **Remover camadas mortas** ou integrá-las:
   - Opção A: Deletar `controllers/`, `views/`, `database/` se não são necessários
   - Opção B: Integrá-las ao fluxo real da aplicação

### Prioridade 2 — Corrigor Arquitetura

4. **Refatorar `app.py`** para separar responsabilidades:
   - Manter apenas a UI Streamlit
   - Delegar orquestração para `controllers/orcamento_controller.py`
   - Delegar exportação para `services/csv_service.py`
5. **Integrar `database/`** ao fluxo — se o SQLite é necessário, conectar `Orcamento` ao `OrcamentoModel` e chamar `init_db()` na inicialização
6. **Adicionar `__init__.py` com re-exports** para tornar os imports mais limpos

### Prioridade 3 — Melhorias de Qualidade

7. **Adicionar tipagem** (type hints) em todas as funções e métodos
8. **Adicionar tratamento de erros** com exceções customizadas
9. **Preencher `test_controllers.py`** e `test_models.py` com testes de integração
10. **Adicionar newline final** em todos os arquivos que não possuem
11. **Remover atributos não utilizados** de `Imovel` (`banheiros`, `metragem`, `descricao`) ou implementar sua utilidade
12. **Usar `dataclasses`** ou `pydantic` para `OrcamentoModel` e `Locatario`

---

## 8. Métricas de Qualidade

| Métrica | Valor | Avaliação |
|---------|-------|-----------|
| Linhas de código total | 436 | Adequado para projeto acadêmico |
| Cobertura de testes | 38 testes, 3 arquivos de teste | Boa para modelos, incompleta para controllers/serviços |
| Duplicação de código | ~30 linhas duplicadas (CSV export) | Problema moderado |
| Código morto | ~120 linhas (controllers + views + database) | Problema significativo |
| Constantes duplicadas | 3 constantes em 2 locais | Problema moderado |
| Aderência à POO | Alta (herança, abstração, polimorfismo) | ✅ Excelente |
| Aderência à arquitetura documentada | Baixa (divergências significativas) | ⚠️ Precisa de alinhamento |

---

## 9. Conclusão

O projeto demonstra **competência sólida em POO** com uso correto de herança, abstração e polimorfismo. A camada de modelos é bem estruturada e os testes unitários cobrem adequadamente as regras de negócio.

No entanto, a arquitetura apresenta **divergências significativas** entre o projeto documentado e a implementação real, com camadas inteiras de código morto e duplicação de funcionalidades. A principal recomendação é **eliminar o código morto** e **unificar as duplicações** antes de expandir o sistema.

A arquitetura monolito do Streamlit é adequada para o escopo acadêmico e o número de usuários previsto (10 simultâneos), mas a separação de responsabilidades dentro desse monolito precisa ser refinada para facilitar a manutenção e evolução futura.

— Aria, arquitetando o futuro 🏗️
