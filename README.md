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
git clone https://github.com/seu-usuario/previsao-de-renda-com-scikit-learn.git
cd previsao-de-renda-com-scikit-learn
```

2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

3. Execute o pipeline completo ou cada etapa individualmente:

### Pipeline Completo
```bash
# Instalar o pacote em modo de desenvolvimento
pip install -e .

# Executar o pipeline completo
python src/data/data_acquisition.py
python src/data/preprocessamento.py
python src/data/feature_engineering.py
python src/models/modelagem.py
```

### Executar a API
```bash
uvicorn src.api.api:app --reload
```

### Executar a Interface Web
```bash
streamlit run src.ui.app
```

## 📊 Dataset

O projeto utiliza o dataset Adult Income do UCI Machine Learning Repository, que contém informações sobre:
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

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
