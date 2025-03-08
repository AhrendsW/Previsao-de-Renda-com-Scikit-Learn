# Arquitetura do Projeto de Previsão de Renda

Este documento descreve a arquitetura e os componentes principais do sistema de previsão de renda.

## Visão Geral

O projeto segue uma arquitetura modular, com componentes separados para cada etapa do pipeline de machine learning:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │     │                 │
│  Aquisição de   │────▶│     Pré-        │────▶│    Feature      │────▶│   Modelagem     │
│     Dados       │     │  processamento  │     │  Engineering    │     │                 │
│                 │     │                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
                                                                               │
                                                                               │
                                                                               ▼
┌─────────────────┐     ┌─────────────────┐                         ┌─────────────────┐
│                 │     │                 │                         │                 │
│   Interface     │◀────│      API        │◀────────────────────────│   Avaliação    │
│   Streamlit     │     │    FastAPI      │                         │   de Modelos   │
│                 │     │                 │                         │                 │
└─────────────────┘     └─────────────────┘                         └─────────────────┘
```

## Componentes Principais

### 1. Aquisição de Dados (`src/data/data_acquisition.py`)

Responsável por:
- Importar o dataset Adult Income do UCI ML Repository
- Realizar validações iniciais
- Salvar os dados brutos para processamento

### 2. Pré-processamento (`src/data/preprocessamento.py`)

Responsável por:
- Tratamento de valores ausentes
- Codificação de variáveis categóricas
- Normalização de variáveis numéricas
- Divisão em conjuntos de treino e teste
- Salvar os dados processados e transformadores

### 3. Feature Engineering (`src/data/feature_engineering.py`)

Responsável por:
- Criação de novas características
- Seleção de características relevantes
- Transformações avançadas nos dados
- Salvar os dados com features engenheiradas

### 4. Modelagem (`src/models/modelagem.py`)

Responsável por:
- Treinamento de diferentes algoritmos
- Otimização de hiperparâmetros
- Avaliação de performance
- Serialização do melhor modelo

### 5. API (`src/api/api.py`)

Responsável por:
- Carregar o modelo treinado
- Expor endpoints para previsões
- Validar entradas
- Processar requisições e retornar previsões

### 6. Interface Web (`src/ui/app.py`)

Responsável por:
- Fornecer uma interface amigável para usuários
- Permitir entrada de dados para previsão
- Visualizar resultados e explicações
- Comunicar-se com a API

## Fluxo de Dados

1. Os dados brutos são obtidos do UCI ML Repository
2. Os dados são pré-processados e transformados
3. Features adicionais são criadas
4. Modelos são treinados com os dados processados
5. O melhor modelo é serializado e disponibilizado
6. A API carrega o modelo e os transformadores
7. A interface web se comunica com a API para obter previsões

## Dependências Externas

- **pandas/numpy**: Manipulação de dados
- **scikit-learn**: Algoritmos de ML e métricas
- **FastAPI**: Framework para API
- **Streamlit**: Framework para interface web
- **joblib**: Serialização de objetos Python

## Armazenamento de Dados

- **Dados processados**: Armazenados em CSV no diretório `data/`
- **Modelos treinados**: Serializados com joblib no diretório `models/`
- **Transformadores**: Serializados com joblib no diretório `data/`
- **Visualizações**: Salvas como PNG no diretório `visualizacoes/`
- **Logs**: Armazenados em arquivos de texto no diretório `logs/` 