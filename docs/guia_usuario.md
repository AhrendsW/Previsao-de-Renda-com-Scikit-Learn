# Guia do Usuário - Interface Streamlit

Este guia explica como utilizar a interface web Streamlit do projeto de Previsão de Renda.

## Iniciando a Interface

Para utilizar o sistema completo, você precisará executar tanto a API quanto a interface Streamlit. Como cada um ocupa um terminal, siga um dos métodos abaixo:

### Método 1: Usando o Script Automatizado

A maneira mais simples é usar o script `run_all.py` que inicia ambos os serviços automaticamente:

```bash
# Certifique-se de que o ambiente virtual está ativado
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Execute o script
python run_all.py
```

Isso abrirá dois terminais separados, um para a API e outro para o Streamlit.

### Método 2: Execução Manual em Terminais Separados

Se preferir iniciar manualmente:

**Terminal 1 - API:**
```bash
# Ative o ambiente virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Execute a API
uvicorn src.api.api:app --reload
```

**Terminal 2 - Interface Streamlit:**
```bash
# Ative o ambiente virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Execute o Streamlit
streamlit run src/ui/app.py
```

A interface será aberta automaticamente no seu navegador padrão, geralmente em:
```
http://localhost:8501
```

A API estará disponível em:
```
http://localhost:8000
```

### Como Parar a Aplicação

Quando terminar de usar a aplicação, você pode pará-la seguindo estas instruções:

#### Parando o Script Automatizado (Método 1)
Se você iniciou a aplicação usando o script `run_all.py`:

1. Feche manualmente as janelas dos terminais abertos pelo script, ou
2. Em cada terminal, pressione `Ctrl+C` para interromper o processo correspondente.

#### Parando a Execução Manual (Método 2)
Se você iniciou a API e o Streamlit manualmente em terminais separados:

Em cada terminal onde a API ou o Streamlit estão rodando, pressione `Ctrl+C` para interromper o processo.

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
   - Tipo de Trabalho (selecione da lista)
   - Escolaridade (selecione da lista)
   - Estado Civil (selecione da lista)
   - Área de Atuação (selecione da lista)
   - Situação Familiar (selecione da lista)
   - Como você se identifica (etnia)
   - Sexo (selecione da lista)
   - Rendimentos Extras (Anual)
   - Perdas Financeiras (Anual)
   - Horas por Semana
   - País de Origem (selecione da lista)

2. **Realizar Previsão**: Clique no botão "Calcular Minha Renda" para obter o resultado.

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
   - Tipo de Trabalho: Empresa Privada
   - Escolaridade: Superior Completo
   - Estado Civil: Casado(a)
   - Área de Atuação: Gerente/Diretor
   - Situação Familiar: Chefe de Família
   - Como você se identifica: Branca
   - Sexo: Masculino
   - Rendimentos Extras (Anual): 0
   - Perdas Financeiras (Anual): 0
   - Horas por Semana: 50
   - País de Origem: Brasil

2. Clique em "Calcular Minha Renda"

3. O resultado provavelmente indicará uma renda ">50K" com alta probabilidade.

### Exemplo 2: Previsão para um Trabalhador com Educação Básica

1. Preencha os campos com:
   - Idade: 25
   - Tipo de Trabalho: Empresa Privada
   - Escolaridade: Ensino Médio Completo
   - Estado Civil: Solteiro(a)
   - Área de Atuação: Prestador de Serviços
   - Situação Familiar: Filho(a)
   - Como você se identifica: Preta
   - Sexo: Masculino
   - Rendimentos Extras (Anual): 0
   - Perdas Financeiras (Anual): 0
   - Horas por Semana: 40
   - País de Origem: Brasil

2. Clique em "Calcular Minha Renda"

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