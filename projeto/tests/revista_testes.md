# Revisão de Testes — Fase Red do TDD

**Revisado por:** Dex (@dev)
**Data:** 2026-08-01
**Fase:** TDD Red — testes escritos, implementação pendente

---

## 1. Visão Geral

| Métrica | Valor |
|---------|-------|
| Total de testes | 38 |
| Arquivos de teste | 5 (`test_imovel.py`, `test_orcamento.py`, `test_locatario.py`, `test_controllers.py`, `test_models.py`) |
| Testes passing | 38 |
| Arquivos vazios | 2 (`test_controllers.py`, `test_models.py`) |
| Cobertura de arquivos fonte | 4/10 (models apenas) |

---

## 2. Problemas Identificados

### 2.1 Críticos

| # | Problema | Impacto | Arquivo |
|---|----------|---------|---------|
| C1 | `test_controllers.py` está vazio | A camada de controle não tem nenhuma validação | `tests/test_controllers.py` |
| C2 | `test_models.py` está vazio | Os modelos do banco (`OrcamentoModel`, `get_connection`, `init_db`) não são testados | `tests/test_models.py` |
| C3 | Nenhum teste para `services/csv_service.py` | A exportação CSV não é validada por testes | `tests/` ausente |
| C4 | Nenhum teste para `views/console_view.py` | A view de console não é validada | `tests/` ausente |
| C5 | Nenhum teste para `config.py` | Constantes globais não são verificadas | `tests/` ausente |
| C6 | Nenhum teste para `database/db_setup.py` | Inicialização do DB não é testada | `tests/` ausente |

### 2.2 Altos

| # | Problema | Impacto | Arquivo |
|---|----------|---------|---------|
| H1 | Sem testes de edge case (valores zero, negativos, limites) | Falha em capturar bugs de entrada inválida | `test_imovel.py`, `test_orcamento.py` |
| H2 | Sem teste para `Imovel` como classe abstrata (não instanciável) | Não valida que a ABC funciona corretamente | `test_imovel.py` |
| H3 | Sem teste para `Locatario` com nome vazio | Entrada inválida não é capturada | `test_locatario.py` |
| H4 | `Orcamento` com `num_parcelas=0` não é testado | Comportamento indefinido para valor inválido | `test_orcamento.py` |
| H5 | `Orcamento` com `num_parcelas=-1` não é testado | Comportamento indefinido para valor negativo | `test_orcamento.py` |
| H6 | Sem teste para `Orcamento.status` | O campo status é definido mas nunca testado | `test_orcamento.py` |
| H7 | Sem teste para `Imovel.banheiros` e `Imovel.metragem` | Atributos definidos mas nunca utilizados nos cálculos — não testados | `test_imovel.py` |

### 2.3 Médios

| # | Problema | Impacto | Arquivo |
|---|----------|---------|---------|
| M1 | `test_orcamento.py` re-instancia os mesmos objetos repetidamente | Duplicação de setup entre testes | `test_orcamento.py` |
| M2 | Falta `conftest.py` com fixtures reutilizáveis | Violação DRY nos testes | `tests/` ausente |
| M3 | Sem `__init__.py` nos tests (não necessário mas pode ser melhorado) | Consistência com o resto do projeto | `tests/` |
| M4 | `test_imovel.py` não testa `Imovel` base diretamente | A classe abstrata não tem cobertura | `test_imovel.py` |
| M5 | `test_locatario.py` não testa `Locatario` com nome vazio ou especial | Validação de entrada ausente | `test_locatario.py` |
| M6 | `test_orcamento.py::test_gerar_parcelas_csv_valores_consistentes` chama `calcular_total()` duas vezes | Redundância — `gerar_parcelas_csv()` já chama `calcular_total()` internamente | `test_orcamento.py:82` |

### 2.4 Baixos

| # | Problema | Impacto | Arquivo |
|---|----------|---------|---------|
| L1 | Falta testar `Orcamento` com `parcelar=True` e `num_parcelas=1` (borda do parcelamento) | Cobertura incompleta do parcelamento | `test_orcamento.py` |
| L2 | Falta testar `Apartamento` com `quartos=3` ou mais | Apenas 1 e 2 quartos são testados | `test_imovel.py` |
| L3 | Falta testar `Casa` com `quartos=3` ou mais | Apenas 1 e 2 quartos são testados | `test_imovel.py` |
| L4 | Falta testar `Estudio` com `vagas_garagem=0` | Borda não testada | `test_imovel.py` |
| L5 | Falta testar `Estudio` com `vagas_garagem=4+` | Apenas 1, 2 e 3 vagas são testadas | `test_imovel.py` |

---

## 3. Análise TDD Red-Phase

### 3.1 O que está correto na fase red

- Os testes estão escritos e **passam** (green) — isso significa que a implementação já existe
- Para estar na fase red, os testes devem ter sido escritos ANTES da implementação
- A estrutura dos testes é limpa: classes por componente, métodos descritivos

### 3.2 O que precisa ser verificado para a fase red

1. **Os testes foram escritos antes da implementação?** — Verificar git blame/history
2. **Os testes falham sem a implementação?** — Remover temporariamente os modelos e rodar `pytest`
3. **Os testes cobrem todos os requisitos funcionais?** — Mapear RF → testes

### 3.3 Mapeamento RF → Testes

| RF | Teste Existente | Status |
|----|----------------|--------|
| 4.1 — 3 tipos de locação | `test_valor_base_apartamento`, `test_valor_base_casa`, `test_valor_base_estudio` | ✅ Coberto |
| 4.2 — Acréscimos por quartos | `test_acrescimo_dois_quartos_apartamento`, `test_acrescimo_dois_quartos_casa`, `test_sem_acrescimo_um_quarto_*` | ✅ Coberto |
| 4.3 — Vagas de garagem | `test_vaga_garagem_*` (todos os tipos) | ✅ Coberto |
| 4.4 — Desconto 5% apartamento sem filhos | `test_desconto_apartamento_sem_filhos`, `test_desconto_apartamento_com_filhos` | ✅ Coberto |
| 4.5 — Taxa de contrato R$2000 parcelável | `test_orcamento_apartamento_sem_filhos_sem_parcelar`, `test_orcamento_apartamento_parcelar_2x`, `test_orcamento_apartamento_parcelar_5x`, `test_orcamento_max_parcelas_5` | ✅ Coberto |
| 4.6 — Resumo total mensal | `test_total_aluguel_*`, `test_orcamento_*` | ✅ Coberto |
| 4.7 — Exportação CSV 12 parcelas | `test_gerar_parcelas_csv_12_parcelas`, `test_gerar_parcelas_csv_valores_consistentes` | ✅ Coberto |

**Todos os RFs estão cobertos por testes.** ✅

---

## 4. Recomendações

### Prioridade 1 — Completar arquivos vazios

1. **Preencher `test_controllers.py`** com testes para:
   - `criar_imovel()` com cada tipo válido
   - `criar_imovel()` com tipo inválido (deve levantar `ValueError`)
   - `criar_locatario()` com e sem filhos
   - `gerar_orcamento()` com cada tipo de imóvel
   - `exportar_orcamento()` gera arquivo no diretório correto

2. **Preencher `test_models.py`** com testes para:
   - `OrcamentoModel` inicialização com todos os campos
   - `OrcamentoModel` com `status` em cada valor de `STATUS_ORCAMENTO`
   - `get_connection()` retorna conexão com `row_factory`
   - `init_db()` cria tabela sem erros

### Prioridade 2 — Adicionar testes de edge case

3. Adicionar testes para valores limítrofes:
   - `Orcamento` com `num_parcelas=0` (deve ser tratado)
   - `Orcamento` com `num_parcelas=-1` (deve ser tratado)
   - `Imovel` com `quartos=0` (Estudio) e `quartos=10` (máximo do input)
   - `Locatario` com nome vazio

4. Adicionar teste para `Imovel` como classe abstrata:
   ```python
   def test_imovel_abstrato_nao_instanciavel(self):
       with pytest.raises(TypeError):
           Imovel("Rua X")
   ```

### Prioridade 3 — Melhorar infraestrutura de testes

5. Criar `tests/conftest.py` com fixtures reutilizáveis:
   ```python
   @pytest.fixture
   def apartamento_padrao():
       return Apartamento("Rua A, 100", quartos=1, vagas_garagem=0)
   
   @pytest.fixture
   def locatario_padrao():
       return Locatario("Joao", tem_filhos=False)
   ```

6. Adicionar `conftest.py` com `pytest.ini` ou `pyproject.toml` para configurar o pytest

7. Remover a chamada duplicada a `calcular_total()` em `test_gerar_parcelas_csv_valores_consistentes`

---

## 5. Veredicto

| Aspecto | Avaliação |
|---------|-----------|
| Estrutura dos testes | ✅ Boa — classes organizadas, nomes descritivos |
| Cobertura dos requisitos funcionais | ✅ Todos os RFs cobertos |
| Cobertura de edge cases | ⚠️ Insuficiente — faltam limites e entradas inválidas |
| Arquivos de teste vazios | ❌ 2 de 5 arquivos estão vazios |
| Infraestrutura de testes | ⚠️ Sem fixtures, sem conftest.py |
| Fase Red TDD | ⚠️ Testes passam (green), mas a implementação já existe — verificar se os testes foram escritos antes |

**Ação imediata:** Preencher `test_controllers.py` e `test_models.py`, adicionar fixtures, e adicionar testes de edge case antes de avançar para a fase green do TDD.

— Dex, sempre construindo 🔨
