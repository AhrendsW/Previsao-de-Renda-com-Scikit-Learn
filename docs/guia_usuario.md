# Guia do Usuário - Interface Streamlit

Este guia explica como utilizar a interface web Streamlit do projeto de Previsão de Renda.

## Iniciando a Interface

Para iniciar a interface Streamlit, siga os passos abaixo:

1. Certifique-se de que todas as dependências estão instaladas:
   ```bash
   pip install -r requirements.txt
   ```

2. Execute o comando:
   ```bash
   streamlit run src/ui/app.py
   ```

3. A interface será aberta automaticamente no seu navegador padrão, geralmente em:
   ```
   http://localhost:8501
   ```

## Navegando pela Interface

A interface Streamlit do projeto de Previsão de Renda possui as seguintes seções:

### 1. Página Inicial

Na página inicial, você encontrará:
- Uma breve descrição do projeto
- Informações sobre o dataset utilizado
- Estatísticas gerais sobre os dados

### 2. Análise Exploratória

Nesta seção, você pode:
- Visualizar gráficos de distribuição das variáveis
- Explorar correlações entre as características
- Analisar a distribuição da variável alvo (faixa de renda)

### 3. Previsão de Renda

Esta é a seção principal para realizar previsões:

1. **Entrada de Dados**: Preencha os campos com as informações do indivíduo:
   - Idade
   - Classe de trabalho (selecione da lista)
   - Nível educacional (selecione da lista)
   - Estado civil (selecione da lista)
   - Ocupação (selecione da lista)
   - Relacionamento (selecione da lista)
   - Raça (selecione da lista)
   - Sexo (selecione da lista)
   - Ganho de capital
   - Perda de capital
   - Horas trabalhadas por semana
   - País de origem (selecione da lista)

2. **Realizar Previsão**: Clique no botão "Prever Renda" para obter o resultado.

3. **Resultados**: A previsão será exibida, indicando:
   - A faixa de renda prevista (">50K" ou "<=50K")
   - A probabilidade da previsão
   - Um gráfico de confiança da previsão

### 4. Explicabilidade do Modelo

Nesta seção, você pode:
- Visualizar a importância das características para o modelo
- Entender como cada variável influencia a previsão
- Explorar exemplos de previsões com diferentes perfis

### 5. Sobre o Projeto

Esta seção contém:
- Informações detalhadas sobre a metodologia
- Métricas de performance dos modelos
- Links para a documentação e repositório do projeto

## Exemplos de Uso

### Exemplo 1: Previsão para um Profissional com Educação Superior

1. Preencha os campos com:
   - Idade: 45
   - Classe de trabalho: Private
   - Nível educacional: Bachelors
   - Estado civil: Married-civ-spouse
   - Ocupação: Exec-managerial
   - Relacionamento: Husband
   - Raça: White
   - Sexo: Male
   - Ganho de capital: 0
   - Perda de capital: 0
   - Horas trabalhadas por semana: 50
   - País de origem: United-States

2. Clique em "Prever Renda"

3. O resultado provavelmente indicará uma renda ">50K" com alta probabilidade.

### Exemplo 2: Previsão para um Trabalhador com Educação Básica

1. Preencha os campos com:
   - Idade: 25
   - Classe de trabalho: Private
   - Nível educacional: HS-grad
   - Estado civil: Never-married
   - Ocupação: Service
   - Relacionamento: Own-child
   - Raça: Black
   - Sexo: Male
   - Ganho de capital: 0
   - Perda de capital: 0
   - Horas trabalhadas por semana: 40
   - País de origem: United-States

2. Clique em "Prever Renda"

3. O resultado provavelmente indicará uma renda "<=50K" com alta probabilidade.

## Dicas e Solução de Problemas

- **Valores Inválidos**: Certifique-se de que todos os campos estão preenchidos corretamente.
- **Erro de Conexão**: Se a previsão falhar, verifique se a API está em execução (`uvicorn src.api.api:app`).
- **Visualizações Lentas**: Algumas visualizações podem demorar para carregar devido à quantidade de dados.
- **Responsividade**: A interface é responsiva e pode ser acessada de dispositivos móveis.

## Recursos Adicionais

- **Documentação da API**: Consulte `docs/api_reference.md` para detalhes sobre a API.
- **Arquitetura do Projeto**: Consulte `docs/arquitetura.md` para entender a estrutura do sistema.
- **Código-fonte**: Explore o diretório `src/` para ver a implementação completa. 