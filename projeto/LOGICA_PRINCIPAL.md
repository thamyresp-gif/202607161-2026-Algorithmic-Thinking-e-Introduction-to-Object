# Lógica Principal do Programa — Orçamento de Aluguel R.M

## Visão Geral

A aplicação calcula o orçamento de aluguel mensal para três tipos de imóveis (Apartamento, Casa, Estúdio), aplicando regras de negócio específicas para cada tipo, e gera um CSV com o detalhamento de 12 parcelas.

## Fluxo Principal

1. **Entrada de dados** — O usuário preenche o formulário Streamlit com: tipo de imóvel, endereço, quartos, vagas, nome do locatário, opção de filhos, e parcelamento do contrato.

2. **Validação** — Verifica se os campos obrigatórios (endereço e nome) foram preenchidos. Se não, exibe erro e interrompe o fluxo.

3. **Instanciação polimórfica** — Com base no tipo de imóvel selecionado, cria-se a instância correta (`Apartamento`, `Casa` ou `Estudio`). Cada subclasse herda de `Imovel` (ABC) e implementa seus próprios cálculos de acréscimo, garagem e desconto.

4. **Cálculo do aluguel líquido** — O método `calcular_total_aluguel()` executa em sequência:
   - `calcular_valor_base()` → retorna o valor base fixo do tipo
   - `calcular_acrescimo_quartos()` → aplica acréscimo se 2 quartos (APART: +R$200, CASA: +R$250)
   - `calcular_vagas_garagem()` → aplica regra específica por tipo (CASA/APART: R$300/vaga; ESTUDIO: R$250 para 2 vagas + R$60/vaga extra)
   - `calcular_desconto()` → aplica 5% de desconto no APARTAMENTO para locatários sem filhos
   - `total_aluguel = base + acrescimos + garagem - desconto`

5. **Parcelamento do contrato** — Se o usuário optar por parcelar, o valor de R$2.000 é dividido pelo número de parcelas (máx. 5). Caso contrário, o valor integral é considerado.

6. **Total mensal** — `total_mensal = total_aluguel + parcela_contrato`

7. **Geração das 12 parcelas** — Para cada mês (1 a 12):
   - Se parcelado e mês ≤ N parcelas: inclui o valor da parcela do contrato
   - Caso contrário: parcela do contrato = R$0
   - `valor_total = valor_aluguel + valor_parcela_contrato`

8. **Exportação CSV** — Gera arquivo `.csv` com as 12 parcelas e um resumo consolidado.

## Pensamento Algorítmico Aplicado

| Conceito | Aplicação no Código |
|----------|---------------------|
| **Abstração** | Classe abstrata `Imovel` define a interface comum (`calcular_valor_base`, `calcular_acrescimo_quartos`, `calcular_vagas_garagem`, `calcular_desconto`) |
| **Herança** | `Apartamento`, `Casa` e `Estudio` herdam de `Imovel` e reutilizam a lógica de `calcular_total_aluguel()` |
| **Polimorfismo** | Cada subclasse implementa os métodos abstratos com regras específicas — o mesmo método `calcular_desconto()` retorna valores diferentes para cada tipo |
| **Encapsulamento** | Cada classe gerencia seus próprios dados e regras de cálculo; a orquestração é feita pela classe `Orcamento` |
| **Decomposição** | O problema complexo (orçamento completo) é decomposto em subproblemas menores: cálculo de base, acréscimos, descontos, garagem, parcelamento |
| **Algoritmos de seleção** | `if/elif/else` para escolher o tipo de imóvel e aplicar regras condicionais (desconto, parcelamento) |
| **Algoritmos de repetição** | `for i in range(1, 13)` para gerar as 12 parcelas |
| **Estruturas de dados** | Dicionários para retornar resultados compostos; listas para armazenar as 12 parcelas |
| **Arredondamento** | `round()` aplicado em todos os cálculos monetários para evitar erros de ponto flutuante |
| **Validação** | Verificação de inputs obrigatórios antes de prosseguir com os cálculos |
| **Reutilização de código** | `calcular_total_aluguel()` é chamado uma vez e reutilizado tanto para o resumo quanto para as parcelas |