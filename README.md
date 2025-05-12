# Trabalho Prático de Engenharia de Software - DataLabeler

## Proposta e Objetivo
O DataLabeler é uma ferramenta em desenvolvimento projetada para facilitar a rotulação de dados em tarefas de aprendizado supervisionado. O software permite a leitura de bases de dados em formatos comuns, como CSV e JSON, e a criação de amostras aleatórias a partir dessa base, o que ajuda a simplificar a tarefa de rotulação manual. 

O programa conta com o rotulador como usuário com login e senha e uma opção de entrar como dev com uma senha global (o programa deve ser hosteado por aquele que pretende disponibilizar os datasets a serem avaliados).

O desenvolvedor/host terá a habilidade de escolher suas bases, escolher labels pré determinadas a serem utilizadas, se as instâncias da base permitirão rotulações de labels múltiplas ou únicas, verificar as rotulações feitas até o momento, autorizar a geração de um dataset final ou parcial rotulado a partir da mescla de rotulações já feitas escolhidas.

Já o rotulador tem apenas um papel, visualizar o dado e classificar instâncias de acordo com os critérios pré determinados pelo desenvolvedor, adicionando uma ou mais labels facilmente a cada entrada de dados, garantindo que as amostras estejam prontas para treinamento de modelos de aprendizado de máquina. 

O principal objetivo é fazer com que o processo de labeling seja mais intuitivo e prático para o rotulador, especialmente porque muitas vezes esse participante não é alguém com experiência na área da computação, além de tornar o processo mais fluido e utilitário para os desenvolvedores, que precisam se preocupar menos com tecnicalidades e devem ter menos trabalho ao cooptar e instruir os rotuladores.

Outras funcionalidades incluem: salvar os dados rotulados, exportando-os em diferentes formatos como CSV ou JSON, filtrar as amostras geradas por critérios específicos, como valores numéricos ou categorias, a opção de visualizar a amostra antes de iniciar a rotulação, a variação do tamanho da amostra extraída e do número de labels (e respectivos nomes, para auxiliar na explicabilidade da classificação).

## Membros do grupo
### Lucas Dayrell de Andrade Machado - 2020035329 - Full
### Samira Araujo Malaquias Souza - 2022107580 - Front-end
### Caio Santana Trigueiro - 2022043310 - Back-end
### Victoria Estanislau Ramos de Oliveira - 2021037490 - Full

## Tecnologias a serem empregadas
### Back-end: 

-**Python 3.10**

-**FastAPI**

-**SQLite** como DB

-**SQLAlchemy** para modelagem e acesso do DB

-**Uvicorn** como servidor ASGI

### Front-end: 

-**HTML5**

-**CSS3**

-**JavaScript** puro

-**FetchAPI** para comunicar com o Back-end

## Backlog do Produto

### 1. Registro de Datasets (CSV / JSONL)
- **Descrição:** upload via `/datasets/register`, detecção automática de separador, criação de atributos e samples sem repetição.
- **Prioridade:** Alta  
- **Critérios de Aceitação:**  
  - A API aceita JSON com `path`, `type`, `sample_size`, `num_samples`, etc.  
  - O backend lê as primeiras linhas do arquivo, detecta separador, cria atributos e gera samples aleatórios sem repetir índices.  
  - O frontend (`register.html` + `register2.html`) envia o payload corretamente e navega para a próxima etapa.

### 2. Configuração de Labels e Atributos
- **Descrição:** tela de configuração (`register2.html`) para escolher quais atributos serão exibidos aos anotadores e definir as labels.
- **Prioridade:** Alta  
- **Critérios de Aceitação:**  
  - O endpoint `POST /datasets/{id}/configure` grava as listas de atributos e labels.  
  - O frontend carrega `/datasets/{id}/attributes`, permite marcação e envia labels separadas por vírgula.

### 3. Geração de Amostras Aleatórias Sem Reposição *(Implementado)*
- **Descrição:** criar `num_samples` grupos de `sample_size` instâncias, sem índices repetidos.
- **Prioridade:** Alta  
- **Critérios de Aceitação:**  
  - `required = sample_size × num_samples ≤ total_rows` valida antes de criar.  
  - Usa `random.shuffle` + fatias do array de índices.  

### 4. Fluxo de Rotulação de Instâncias
- **Descrição:** exibir as linhas de cada sample em `classify.html`, permitir seleção de uma ou múltiplas labels e salvar via `POST /annotations/`.
- **Prioridade:** Alta  
- **Critérios de Aceitação:**  
  - API `/sample_rows/by_sample/{id}` retorna `row.data` completo.  
  - Frontend percorre `currentRows`, mostra atributos dinâmicos, coleta checkboxes/radios e envia anotações.

### 5. Exportação de Dados Rotulados
- **Descrição:** permitir download dos dados anotados em CSV ou JSON.
- **Prioridade:** Média  
- **Critérios de Aceitação:**  
  - Rotas `GET /datasets/{id}/export?format=csv` e `?format=json`.  
  - Frontend exibe botões “Exportar CSV” e “Exportar JSON” no dashboard.

### 6. Filtragem de Amostras
- **Descrição:** fornecer filtros por valor de atributo antes ou durante a rotulação.
- **Prioridade:** Média  
- **Critérios de Aceitação:**  
  - Endpoint `/sample_rows/by_sample/{id}?filter[col]=valor`.  
  - UI em `classify.html` para definir critério e reaplicar a requisição.

### 7. Dashboard de Progresso de Rotulação
- **Descrição:** página `dev-dashboard.html` mostrando quantas instâncias foram anotadas por sample e no total.
- **Prioridade:** Média  
- **Critérios de Aceitação:**  
  - Endpoint `GET /datasets/{id}/stats` com contagens de annotations.  
  - Frontend renderiza gráficos ou tabelas.

### 8. Autorização por Senha em Datasets Privados
- **Descrição:** modal de senha em `select-dataset.html` que chama `POST /datasets/{id}/verify-password`.
- **Prioridade:** Baixa  
- **Critérios de Aceitação:**  
  - Se `is_private`, exibe modal; senha correta leva ao `classify.html`, caso contrário mostra erro.

### 9. Interface de Ajuda (Tooltips)
- **Descrição:** dicas contextuais em pontos-chave da interface (campos, botões).
- **Prioridade:** Baixa  
- **Critérios de Aceitação:**  
  - Implementar tooltips via atributos `title` ou componentes Bootstrap em formulários de registro, configuração e rotulação.

### 10. Persistência de Progresso *(Implementado)*
- **Descrição:**  
  - salvar/recuperar progresso de rotulação.  
- **Prioridade:** Baixa / Média  
- **Critérios de Aceitação:**   
  - Funcionalidade de exportar/importar progresso de rotulação.

---

## Backlogs das Sprints – DataLabeler  

### Sprint 1 Backlog – Fundação e Fluxo Básico  
**Objetivo:** estabelecer upload de dataset, amostragem, rotulação simples e exportação.

1. **Registro de Datasets** (Prioridade: Alta)  
   - [Backend] `register_dataset` com parsing e criação de atributos/samples  
   - [Frontend] Form de upload em `register.html` e fetch para `/datasets/register`
   - [Testes] Unit tests para parsing de CSV/JSONL e validação de samples 

2. **Geração de Amostras Aleatórias** (Prioridade: Alta)  
   - [Backend] Lógica sem reposição em `register_dataset`
   - [Frontend] Inputs `sample_size` e `num_samples` em `register.html`   
   - [Testes] Validar ausência de índices duplicados 

3. **Rotulação Simples (1 label)** (Prioridade: Alta)  
   - [Backend] Endpoint `POST /annotations/` 
   - [Frontend] Interface de rádio buttons em `classify.html` 

4. **Exportação Básica de Dados Rotulados** (Prioridade: Alta)  
   - [Backend] Rotas de exportação CSV/JSON 
   - [Frontend] Botões “Exportar” no dashboard 

---

### Sprint 2 Backlog – Configuração e Multilabel  
**Objetivo:** permitir configuração de labels/atributos e suporte a múltiplas labels.

1. **Configuração de Labels e Atributos** (Prioridade: Alta)  
   - [Backend] `POST /datasets/{id}/configure`    
   - [Frontend] `register2.html` para marcar atributos e inserir labels 

2. **Suporte a Multiplas Labels** (Prioridade: Média)  
   - [Backend] Adaptar model e endpoint para lista de labels    
   - [Frontend] Checkboxes condicionais em `classify.html` 

3. **Preview de Amostra Antes de Rotulação** (Prioridade: Média)  
   - [Frontend] Tela de visualização dos dados amostrados 
   - [Frontend] Botões “Iniciar Rotulação” / “Gerar Nova Amostra” 

---

### Sprint 3 Backlog – Filtragem e Dashboard  
**Objetivo:** implementar filtros e oferecer painel de progresso.

1. **Filtragem de Amostras** (Prioridade: Média)  
   - [Backend] Parâmetros de filtro em `/sample_rows`
   - [Frontend] UI de filtros em `classify.html` 

2. **Dashboard de Progresso** (Prioridade: Média)  
   - [Backend] Endpoint `GET /datasets/{id}/stats`  
   - [Frontend] Gráficos/tabelas em `dev-dashboard.html`

---

### Sprint 4 Backlog – Segurança e Usabilidade  
**Objetivo:** reforçar a autorização e melhorar a usabilidade.

1. **Autorização por Senha** (Prioridade: Baixa)  
   - [Backend] `POST /datasets/{id}/verify-password` 
   - [Frontend] Modal de senha em `select-dataset.html`

2. **Interface de Ajuda (Tooltips)** (Prioridade: Baixa)  
   - [Frontend] Adicionar tooltips contextuais em formulários e botões

---

### Sprint 5 Backlog – Persistência  
**Objetivo:** consolidar métricas de concordância e permitir salvar/retomar progresso.

**Persistência de Progresso de Rotulação** (Prioridade: Média)  
   - [Backend] Save/load do estado de rotulação 
   - [Frontend] Botões “Salvar Progresso” / “Carregar Progresso”

![CERTO2UML-1](https://github.com/user-attachments/assets/95446edb-9636-4819-8f9b-094aaadc9529)



![UML datalabeler](https://github.com/user-attachments/assets/59022b61-e52f-446a-aa72-35dca73aaae6)
