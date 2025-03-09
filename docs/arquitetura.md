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

### 5. Avaliação de Modelos

Responsável por:
- Cálculo de métricas de performance
- Geração de visualizações para análise
- Comparação entre diferentes modelos
- Seleção do melhor modelo

#### Métricas Implementadas

```python
def avaliar_modelo(y_true, y_pred, y_proba):
    """Calcula métricas de avaliação para o modelo."""
    metricas = {
        'accuracy': accuracy_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred),
        'roc_auc': roc_auc_score(y_true, y_proba)
    }
    return metricas
```

#### Visualizações

```python
def plotar_matriz_confusao(y_true, y_pred, nome_modelo):
    """Plota e salva a matriz de confusão."""
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['<=50K', '>50K'],
                yticklabels=['<=50K', '>50K'])
    plt.savefig(f'models/confusion_matrix_{nome_modelo}.png')
```

#### Processo de Seleção

O melhor modelo é selecionado com base em:
1. Performance no conjunto de teste (F1-Score como métrica principal)
2. Robustez (avaliada via validação cruzada)
3. Tempo de inferência
4. Interpretabilidade dos resultados

### 6. API (`src/api/api.py`)

Responsável por:
- Carregar o modelo treinado
- Expor endpoints para previsões
- Validar entradas
- Processar requisições e retornar previsões

### 7. Interface Web (`src/ui/app.py`)

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

## Oportunidades de Evolução Arquitetural

Esta seção descreve possíveis evoluções técnicas para o projeto, detalhando como implementar as melhorias mencionadas no README principal.

### 1. Arquitetura para Deploy em Produção

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│    Docker       │────▶│   Plataforma    │────▶│   Balanceador   │
│   Container     │     │     Cloud       │     │    de Carga     │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Monitoramento  │◀────│   Autenticação  │◀────│    API em       │
│                 │     │    & Segurança  │     │   Produção      │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

#### Implementação Técnica:

1. **Containerização**:
   - Criar `Dockerfile` na raiz do projeto
   - Configurar `docker-compose.yml` para orquestrar API e banco de dados
   - Implementar multi-stage builds para otimizar tamanho da imagem

2. **CI/CD Pipeline**:
   - Configurar GitHub Actions ou GitLab CI
   - Implementar testes automatizados antes do deploy
   - Configurar deploy automático para ambiente de staging e produção

3. **Segurança**:
   - Implementar autenticação JWT ou OAuth2 na API
   - Configurar HTTPS com certificados válidos
   - Implementar rate limiting para prevenir ataques de força bruta

### 2. Arquitetura para Modelos Avançados

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Preprocessador │────▶│  Feature Store  │────▶│  Orquestrador   │
│                 │     │                 │     │   de Modelos    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Explicabilidade│◀────│   Ensemble de   │◀────│  Modelos Deep   │
│     (SHAP)      │     │     Modelos     │     │    Learning     │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

#### Implementação Técnica:

1. **Deep Learning**:
   - Implementar redes neurais usando TensorFlow ou PyTorch
   - Criar camadas de embedding para variáveis categóricas
   - Utilizar técnicas de regularização como Dropout e BatchNorm

2. **Ensemble Avançado**:
   - Implementar Stacking com scikit-learn `StackingClassifier`
   - Utilizar diferentes modelos base (XGBoost, LightGBM, CatBoost)
   - Implementar validação cruzada para evitar overfitting

3. **Explicabilidade**:
   - Integrar biblioteca SHAP para explicações locais e globais
   - Implementar gráficos de dependência parcial
   - Criar dashboard de explicabilidade para usuários finais

### 3. Arquitetura para Dados Atualizados

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Fontes de      │────▶│  Pipeline ETL   │────▶│  Data Warehouse │
│    Dados        │     │   (Airflow)     │     │                 │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Monitoramento  │◀────│  Retreinamento  │◀────│  Feature Store  │
│    de Drift     │     │   Automático    │     │                 │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

#### Implementação Técnica:

1. **Pipeline ETL**:
   - Implementar Apache Airflow para orquestração
   - Criar DAGs para extração periódica de dados
   - Implementar validações de qualidade de dados

2. **Feature Store**:
   - Utilizar ferramentas como Feast ou Hopsworks
   - Implementar versionamento de features
   - Configurar cache para features frequentemente utilizadas

3. **Monitoramento de Drift**:
   - Implementar métricas de detecção de data drift
   - Configurar alertas para degradação de performance
   - Criar dashboard de monitoramento em tempo real

### 4. Arquitetura para Interface Avançada

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Streamlit      │────▶│  API Gateway    │────▶│  Serviço de     │
│  Cloud          │     │                 │     │  Autenticação   │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Armazenamento  │◀────│  Serviço de     │◀────│  API de         │
│  de Perfis      │     │  Personalização │     │  Previsão       │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

#### Implementação Técnica:

1. **Deploy Streamlit**:
   - Configurar conta no Streamlit Cloud
   - Implementar secrets management para credenciais
   - Configurar GitHub Actions para deploy automático

2. **Personalização**:
   - Implementar banco de dados para armazenar perfis de usuários
   - Criar sistema de autenticação leve
   - Desenvolver funcionalidade de comparação de cenários

3. **Otimização Mobile**:
   - Implementar layout responsivo com st.columns
   - Otimizar tamanho de imagens e gráficos
   - Testar em diferentes dispositivos e navegadores 