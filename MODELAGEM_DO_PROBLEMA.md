# Modelagem do Problema — Orçamento de Aluguel

## 1. Título

**Orçamento de Aluguel** — Calculadora de orçamento de aluguel para a imobiliária R.M

---

## 2. Desafio

Gerar um orçamento de aluguel mensal automatizado para a empresa **R.M**, especializada na locação de casas, apartamentos e estúdios.

Uma aplicação de imobiliária é um sistema digital desenvolvido para facilitar a gestão e a negociação de imóveis. Ela permite que os administradores cadastrem propriedades disponíveis para aluguel, incluindo informações como localização, preço, características do imóvel (como número de quartos, banheiros e metragem), fotos e status da negociação. O sistema também pode oferecer funcionalidades como controle de contratos, agendamento de visitas e gerenciamento de clientes e corretores.

**Objetivo:** Automatizar e facilitar a geração de orçamentos de imóveis para os clientes da R.M, atendendo às necessidades operacionais e comerciais da imobiliária.

---

## 3. Business Drivers (Motivadores de Negócio)

| # | Driver | Descrição |
|---|--------|-----------|
| 1 | **Automação de Processos** | Automatizar a geração de orçamentos de imóveis, reduzindo o esforço manual |
| 2 | **Eficiência Operacional** | Facilitar as necessidades operacionais e comerciais da imobiliária, que lida com diversos tipos de propriedades (casas, apartamentos e estúdios) |
| 3 | **Melhoria no Atendimento ao Cliente** | Prover uma ferramenta rápida e precisa para que os clientes recebam orçamentos detalhados de locação |

---

## 4. Requisitos Funcionais

### 4.1 Tipos de Locação e Valores Base

A R.M trabalha com 3 tipos de locação e valores padrão:

| Tipo de Imóvel | Valor Base | Quartos |
|----------------|-----------|---------|
| Apartamento | R$ 700,00 | 1 quarto |
| Casa | R$ 900,00 | 1 quarto |
| Estúdio | R$ 1.200,00 | — |

### 4.2 Acréscimos por Quartos

- **Apartamentos de 2 quartos:** +R$ 200,00
- **Casas de 2 quartos:** +R$ 250,00

### 4.3 Gerenciamento de Vagas de Garagem

| Tipo de Imóvel | Regra |
|----------------|-------|
| Casas e Apartamentos | +R$ 300,00 por vaga |
| Estúdios | R$ 250,00 por duas vagas; R$ 60,00 por cada vaga adicional |

### 4.4 Descontos

- **5% de desconto** no aluguel de apartamentos para locatários **sem filhos**

### 4.5 Taxa de Contrato

- Valor fixo de **R$ 2.000,00**
- Pode ser **parcelado em até 5 vezes** no orçamento

### 4.6 Exibição de Resumo

- Apresentar o **valor total do aluguel mensal** somado à **parcela do contrato**

### 4.7 Exportação de Dados

- Gerar um arquivo **`.csv`** contendo as **12 parcelas** do orçamento planejado

---

## 5. Requisitos Não Funcionais (Baseados no SWEBOK 4.0)

| # | Requisito | Descrição |
|---|-----------|-----------|
| 1 | **Manutenibilidade** | O sistema deve obrigatoriamente utilizar princípios de POO e ser bem estruturado |
| 2 | **Portabilidade** | A aplicação deve gerar saídas em formato padrão interoperável (CSV) |
| 3 | **Funcionalidade/Confiabilidade** | O código deve estar funcional e demonstrar o pensamento algorítmico aplicado |
| 4 | **Documentação Técnica** | Entrega de fluxograma e descrição da estrutura lógica do programa |
| 5 | **Usabilidade** | Interface amigável (alinhado ao SWEBOK) |
| 6 | **Eficiência de Desempenho** | Desempenho adequado para o domínio do problema (alinhado ao SWEBOK) |

---

## 6. Arquitetura do Software

A arquitetura sugerida é **Modular baseada em Camadas**, considerando as exigências de POO e a possibilidade de interface:

```
┌─────────────────────────┐
│   Camada de Visão       │  ← CLI (console) ou Interface HTML/CSS
│   (View)                │
├─────────────────────────┤
│   Camada de Controle    │  ← Orquestra o fluxo de dados entre Model e View
├─────────────────────────┤
│   Camada de Modelo      │  ← Classes: Imóvel, Apartamento, Casa, Estúdio, Orçamento
│   (Model)               │     Contêm regras de cálculo e lógica de negócio
├─────────────────────────┤
│   Camada de Persistência│  ← Geração e gravação do arquivo .csv
│   /Saída                │
└─────────────────────────┘
```

### 6.1 Camada de Modelo (Model)

- **Imóvel** (classe base/abstrata) — atributos comuns a todos os imóveis
- **Apartamento** — valor base R$ 700,00; acréscimo por quarto R$ 200,00; vaga garagem R$ 300,00; desconto 5% sem filhos
- **Casa** — valor base R$ 900,00; acréscimo por quarto R$ 250,00; vaga garagem R$ 300,00
- **Estúdio** — valor base R$ 1.200,00; vagas R$ 250,00 (2 vagas) / R$ 60,00 (adicional)
- **Orçamento** — orquestra cálculos totais, parcelamento da taxa de contrato e exportação CSV

### 6.2 Camada de Visão (View)

- Interface via **console (CLI)** ou **HTML/CSS**

### 6.3 Camada de Persistência/Saída

- Módulo responsável pela geração e gravação do arquivo `.csv`

### 6.4 Controle de Versão

- Uso obrigatório de repositório **GitHub** para hospedagem do código

---

## 7. Opções de Tecnologias

| Categoria | Tecnologia | Justificativa |
|-----------|-----------|---------------|
| **Linguagem Principal** | Python | Vasta documentação e tutoriais recomendados |
| **Interface Gráfica/Web** | HTML e CSS | Opção para aplicação com interface (conforme documento) |
| **Frameworks Web** (opcional) | Flask ou Django | Integração Python + HTML/CSS; mencionados em guias de estudo |
| **Manipulação de Dados** | Bibliotecas nativas do Python (csv) | Geração de arquivos CSV |
| **Ferramentas de Design** | Lucidchart, Draw.io ou similar | Criação do fluxograma obrigatório |
| **Controle de Versão** | Git + GitHub | Hospedagem do código-fonte |

---

## 8. Fontes de Pesquisa

| Fonte | Link | Descrição |
|-------|------|-----------|
| Python.org — Tutorial Oficial | https://www.python.org/doc/ | Documentação oficial do Python; tutorial abrangente desde conceitos básicos até POO e manipulação de arquivos |
| DevMedia — Guia Completo de Python | — | Guia de estudo para Python |

---

## 9. Entregáveis e Distribuição da Pontuação

| Parte | Peso | Descrição |
|-------|------|-----------|
| **Teórica** | 25% | Fluxograma da aplicação e descrição da estrutura lógica do programa (em PDF), incluindo pseudocódigo ou comentários explicativos sobre o pensamento algorítmico aplicado |
| **Prática** | 50% | Código-fonte funcional (.py), arquivos HTML/CSS (se houver interface), link do repositório GitHub. O código deve estar funcional, bem estruturado e utilizar princípios de POO |
| **Vídeo Pitch** | 25% | Vídeo de até 4 minutos (gravador de tela) explicando o projeto, destacando trechos do código e demonstrando a navegação. Deve ser publicado no YouTube ou redes sociais (LinkedIn) e o link enviado para avaliação |

---

## 10. Fontes Utilizadas

- `init.md` — guia estruturado do projeto com requisitos, arquitetura e tecnologias
- `TRABALHO - Algorithmic Thinking & Introduction to Object-Oriented Programming.docx - Copy (.docx` — documento oficial do trabalho com desafio, funcionalidades, fontes de pesquisa e critérios de avaliação