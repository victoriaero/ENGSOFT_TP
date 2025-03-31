# Trabalho Prático de Engenharia de Software - DataLabeler

## Proposta e Objetivo
O DataLabeler é uma ferramenta em desenvolvimento projetada para facilitar a rotulação de dados em tarefas de aprendizado supervisionado. O software permite a leitura de bases de dados em formatos comuns, como CSV e JSON, e a criação de amostras aleatórias a partir dessa base, o que ajuda a simplificar a tarefa de rotulação manual. 

O programa conta com dois tipos distintos de usuários, o desenvolvedor/dono da base de dados e o rotulador. 

O desenvolvedor terá a habilidade de fazer upload de suas bases, escolher labels pré determinadas a serem utilizadas, se as instâncias da base permitirão rotulações de labels múltiplas ou únicas, verificar as rotulações feitas até o momento, autorizar a geração de um dataset final ou parcial rotulado a partir da mescla de rotulações já feitas escolhidas.

Já o rotulador tem apenas um papel, visualizar o dado e classificar instâncias de acordo com os critérios pré determinados pelo desenvolvedor, adicionando uma ou mais labels facilmente a cada entrada de dados, garantindo que as amostras estejam prontas para treinamento de modelos de aprendizado de máquina. 

O principal objetivo é fazer com que o processo de labeling seja mais intuitivo e prático para o rotulador, especialmente porque muitas vezes esse participante não é alguém com experiência na área da computação, além de tornar o processo mais fluido e utilitário para os desenvolvedores, que precisam se preocupar menos com tecnicalidades e devem ter menos trabalho ao cooptar e instruir os rotuladores.

Outras funcionalidades incluem: salvar os dados rotulados, exportando-os em diferentes formatos como CSV ou JSON, filtrar as amostras geradas por critérios específicos, como valores numéricos ou categorias, a opção de visualizar a amostra antes de iniciar a rotulação, a variação do tamanho da amostra extraída e do número de labels (e respectivos nomes, para auxiliar na explicabilidade da classificação). E para a parte de gerar o dataset final/parcial rotulado a partir da mesclagem pretendemos implementar um sistema de comparação classificadores usando a métrica do Fleiss' Kappa, que avalia a concordância entre dois ou mais avaliadores nesse processo, a fim de garantir mais robustez e se aproximar dos métodos usados na academia para essa tarefa.

## Membros do grupo
### Lucas Dayrell de Andrade Machado - 2020035329 - Full
### Samira Araujo Malaquias Souza - 2022107580 - Front-end
### Caio Santana Trigueiro - 2022043310 - Back-end
### Victoria Estanislau Ramos de Oliveira - 2021037490 - Full

## Tecnologias a serem empregadas
### Back-end: Python
### Front-end: PyQT5 

## Backlog do Produto

### 1. Leitura de Bases de Dados em Formatos CSV e JSON
- **Descrição:** O sistema deve ser capaz de importar bases de dados nos formatos CSV e JSON para serem rotuladas.
- **Prioridade:** Alta
- **Critérios de Aceitação:** O sistema deve carregar corretamente os dados, mostrando as entradas para o usuário.

### 2. Criação de Amostras Aleatórias
- **Descrição:** A ferramenta deve permitir a criação de amostras aleatórias da base de dados para facilitar a rotulação.
- **Prioridade:** Alta
- **Critérios de Aceitação:** O usuário pode definir o tamanho da amostra e os dados devem ser extraídos aleatoriamente da base carregada.

### 3. Atribuição de Labels
- **Descrição:** O usuário pode rotular cada entrada de dados com uma ou mais labels.
- **Prioridade:** Alta
- **Critérios de Aceitação:** A interface permite adicionar múltiplos labels a cada entrada de dados.

### 4. Exportação de Dados Rotulados
- **Descrição:** O sistema deve permitir que o usuário exporte os dados rotulados nos formatos CSV ou JSON.
- **Prioridade:** Alta
- **Critérios de Aceitação:** Os dados devem ser exportados corretamente com as labels atribuídas.

### 5. Filtragem de Amostras
- **Descrição:** O usuário pode filtrar as amostras baseadas em critérios como valores numéricos ou categorias.
- **Prioridade:** Média
- **Critérios de Aceitação:** O sistema deve fornecer filtros eficientes para restringir as amostras exibidas ao usuário.

### 6. Visualização da Amostra Antes de Rotulação
- **Descrição:** O usuário pode visualizar a amostra antes de iniciar o processo de rotulação.
- **Prioridade:** Média
- **Critérios de Aceitação:** A visualização das amostras deve ser clara e acessível antes da rotulação.

### 7. Variação do Tamanho da Amostra e Número de Labels
- **Descrição:** O sistema deve permitir ao usuário configurar o número de amostras e a quantidade de labels a serem atribuídas.
- **Prioridade:** Média
- **Critérios de Aceitação:** O usuário pode definir o número de amostras e a quantidade de labels, além de personalizar os nomes dos labels.

### 8. Comparação de Classificadores com Fleiss' Kappa
- **Descrição:** Implementar uma comparação entre dois ou mais classificadores com a métrica Fleiss' Kappa para medir a concordância entre os avaliadores.
- **Prioridade:** Baixa
- **Critérios de Aceitação:** O sistema deve calcular e exibir a métrica Fleiss' Kappa corretamente.

### 9. Salvar o Progresso da Rotulação
- **Descrição:** O sistema deve permitir que o usuário salve o progresso da rotulação para retomar mais tarde.
- **Prioridade:** Média
- **Critérios de Aceitação:** O sistema deve salvar os dados rotulados e permitir que o usuário os recarregue posteriormente.

### 10. Interface de Ajuda (Tooltips)
- **Descrição:** A ferramenta deve fornecer dicas e orientações sobre como usar as funcionalidades, exibindo tooltips em pontos chave da interface.
- **Prioridade:** Baixa
- **Critérios de Aceitação:** A interface deve apresentar tooltips que ajudem o usuário a entender as funcionalidades da ferramenta.


# Backlogs das Sprints - DataLabeler 
(Tarefas atribuídas para os membros do grupo aleatóriamente, sujeito a mudança)

## Sprint 1 Backlog - Fundação e Fluxo Básico

*Objetivo do Sprint: Estabelecer a capacidade central de carregar dados, criar uma amostra, rotular (forma simples) e exportar.*

### História #1: Leitura de Bases de Dados em Formatos CSV e JSON (Prioridade: Alta)
* **Descrição:** O sistema deve ser capaz de importar bases de dados nos formatos CSV e JSON para serem rotuladas.
* **Tarefas e Responsáveis:**
    * - [Backend] Implementar função de leitura e parsing de arquivos CSV [Lucas]
    * - [Backend] Implementar função de leitura e parsing de arquivos JSON [Lucas]
    * - [Frontend] Criar interface para seleção de arquivo (CSV/JSON) [Samira]
    * - [Frontend] Integrar backend para carregar e exibir prévia/confirmação dos dados carregados [Samira]
    * - [Testes] Criar testes unitários para leitura de CSV e JSON [Caio]

### História #2: Criação de Amostras Aleatórias (Prioridade: Alta)
* **Descrição:** A ferramenta deve permitir a criação de amostras aleatórias da base de dados para facilitar a rotulação.
* **Tarefas e Responsáveis:**
    * - [Backend] Implementar lógica para extrair amostra aleatória de tamanho N da base carregada [Lucas]
    * - [Frontend] Adicionar campo na interface para o usuário definir o tamanho da amostra [Victoria]
    * - [Frontend] Implementar botão "Gerar Amostra" e conectar com o backend [Victoria]
    * - [Frontend] Exibir a amostra gerada em uma tabela/lista na interface [Samira]

### História #3: Atribuição de Labels (Prioridade: Alta - Versão Inicial Simples)
* **Descrição:** O usuário pode rotular cada entrada de dados com *uma* label (versão inicial).
* **Tarefas e Responsáveis:**
    * - [Backend] Definir estrutura de dados para armazenar instância + label associada [Caio]
    * - [Frontend] Para cada item da amostra, adicionar botões/dropdown para selecionar UMA label pré-definida (ex: Positivo/Negativo) [Victoria]
    * - [Frontend] Armazenar a label selecionada para cada instância da amostra atual [Victoria]

### História #4: Exportação de Dados Rotulados (Prioridade: Alta)
* **Descrição:** O sistema deve permitir que o usuário exporte os dados rotulados nos formatos CSV ou JSON.
* **Tarefas e Responsáveis:**
    * - [Backend] Implementar função para gerar arquivo CSV com dados + coluna de label [Lucas]
    * - [Backend] Implementar função para gerar arquivo JSON com dados + campo de label [Lucas]
    * - [Frontend] Adicionar botões "Exportar CSV" e "Exportar JSON" [Samira]
    * - [Frontend] Integrar botões de exportação com as funções do backend [Samira]
    * - [Testes] Criar testes unitários para exportação em CSV e JSON [Caio]

---

## Sprint 2 Backlog - Múltiplas Labels, Configuração e Visualização

*Objetivo do Sprint: Implementar a funcionalidade de múltiplas labels, permitir a configuração pelo desenvolvedor e melhorar a visualização.*

### História #3 (Refinamento): Atribuição de Labels (Suporte a Múltiplas Labels)
* **Descrição:** O usuário pode rotular cada entrada de dados com uma ou mais labels, conforme configurado pelo desenvolvedor.
* **Tarefas e Responsáveis:**
    * - [Backend] Modificar estrutura de dados para suportar lista de labels por instância [Caio]
    * - [Backend] Implementar lógica para o Desenvolvedor definir labels disponíveis e modo (única/múltipla) [Lucas]
    * - [Frontend] Criar interface de configuração (para Desenvolvedor) para definir labels e modo [Victoria]
    * - [Frontend] Modificar interface de rotulação para suportar seleção múltipla (ex: checkboxes) se configurado [Samira]
    * - [Testes] Atualizar testes de atribuição e exportação para múltiplas labels [Caio]

### História #7: Variação do Tamanho da Amostra e Número de Labels (Prioridade: Média)
* **Descrição:** O sistema deve permitir ao usuário (Desenvolvedor) configurar o número de amostras e a quantidade/nomes de labels a serem atribuídas.
* **Tarefas e Responsáveis:**
    * - [Backend] Armazenar configurações de labels (nomes, quantidade) definidas pelo Desenvolvedor [Lucas]
    * - [Frontend] Refinar interface de configuração (História #3) para incluir nomes customizados de labels [Victoria]
    * - [Frontend] Garantir que a interface de rotulação use os nomes e quantidade de labels definidos [Samira]

### História #6: Visualização da Amostra Antes de Rotulação (Prioridade: Média)
* **Descrição:** O usuário pode visualizar a amostra antes de iniciar o processo de rotulação.
* **Tarefas e Responsáveis:**
    * - [Frontend] Criar uma etapa/tela de "Preview da Amostra" após a geração e antes da rotulação [Samira]
    * - [Frontend] Exibir os dados da amostra nesta tela de preview de forma clara [Samira]
    * - [Frontend] Adicionar botões "Iniciar Rotulação" ou "Gerar Nova Amostra" na tela de preview [Victoria]

### História #: Distinção de Papéis (Desenvolvedor/Rotulador)
* **Descrição:** Implementar a lógica básica para diferenciar as funcionalidades disponíveis para Desenvolvedores e Rotuladores.
* **Tarefas e Responsáveis:**
    * - [Backend] Implementar um mecanismo simples de identificação de papel (pode ser inicial, sem login complexo) [Caio]
    * - [Frontend] Adaptar a interface para mostrar/ocultar opções com base no papel do usuário (ex: Configuração só para Desenvolvedor) [Victoria]

---

## Sprint 3 Backlog - Persistência, Filtragem e Progresso

*Objetivo do Sprint: Permitir salvar e carregar o progresso, filtrar amostras e dar visibilidade sobre o andamento da rotulagem.*

### História #9: Salvar o Progresso da Rotulação (Prioridade: Média)
* **Descrição:** O sistema deve permitir que o usuário salve o progresso da rotulação para retomar mais tarde.
* **Tarefas e Responsáveis:**
    * - [Backend] Definir formato e implementar lógica para salvar o estado atual da rotulagem (quais instâncias foram rotuladas e com quais labels) em um arquivo [Lucas]
    * - [Backend] Implementar lógica para carregar um arquivo de progresso salvo e restaurar o estado na aplicação [Lucas]
    * - [Frontend] Adicionar botões/menu "Salvar Progresso" e "Carregar Progresso" [Samira]
    * - [Frontend] Integrar funcionalidade de salvar/carregar com o backend [Samira]
    * - [Testes] Criar testes para salvar e carregar progresso [Caio]

### História #5: Filtragem de Amostras (Prioridade: Média)
* **Descrição:** O usuário pode filtrar as amostras baseadas em critérios como valores numéricos ou categorias (em colunas específicas).
* **Tarefas e Responsáveis:**
    * - [Backend] Implementar lógica de filtragem de dados baseada em critérios (ex: coluna X > valor Y, coluna Z == 'categoria A') [Caio]
    * - [Frontend] Criar elementos de UI para o usuário definir filtros (selecionar coluna, operador, valor) [Victoria]
    * - [Frontend] Aplicar o filtro definido à visualização da amostra (antes ou durante a rotulação) [Victoria]
    * - [Testes] Criar testes para a lógica de filtragem [Lucas]

### História #: Visualização de Progresso (Desenvolvedor)
* **Descrição:** O Desenvolvedor pode verificar as rotulações feitas até o momento.
* **Tarefas e Responsáveis:**
    * - [Backend] Implementar função para sumarizar o estado da rotulagem (quantos itens rotulados, distribuição de labels, etc.) [Caio]
    * - [Frontend] Criar uma tela/painel para o Desenvolvedor visualizar o sumário do progresso da rotulagem [Samira]
    * - [Frontend] (Opcional) Permitir ao Desenvolvedor visualizar as labels atribuídas a instâncias específicas [Samira]

---

## Sprint 4 Backlog - Concordância entre Avaliadores e Usabilidade

*Objetivo do Sprint: Implementar a métrica de concordância Fleiss' Kappa e melhorar a usabilidade com tooltips.*

### História #8: Comparação de Classificadores com Fleiss' Kappa (Prioridade: Baixa)
* **Descrição:** Implementar uma comparação entre (potencialmente) múltiplos arquivos de rotulação usando a métrica Fleiss' Kappa para medir a concordância.
* **Tarefas e Responsáveis:**
    * - [Backend] Pesquisar e escolher biblioteca Python para cálculo do Fleiss' Kappa ou implementar a fórmula [Lucas]
    * - [Backend] Implementar lógica para carregar múltiplos arquivos de rotulação (progresso salvo ou exportado) referentes à *mesma* amostra/base [Caio]
    * - [Backend] Preparar os dados carregados no formato exigido pela métrica Fleiss' Kappa [Caio]
    * - [Backend] Calcular e retornar o valor do Fleiss' Kappa [Lucas]
    * - [Frontend] Criar interface para o Desenvolvedor selecionar múltiplos arquivos de rotulação para comparação [Victoria]
    * - [Frontend] Exibir o resultado do cálculo do Fleiss' Kappa para o Desenvolvedor [Victoria]
    * - [Testes] Criar testes para o cálculo e integração do Fleiss' Kappa [Samira]

### História #10: Interface de Ajuda (Tooltips) (Prioridade: Baixa)
* **Descrição:** A ferramenta deve fornecer dicas e orientações sobre como usar as funcionalidades, exibindo tooltips em pontos chave da interface.
* **Tarefas e Responsáveis:**
    * - [Frontend] Identificar pontos chave da interface que se beneficiariam de tooltips (botões, campos complexos, etc.) [Samira]
    * - [Frontend] Implementar a exibição de tooltips com textos explicativos nesses pontos chave usando PyQT5 [Samira]
    * - [Conteúdo] Redigir textos claros e concisos para os tooltips [Victoria/Caio]

### História #11: Geração de Dataset Final/Parcial (Desenvolvedor)
* **Descrição:** Permitir ao desenvolvedor gerar um dataset final a partir da mescla de rotulações (preparação para usar Kappa).
* **Tarefas e Responsáveis:**
    * - [Backend] Implementar lógica para mesclar dados de diferentes arquivos de rotulação (associando labels de diferentes rotuladores à mesma instância) [Lucas]
    * - [Frontend] Criar interface para o Desenvolvedor selecionar os arquivos de rotulação a serem mesclados e gerar o dataset final [Victoria]
    * - [Frontend] Integrar a geração do dataset com a exibição opcional da concordância (Kappa) se aplicável [Victoria]

---

## Sprint 5 Backlog - Refinamento, Testes Finais e Documentação

*Objetivo do Sprint: Realizar testes abrangentes, corrigir bugs, refinar a interface com base no feedback e finalizar a documentação.*

### História #Geral: Testes e Correção de Bugs
* **Descrição:** Garantir a estabilidade e o correto funcionamento de todas as funcionalidades implementadas.
* **Tarefas e Responsáveis:**
    * - [Testes] Executar testes de integração cobrindo os fluxos principais (Desenvolvedor e Rotulador) [Caio]
    * - [Testes] Realizar testes de usabilidade com potenciais usuários (se possível) [Todos]
    * - [Desenvolvimento] Corrigir bugs identificados durante os testes das Sprints anteriores e desta Sprint [Todos]
    * - [Desenvolvimento] Revisar e refatorar código para clareza e performance onde necessário [Todos]

### História #Geral: Refinamento da Interface e UX
* **Descrição:** Melhorar a experiência do usuário com base nos testes e feedback.
* **Tarefas e Responsáveis:**
    * - [Frontend] Ajustar layout, mensagens de erro/sucesso e fluxo de navegação conforme feedback [Samira/Victoria]
    * - [Frontend] Garantir consistência visual e de interação em toda a aplicação [Samira/Victoria]

### História #Geral: Documentação Final
* **Descrição:** Finalizar a documentação do projeto, incluindo o README.
* **Tarefas e Responsáveis:**
    * - [Documentação] Revisar e completar o README.md no GitHub com instruções de instalação, uso e descrição final [Lucas]
    * - [Documentação] Adicionar comentários relevantes no código onde ainda faltar [Todos]
    * - [Documentação] Preparar uma breve apresentação ou relatório final do projeto (se aplicável) [Todos]
