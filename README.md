# 🎯 Previsão de Renda com Machine Learning

Este projeto tem como objetivo criar um modelo preditivo para estimar a faixa de renda de indivíduos com base em características socioeconômicas, utilizando técnicas de Machine Learning.

Desenvolvido com Python 3.9.5 e bibliotecas modernas de ciência de dados, este projeto implementa um pipeline completo de machine learning, desde a aquisição dos dados até o deploy de uma API para disponibilizar as previsões.

## 📋 Estrutura do Projeto

```
.
├── data/                # Dados processados e transformadores
├── logs/                # Logs de execução do sistema
├── models/              # Modelos treinados e métricas
├── src/                 # Código-fonte do projeto
│   ├── api/             # API FastAPI para servir o modelo
│   ├── data/            # Scripts de processamento de dados
│   ├── models/          # Treinamento e avaliação de modelos
│   ├── ui/              # Interface Streamlit
│   └── utils/           # Funções auxiliares
├── tests/               # Testes unitários e de integração
└── visualizacoes/       # Gráficos e visualizações geradas
```

## 🚀 Como Começar

1. Clone o repositório:
```bash
git clone https://github.com/AhrendsW/Previsao-de-Renda-com-Scikit-Learn.git
cd Previsao-de-Renda-com-Scikit-Learn
```

2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

3. Instale o pacote em modo de desenvolvimento:
```bash
pip install -e .
```

4. Execute o pipeline completo ou cada etapa individualmente:

### Pipeline Completo
```bash
python src/data/data_acquisition.py
python src/data/preprocessamento.py
python src/data/feature_engineering.py
python src/models/modelagem.py
```

### Executar a API e a Interface Web

Para utilizar o sistema completo, você precisará executar tanto a API quanto a interface Streamlit. Como cada um ocupa um terminal, siga um dos métodos abaixo:

#### Método 1: Usando Terminais Separados

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

#### Método 2: Usando Processos em Background (Windows)

```bash
# Inicie a API em background
start cmd /k ".venv\\Scripts\\activate && uvicorn src.api.api:app --reload"

# Inicie o Streamlit no terminal atual
.venv\Scripts\activate && streamlit run src/ui/app.py
```

#### Método 3: Usando Processos em Background (Linux/Mac)

```bash
# Inicie a API em background
source .venv/bin/activate && uvicorn src.api.api:app --reload &

# Inicie o Streamlit no terminal atual
source .venv/bin/activate && streamlit run src/ui/app.py
```

#### Método 4: Usando o Script Automatizado

O projeto já inclui um arquivo `run_all.py` na raiz que inicia automaticamente tanto a API quanto o Streamlit em terminais separados. Para utilizá-lo:

```bash
# Certifique-se de que o ambiente virtual está ativado
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Execute o script
python run_all.py
```

Este script abrirá dois terminais separados, um para a API e outro para o Streamlit, e exibirá as URLs onde cada serviço estará disponível.

### Como Parar a Aplicação

Dependendo do método que você utilizou para iniciar a aplicação, existem diferentes formas de pará-la:

#### Parando Terminais Separados (Método 1)
Em cada terminal onde a API ou o Streamlit estão rodando:
```bash
# Pressione a combinação de teclas
Ctrl+C
```

#### Parando Processos em Background no Windows (Método 2)
Para parar a API rodando em background:
```bash
# No terminal onde você iniciou o processo
taskkill /F /IM cmd.exe /T
```
Ou feche manualmente a janela do terminal onde a API está rodando.

#### Parando Processos em Background no Linux/Mac (Método 3)
Para parar a API rodando em background:
```bash
# Encontre o PID do processo uvicorn
ps aux | grep uvicorn

# Mate o processo usando o PID encontrado
kill -9 <PID>
```

Para o Streamlit, pressione `Ctrl+C` no terminal onde ele está rodando.

#### Parando o Script Automatizado (Método 4)
Quando você usa o script `run_all.py`, ele abre terminais separados. Para parar:

1. Feche manualmente as janelas dos terminais abertos pelo script, ou
2. Em cada terminal, pressione `Ctrl+C` para interromper o processo correspondente.

## 📊 Dataset

O projeto utiliza o dataset Adult Income do UCI Machine Learning Repository, disponível em: [https://archive.ics.uci.edu/dataset/2/adult](https://archive.ics.uci.edu/dataset/2/adult)

Este dataset contém informações sobre:
- Características demográficas (idade, sexo, raça)
- Nível educacional
- Ocupação e classe de trabalho
- Estado civil e relacionamentos
- Horas trabalhadas por semana
- Ganhos e perdas de capital
- País de origem

O objetivo é prever se a renda anual de um indivíduo é superior a $50K.

## 🧪 Fluxo de Trabalho

1. **Aquisição de Dados**: Importação do dataset do UCI ML Repository usando a biblioteca `ucimlrepo`.
2. **Pré-processamento**: Tratamento de valores ausentes, codificação de variáveis categóricas e normalização.
3. **Feature Engineering**: Criação de novas características e seleção das mais relevantes.
4. **Modelagem**: Treinamento e otimização de diferentes algoritmos (Regressão Logística, Random Forest, XGBoost).
5. **Avaliação**: Análise de métricas como acurácia, precisão, recall, F1-score e matriz de confusão.
6. **Deploy**: Disponibilização do modelo através de uma API FastAPI e interface Streamlit.

## 📈 Modelos Implementados

- **Regressão Logística**: Modelo base para classificação binária.
- **Random Forest**: Ensemble de árvores de decisão para capturar relações não-lineares.
- **XGBoost**: Algoritmo de gradient boosting otimizado para performance.

Os resultados comparativos dos modelos estão disponíveis no diretório `models/`.

## 📊 Métricas de Avaliação

Para avaliar a performance dos modelos, utilizamos as seguintes métricas:

### Métricas Principais

- **Acurácia**: Proporção de previsões corretas em relação ao total de amostras.
- **F1-Score**: Média harmônica entre precisão e recall, equilibrando falsos positivos e falsos negativos.
- **ROC-AUC**: Área sob a curva ROC, medindo a capacidade do modelo de distinguir entre as classes.

### Visualizações de Performance

- **Matriz de Confusão**: Visualização que mostra a distribuição de previsões corretas e incorretas para cada classe.
- **Curva ROC**: Gráfico que ilustra a performance do modelo em diferentes limiares de classificação.
- **Importância das Features**: Ranking das características mais relevantes para as previsões do modelo.

### Resultados Obtidos

Os modelos treinados alcançaram as seguintes performances no conjunto de teste:

| Modelo                    | Acurácia | F1-Score | ROC-AUC |
|---------------------------|----------|----------|---------|
| Regressão Logística       | 0.827    | 0.587    | 0.878   |
| XGBoost                   | 0.831    | 0.613    | 0.882   |
| Regressão Logística (otim)| 0.827    | 0.587    | 0.878   |
| XGBoost (otimizado)       | 0.837    | 0.621    | 0.887   |

O modelo XGBoost otimizado foi selecionado como o melhor modelo devido à sua performance superior em todas as métricas avaliadas.

## 🛠️ Tecnologias Utilizadas

- **Python 3.9.5**: Linguagem de programação principal
- **pandas (2.1.0)** e **numpy (1.24.3)**: Manipulação e processamento de dados
- **scikit-learn (1.3.0)**: Implementação de modelos de machine learning
- **matplotlib (3.7.2)** e **seaborn (0.12.2)**: Visualização de dados
- **FastAPI (0.104.1)** e **uvicorn (0.24.0)**: Desenvolvimento da API
- **Streamlit (1.28.0)**: Interface web interativa
- **joblib (1.3.2)**: Serialização de modelos e transformadores

## 🧪 Testes

Para testar a API localmente:
```bash
# Inicie a API em um terminal
uvicorn src.api.api:app --reload

# Em outro terminal, execute o script de teste
python test_api.py
```

## 📝 Logs

Os logs do sistema são armazenados no diretório `logs/` e incluem:
- Informações sobre o carregamento dos dados
- Estatísticas do dataset
- Alertas sobre valores nulos ou inconsistências
- Métricas de performance dos modelos
- Erros e exceções

## 👥 Contribuição

Para contribuir com o projeto:
1. Faça um Fork
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 🚀 Próximos Passos

Este projeto pode ser expandido e melhorado de várias maneiras. Abaixo estão algumas sugestões para trabalhos futuros:

### 1. Deploy da API em Ambiente de Produção

- **Containerização com Docker**: Criar um Dockerfile para empacotar a API e suas dependências
- **Deploy em Plataformas Cloud**:
  - AWS Elastic Beanstalk ou Lambda para serverless
  - Google Cloud Run ou App Engine
  - Azure App Service
  - Heroku ou Render para soluções mais simples
- **Configuração de CI/CD**: Implementar pipeline de integração e deploy contínuos
- **Autenticação e Segurança**: Adicionar camadas de autenticação (JWT, OAuth) e proteção contra ataques

### 2. Deploy da Interface Streamlit

- **Streamlit Cloud**: Hospedar a interface na plataforma Streamlit Cloud
- **Hugging Face Spaces**: Alternativa para deploy gratuito
- **Integração com Domínio Personalizado**: Configurar um domínio próprio para a aplicação
- **Otimização de Performance**: Melhorar o tempo de carregamento e responsividade

### 3. Exploração de Modelos Avançados

- **Deep Learning**: Implementar redes neurais com TensorFlow ou PyTorch
- **Modelos de Ensemble Avançados**: Stacking ou Blending de múltiplos modelos
- **AutoML**: Explorar frameworks como AutoGluon, TPOT ou Auto-Sklearn
- **Modelos Interpretáveis**: Implementar modelos mais interpretáveis como RuleFit ou SHAP

### 4. Atualização e Expansão dos Dados

- **Dados Mais Recentes**: Buscar fontes de dados atualizadas sobre renda e características socioeconômicas
- **Enriquecimento com Fontes Adicionais**: Combinar com outros datasets para obter mais features
- **Dados Brasileiros**: Adaptar o modelo para o contexto brasileiro usando dados do IBGE ou PNAD
- **Coleta Contínua**: Implementar um sistema para atualização periódica dos dados

### 5. Melhorias na Experiência do Usuário

- **Dashboard Interativo**: Expandir a interface com visualizações mais ricas e interativas
- **Explicabilidade**: Adicionar explicações detalhadas sobre as previsões (LIME, SHAP)
- **Personalização**: Permitir que usuários salvem perfis e comparem diferentes cenários
- **Versão Mobile**: Otimizar a interface para dispositivos móveis

### 6. Monitoramento e Manutenção

- **Monitoramento de Drift**: Implementar detecção de data drift e model drift
- **Logging Avançado**: Integrar com ferramentas como ELK Stack ou Prometheus
- **Retreinamento Automático**: Sistema para retreinar o modelo periodicamente
- **Testes A/B**: Comparar performance de diferentes versões do modelo em produção

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
