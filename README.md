# Trabalho Prático de Engenharia de Software - DataLabeler

## Proposta e Objetivo
O DataLabeler é uma ferramenta em desenvolvimento projetada para facilitar a rotulação de dados em tarefas de aprendizado supervisionado. O software permite a leitura de bases de dados em formatos comuns, como CSV, e a criação de amostras aleatórias a partir dessa base, o que ajuda a simplificar a tarefa de rotulação manual. Com o DataLabeler, o usuário pode adicionar uma ou mais labels facilmente a cada entrada de dados, garantindo que as amostras estejam prontas para treinamento de modelos de aprendizado de máquina. Além disso, a ferramenta permite salvar os dados rotulados, exportando-os em diferentes formatos como CSV ou JSON. Outras funcionalidades incluem a possibilidade de filtrar as amostras geradas por critérios específicos, como valores numéricos ou categorias, a opção de visualizar a amostra antes de iniciar a rotulação, a variação do tamanho da amostra extraída e do número de labels (e respectivos nomes, para auxiliar na explicabilidade da classificação). Pretendemos também implementar um sistema de comparação de dois ou mais classificadores usando a métrica do Fleiss' Kappa, que avalia a concordância entre dois ou mais avaliadores nesse processo, a fim de garantir mais robustez e se aproximar dos métodos usados na academia para essa tarefa.

## Membros do grupo
### Lucas Dayrell de Andrade Machado - 2020035329 - x-End
### Samira Araujo Malaquias Souza - 2022107580 - y-End
### Caio Santana Trigueiro - 2022043310 - z-End
### Victoria Estanislau Ramos de Oliveira - 2021037490 - w-End

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
