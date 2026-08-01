Trabalho de Faculdade
1 fonte
·
22 de jul. de 2026
Este documento descreve um projeto acadêmico focado em pensamento algorítmico e programação orientada a objetos utilizando a linguagem Python. O desafio central consiste em desenvolver um software para a empresa R.M que automatize a geração de orçamentos de aluguel, considerando diferentes tipos de imóveis, taxas de contrato e variáveis como número de quartos ou vagas de garagem. Para apoiar a execução, o texto sugere diversas fontes de pesquisa, incluindo documentações oficiais e tutoriais interativos. A avaliação final exige a entrega de um fluxograma lógico, o código-fonte funcional hospedado no GitHub e um vídeo explicativo sobre o funcionamento da aplicação. O material serve como um guia estruturado para que o estudante demonstre competências técnicas em desenvolvimento de sistemas e organização de projetos digitais.

quarta-feira, 22 de julho

Quero entender o business drivers; 2. Quero listyra os requisitos funcionais de acrodo com o documento. 3. quero listar os requisitos não funcicionáis do noassa aplicação de acordo com o sweok4.0. 4. Eu qeuro listar a arquitetura do meu software. 5. me de opções de tecnologias para trabalhar  em cima.

Com base no documento fornecido, aqui estão as informações solicitadas para o desenvolvimento do seu projeto de Calculadora de Orçamento de Aluguel:
1. Business Drivers (Motivadores de Negócio)
Os principais impulsionadores para o desenvolvimento desta aplicação para a empresa R.M são:
Automação de Processos: O objetivo central é automatizar a geração de orçamentos de imóveis, reduzindo o esforço manual
.
Eficiência Operacional: Facilitar as necessidades operacionais e comerciais da imobiliária, que lida com diversos tipos de propriedades (casas, apartamentos e estúdios)
.
Melhoria no Atendimento ao Cliente: Prover uma ferramenta rápida e precisa para que os clientes recebam orçamentos detalhados de locação
.
2. Requisitos Funcionais
De acordo com as regras de negócio descritas, a aplicação deve:
Gerar orçamentos baseados em três tipos de locação: Apartamentos (R700,00),Casas(R 900,00) e Estúdios (R$ 1.200,00)
.
Calcular acréscimos por quartos: Somar R200,00paraapartamentosde2quartoseR 250,00 para casas de 2 quartos
.
Gerenciar vagas de garagem: Adicionar R300,00paracasaseapartamentos
.Paraest 
u
ˊ
 dios,cobrarR 250,00 por duas vagas e R$ 60,00 por cada vaga adicional
.
Aplicar descontos: Conceder 5% de desconto no aluguel de apartamentos para locatários sem filhos
.
Processar Taxa de Contrato: Incluir um valor fixo de R$ 2.000,00, que pode ser parcelado em até 5 vezes no orçamento
.
Exibir Resumo: Apresentar o valor total do aluguel mensal somado à parcela do contrato
.
Exportar Dados: Gerar um arquivo ".csv" contendo as 12 parcelas do orçamento planejado
.
3. Requisitos Não Funcionais (Baseados no SWEBOK e Documento)
Embora o SWEBOK 4.0 não seja citado diretamente nas fontes, o documento estabelece padrões técnicos que se alinham a ele (informações adicionais fora das fontes marcadas como tal):
Manutenibilidade: O sistema deve obrigatoriamente utilizar princípios de Programação Orientada a Objetos (POO) e ser bem estruturado
.
Portabilidade: A aplicação deve ser capaz de gerar saídas em formato padrão interoperável (CSV)
.
Funcionalidade/Confiabilidade: O código deve estar funcional e demonstrar o pensamento algorítmico aplicado
.
Documentação Técnica: É exigida a entrega de um fluxograma e a descrição da estrutura lógica do programa
.
Nota: De acordo com o SWEBOK (fora das fontes), requisitos como Usabilidade (interface amigável) e Eficiência de Desempenho também seriam fundamentais aqui.
4. Arquitetura do Software
Considerando as exigências de POO e a possibilidade de interface, a arquitetura sugerida é a Modular baseada em Camadas:
Camada de Modelo (Model): Classes que representam as entidades (Imóvel, Apartamento, Casa, Estúdio, Orçamento) e contêm as regras de cálculo e lógica de negócio
.
Camada de Visão (View): Pode ser via console (CLI) ou uma interface HTML/CSS, conforme mencionado como opção no documento
.
Camada de Persistência/Saída: Módulo responsável pela geração e gravação do arquivo .csv
.
Controle de Versão: Uso obrigatório de repositório GitHub para hospedagem do código
.
5. Opções de Tecnologias
As fontes sugerem e permitem as seguintes tecnologias para o projeto:
Linguagem Principal: Python, devido à vasta documentação e tutoriais recomendados
.
Interface Gráfica/Web: HTML e CSS caso opte por uma aplicação com interface
.
Frameworks Web (Opcional - Fora das fontes): Para integrar o Python com HTML/CSS, você pode usar Flask ou Django, que são mencionados em guias de estudo sugeridos
.
Manipulação de Dados: Bibliotecas nativas do Python para manipulação de arquivos CSV
.
Ferramentas de Design: Ferramentas para criação do fluxograma obrigatório (como Lucidchart, Draw.io ou similar)
.
Você gostaria que eu criasse um relatório detalhado com a estrutura de classes em Python para este projeto ou prefere um quiz para testar seu conhecimento sobre os requisitos listados?