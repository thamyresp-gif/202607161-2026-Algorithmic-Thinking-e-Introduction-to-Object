# Plano de Adequação — Requisitos Não Funcionais (SWEBOK 4.0)

## Projeto: Orçamento de Aluguel R.M

## Referência: ISO/IEC 25010:2023 / SWEBOK 4.0

---

## 1. Matriz de Testes por Eixo de Qualidade

### 1.1 Funcionalidade (Functional Suitability)

| ID | Teste | Tipo | Ferramenta | Critério de Aceite |
|----|-------|------|------------|-------------------|
| F-01 | Cobertura de código ≥ 80% | Estático | `pytest-cov` | `pytest --cov=. --cov-report=term-missing` |
| F-02 | 37 testes unitários passam | Unitário | `pytest` | `pytest tests/ --ignore=test_playwright_flows.py` |
| F-03 | 9 fluxos E2E passam | E2E | `playwright` | `pytest tests/test_playwright_flows.py` |
| F-04 | Cenários de negócio cobertos | Cenário | Manual + Playwright | Todos os fluxos do MODELAGEM_DO_PROBLEMA.md |
| F-05 | Corretude dos cálculos | Unitário | `pytest` | Valores conhecidos para cada tipo de imóvel |

### 1.2 Confiabilidade (Reliability)

| ID | Teste | Tipo | Ferramenta | Critério de Aceite |
|----|-------|------|------------|-------------------|
| R-01 | Tempo de resposta P95 < 500ms | Performance | `pytest-benchmark` | Média de 1000 iterações |
| R-02 | Memória P95 < 50MB | Recursos | `tracemalloc` | Medido durante cálculo |
| R-03 | Tolerância a inputs inválidos | Unitário | `pytest` | Mensagem de erro exibida, sem crash |
| R-04 | Recuperação após erro | E2E | Playwright | App continua funcional após erro |
| R-05 | Disponibilidade do app | Health Check | `curl` | HTTP 200 em `/health` |

### 1.3 Usabilidade (Usability)

| ID | Teste | Tipo | Ferramenta | Critério de Aceite |
|----|-------|------|------------|-------------------|
| U-01 | Fluxos completos sem erro | E2E | Playwright | 9/9 testes passam |
| U-02 | Tempo de conclusão de fluxo | Performance | Playwright | < 30s por fluxo |
| U-03 | Mensagens de erro claras | E2E | Playwright | Erros visíveis e compreensíveis |
| U-04 | Elementos UI renderizados | E2E | Playwright | Todos os campos visíveis |
| U-05 | Aprendibilidade | Manual | Teste com usuário | Tempo para primeiro uso < 5 min |

### 1.4 Eficiência de Desempenho (Performance Efficiency)

| ID | Teste | Tipo | Ferramenta | Critério de Aceite |
|----|-------|------|------------|-------------------|
| P-01 | Tempo de cálculo por tipo | Benchmark | `pytest-benchmark` | < 10ms por cálculo |
| P-02 | Tempo de exportação CSV | Benchmark | `pytest-benchmark` | < 100ms por export |
| P-03 | Teste de carga (10 usuários simultâneos) | Carga | `locust` | < 2s de tempo de resposta |
| P-04 | Teste de estresse (50 usuários) | Estresse | `locust` | Sem crashes, recuperação automática |
| P-05 | Uso de memória sob carga | Recursos | `psutil` | < 100MB em pico |
| P-06 | Throughput de requisições | Carga | `locust` | > 10 req/s |

### 1.5 Segurança (Security)

| ID | Teste | Tipo | Ferramenta | Critério de Aceite |
|----|-------|------|------------|-------------------|
| S-01 | Zero vulnerabilidades HIGH | Análise estática | `bandit` | `bandit -r models/ services/ app.py config.py` |
| S-02 | Sanitização de inputs | Unitário | `pytest` | Inputs maliciosos não causam crash |
| S-03 | Integridade do CSV | Unitário | `pytest` | CSV gerado sem corrupção |
| S-04 | Formato CSV interoperável | Unitário | `pytest` | Abre em Excel/LibreOffice |
| S-05 | Sem dependências vulneráveis | Dependências | `pip-audit` | Zero vulnerabilidades CVE |

### 1.6 Manutenibilidade (Maintainability)

| ID | Teste | Tipo | Ferramenta | Critério de Aceite |
|----|-------|------|------------|-------------------|
| M-01 | Complexidade ciclomática < 10 | Estático | `radon cc` | Max CC por função < 10 |
| M-02 | Duplicação de código < 5% | Estático | `radon raw` | DUPLIC < 5% |
| M-03 | Cobertura de testes ≥ 80% | Estático | `pytest-cov` | `coverage report` |
| M-04 | Sem código morto | Estático | Manual + `vulture` | Nenhuma função não utilizada |
| M-05 | Constantes unificadas | Estático | Manual | Sem duplicatas em `config.py` vs `models/` |
| M-06 | Tipagem completa | Estático | `mypy` | Zero erros de tipo |
| M-07 | Linting limpo | Estático | `flake8` | Zero erros (E/W) |

### 1.7 Portabilidade (Portability)

| ID | Teste | Tipo | Ferramenta | Critério de Aceite |
|----|-------|------|------------|-------------------|
| PO-01 | Instalação em ambiente limpo | Integração | `pip install` | `pip install -r requirements.txt` sem erros |
| PO-02 | Funciona em Linux | CI | GitHub Actions | Teste em runner Linux |
| PO-03 | Funciona em Windows | CI | GitHub Actions | Teste em runner Windows |
| PO-04 | CSV formato padrão | Unitário | `pytest` | Delimiter `,` ou `;`, encoding UTF-8 |
| PO-05 | Sem dependência de SO específico | Análise | Manual | Nenhuma chamada de sistema específica |

### 1.8 Compatibilidade (Compatibility)

| ID | Teste | Tipo | Ferramenta | Critério de Aceite |
|----|-------|------|------------|-------------------|
| C-01 | CSV aberto em Excel | Manual | Teste humano | Sem erros de parsing |
| C-02 | CSV aberto em LibreOffice | Manual | Teste humano | Sem erros de parsing |
| C-03 | Streamlit versão compatível | Integração | `pip install` | `streamlit==1.38.0` funciona |
| C-04 | Python 3.12 compatível | Integração | `pytest` | Todos os testes passam |

---

## 2. Plano de Observabilidade (OpenTelemetry + Prometheus + Grafana)

### 2.1 Arquitetura de Observabilidade

```
┌─────────────────────────────────────────────────────────────────┐
│                     Aplicação Streamlit                         │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │ OpenTelemetry   │  │ Prometheus       │  │ Health Check   │ │
│  │ Instrumentation │  │ Metrics Export   │  │ Endpoint       │ │
│  │ (traces/metrics)│  │ (/metrics)       │  │ (/health)      │ │
│  └────────┬────────┘  └────────┬─────────┘  └───────┬────────┘ │
│           │                    │                     │           │
└───────────┼────────────────────┼─────────────────────┼───────────┘
            │                    │                     │
            ▼                    ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Docker Compose Stack                        │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────────┐ │
│  │ Prometheus   │  │ Grafana      │  │ OpenTelemetry Collector│ │
│  │ :9090        │  │ :3000        │  │ :4317 (OTLP)          │ │
│  │ Scrape /metrics│ │ Dashboards  │  │ Export to Prometheus  │ │
│  └──────┬──────┘  └──────┬───────┘  └───────────┬───────────┘ │
│         │                │                       │             │
│         ▼                ▼                       ▼             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Persistent Storage (Volumes)                │   │
│  │  prometheus_data/  grafana_data/  otel_collector_data/  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Métricas Coletadas

| Categoria | Métrica | Tipo | Descrição |
|-----------|---------|------|-----------|
| **Aplicação** | `app_request_duration_seconds` | Histogram | Tempo de resposta por endpoint |
| **Aplicação** | `app_request_total` | Counter | Total de requisições por status |
| **Aplicação** | `app_calculation_duration_seconds` | Histogram | Tempo de cálculo do orçamento |
| **Aplicação** | `app_csv_export_total` | Counter | Total de exportações CSV |
| **Aplicação** | `app_error_total` | Counter | Total de erros por tipo |
| **Aplicação** | `app_active_users` | Gauge | Usuários ativos simultâneos |
| **Sistema** | `process_cpu_seconds_total` | Counter | CPU usado pelo processo |
| **Sistema** | `process_resident_memory_bytes` | Gauge | Memória RAM usada |
| **Sistema** | `process_open_fds` | Gauge | File descriptors abertos |
| **Health** | `app_health_status` | Gauge | 1=healthy, 0=unhealthy |

### 2.3 Dashboards Grafana

| Dashboard | Métricas Principais | Painéis |
|-----------|--------------------|---------|
| **Performance** | Latência, throughput, tempo de cálculo | Time series, heatmap, stat |
| **Saúde** | Status do app, erros, uptime | Status map, singlestat |
| **Recursos** | CPU, memória, file descriptors | Graph, gauge |
| **Negócio** | Orçamentos gerados, CSV exports, tipos de imóvel | Bar chart, pie chart |

### 2.4 Alertas

| Alerta | Condição | Severidade |
|--------|----------|-----------|
| Alta latência | P95 > 1s por 5 min | Warning |
| App indisponível | Health check falha | Critical |
| Alto uso de memória | RAM > 200MB por 5 min | Warning |
| Erro rate alto | Erros > 10% por 5 min | Critical |
| Cálculo lento | Tempo médio > 500ms por 5 min | Warning |

---

## 3. Scripts e Ferramentas a Criar

| Arquivo | Descrição |
|---------|-----------|
| `projeto/scripts/measure_nfrs.py` | Script principal de medição NFR |
| `projeto/tests/test_nfr_performance.py` | Testes de performance |
| `projeto/tests/test_nfr_security.py` | Testes de segurança |
| `projeto/tests/test_nfr_maintainability.py` | Testes de manutenibilidade |
| `projeto/otel_instrumentation.py` | OpenTelemetry instrumentation |
| `projeto/prometheus_metrics.py` | Prometheus metrics definitions |
| `projeto/health_check.py` | Health check endpoint |
| `projeto/load_test.py` | Script de teste de carga |
| `projeto/docker-compose.observability.yml` | Stack de observabilidade |
| `projeto/grafana/dashboard.json` | Dashboard Grafana |
| `projeto/prometheus/prometheus.yml` | Configuração Prometheus |
| `projeto/requirements-observability.txt` | Dependências de observabilidade |

---

## 4. Critérios de Aceitação para Produção

- [ ] Todos os testes unitários passam (37/37)
- [ ] Todos os testes Playwright passam (9/9)
- [ ] Todos os testes NFR passam (14/14)
- [ ] Cobertura de código ≥ 80%
- [ ] Complexidade ciclomática máxima < 10
- [ ] Zero vulnerabilidades de alta severidade (bandit)
- [ ] Tempo de resposta P95 < 500ms
- [ ] Memória P95 < 50MB
- [ ] CSV gerado válido e interoperável
- [ ] App instala e roda sem erros
- [ ] OpenTelemetry instrumentado e exportando métricas
- [ ] Prometheus coletando métricas
- [ ] Grafana dashboard configurado e acessível
- [ ] Alertas configurados e funcionando
- [ ] Código morto eliminado ou justificado
- [ ] Teste de carga passa (10 usuários simultâneos)