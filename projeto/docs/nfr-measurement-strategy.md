# Estratégia de Medição de Requisitos Não Funcionais

## Projeto: Orçamento de Aluguel — R.M

## Referência: SWEBOK 4.0 / ISO/IEC 25010:2023

---

## 1. Visão Geral

Esta estratégia define os eixos de requisitos não funcionais (RNFs) a serem medidos antes da colocação em produção, os indicadores de medição, as ferramentas e os scripts automatizados.

---

## 2. Eixos de Medição (SWEBOK 4.0 — ISO/IEC 25010:2023)

### 2.1 Funcionalidade (Functional Suitability)

| Sub-característica | Indicador | Meta | Ferramenta |
|---------------------|-----------|------|------------|
| Completude | Cobertura de requisitos funcionais testados | 100% | pytest + pytest-cov |
| Corretude | Taxa de acerto nos testes unitários | ≥ 95% | pytest |
| Apropriação | Validação de cenários de negócio | Todos os cenários críticos | pytest |

**Métricas:**
- Cobertura de código por testes (linhas, ramificações, funções)
- Número de cenários de negócio cobertos
- Taxa de passagem nos testes unitários e E2E

### 2.2 Confiabilidade (Reliability)

| Sub-característica | Indicador | Meta | Ferramenta |
|---------------------|-----------|------|------------|
| Maturidade | Taxa de falhas em cenários de erro | 0 crashes | pytest |
| Disponibilidade | Tempo de resposta do app | < 2s | Playwright |
| Tolerância a falhas | Tratamento de inputs inválidos | Mensagens de erro exibidas | Playwright |
| Recuperabilidade | Recuperação após erro sem restart | Automática | Playwright |

**Métricas:**
- Tempo de resposta por fluxo (Playwright)
- Taxa de erro em inputs inválidos
- Número de crashes em testes de stress

### 2.3 Usabilidade (Usability)

| Sub-característica | Indicador | Meta | Ferramenta |
|---------------------|-----------|------|------------|
| Aprendibilidade | Tempo para conclusão do primeiro fluxo | < 30s | Playwright |
| Operabilidade | Fluxos completos sem erros | 100% | Playwright |
| Proteção contra erros | Mensagens de erro claras | Exibidas para todos os erros | Playwright |
| Estética | Elementos UI renderizados corretamente | 100% | Playwright |

**Métricas:**
- Tempo de execução de cada fluxo Playwright
- Taxa de sucesso nos fluxos E2E
- Presença de mensagens de erro nos cenários de falha

### 2.4 Eficiência de Desempenho (Performance Efficiency)

| Sub-característica | Indicador | Meta | Ferramenta |
|---------------------|-----------|------|------------|
| Comportamento temporal | Tempo de resposta do cálculo | < 500ms | pytest-benchmark |
| Utilização de recursos | Memória usada pelo cálculo | < 50MB | memory-profiler |
| Capacidade | Resposta sob carga simultânea | < 2s | Locust ou k6 |

**Métricas:**
- Tempo médio de cálculo por tipo de imóvel
- P95 e P99 de tempo de resposta
- Consumo de memória por requisição

### 2.5 Segurança (Security)

| Sub-característica | Indicador | Meta | Ferramenta |
|---------------------|-----------|------|------------|
| Confidencialidade | Dados sensíveis não expostos | Nenhum leak | bandit |
| Integridade | CSV gerado consistente | Sem corrupção | Script customizado |
| Autenticidade | Inputs sanitizados | Sem injection | bandit + custom |

**Métricas:**
- Número de vulnerabilidades encontradas (bandit)
- Integridade do CSV gerado (checksum)
- Sanitização de inputs (testes de injection)

### 2.6 Manutenibilidade (Maintainability)

| Sub-característica | Indicador | Meta | Ferramenta |
|---------------------|-----------|------|------------|
| Modularidade | Acoplamento entre módulos | Baixo | radon (CC) |
| Reutilização | Duplicação de código | < 5% | radon (DUPLIC) |
| Analisabilidade | Complexidade ciclomática | < 10 por função | radon (CC) |
| Modificabilidade | Linhas alteradas por mudança | < 50 | git diff |
| Testabilidade | Cobertura de testes | ≥ 80% | pytest-cov |

**Métricas:**
- Complexidade ciclomática por função (radon cc)
- Duplicação de código (radon raw)
- Cobertura de testes (pytest-cov)
- Métricas LOC por módulo

### 2.7 Portabilidade (Portability)

| Sub-característica | Indicador | Meta | Ferramenta |
|---------------------|-----------|------|------------|
| Adaptabilidade | Funciona em diferentes SO | Linux/Windows/Mac | CI matrix |
| Instalabilidade | Instalação sem erros | 100% | pip install -r requirements.txt |
| Substituibilidade | Componentes substituíveis | Sem dependência rígida | Análise de imports |

**Métricas:**
- Taxa de sucesso de instalação em diferentes ambientes
- Número de dependências fixas vs flexíveis

### 2.8 Compatibilidade (Compatibility)

| Sub-característica | Indicador | Meta | Ferramenta |
|---------------------|-----------|------|------------|
| Coexistência | Não conflita com outras apps | Nenhum conflito | Teste manual |
| Interoperabilidade | CSV aberto em Excel/LibreOffice | Sem erros | Validação de formato |

**Métricas:**
- Validação de formato CSV (delimiter, encoding, headers)
- Teste de abertura em diferentes leitores CSV

---

## 3. Scripts de Medição Automatizada

### 3.1 `scripts/measure_nfrs.py`
Script principal que executa todas as medições e gera um relatório consolidado.

### 3.2 `projeto/tests/test_nfr_performance.py`
Testes de desempenho com pytest-benchmark.

### 3.3 `projeto/tests/test_nfr_security.py`
Testes de segurança com bandit e validação de inputs.

### 3.4 `projeto/tests/test_nfr_maintainability.py`
Testes de manutenibilidade com métricas de complexidade e cobertura.

---

## 4. Matriz de Execução

| Eixo | Script | Frequência | Gate |
|------|--------|-----------|------|
| Funcionalidade | `pytest --cov` | A cada commit | ≥ 95% cobertura |
| Confiabilidade | `pytest test_playwright_flows.py` | A cada release | 100% pass |
| Usabilidade | `pytest test_playwright_flows.py` | A cada release | 100% pass |
| Desempenho | `pytest test_nfr_performance.py` | Semanal | < 500ms P95 |
| Segurança | `bandit -r projeto/` | A cada commit | 0 high severity |
| Manutenibilidade | `scripts/measure_nfrs.py` | Semanal | < 10 CC, < 5% dup |
| Portabilidade | `pip install -r requirements.txt` | A cada release | 100% success |
| Compatibilidade | Validação CSV manual | A cada release | Sem erros |

---

## 5. Critérios de Aceitação para Produção

- [ ] Todos os testes unitários passam (37/37)
- [ ] Todos os testes Playwright passam (9/9)
- [ ] Cobertura de código ≥ 80%
- [ ] Complexidade ciclomática máxima < 10
- [ ] Zero vulnerabilidades de alta severidade (bandit)
- [ ] Tempo de resposta P95 < 500ms
- [ ] CSV gerado válido e interoperável
- [ ] App instala e roda sem erros
- [ ] Código morto eliminado ou justificado