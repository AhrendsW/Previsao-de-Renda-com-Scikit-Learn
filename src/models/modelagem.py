"""
Módulo responsável pela modelagem e avaliação dos modelos.
Implementa diferentes algoritmos e técnicas de avaliação.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    confusion_matrix
)
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils.logger import configurar_logger
import os
import sys
import logging

logger = configurar_logger('modelagem')
logger.setLevel(logging.DEBUG)

def carregar_dados() -> Tuple[pd.DataFrame, pd.Series]:
    """
    Carrega os dados processados para modelagem.
    
    Returns:
        Tuple com features e target
    """
    logger.debug("Iniciando carregamento dos dados...")
    
    try:
        logger.debug("Tentando ler features_engineered.csv...")
        X = pd.read_csv('data/features_engineered.csv')
        logger.debug(f"Features carregadas com sucesso. Shape: {X.shape}")
        
        logger.debug("Tentando ler target.csv...")
        y = pd.read_csv('data/target.csv')
        logger.debug(f"Target carregado com sucesso. Shape: {y.shape}")
        
        logger.debug("Convertendo target para valores numéricos...")
        y = y['income'].map({'<=50K': 0, '>50K': 1, '<=50K.': 0, '>50K.': 1})
        logger.debug("Conversão do target concluída")
        
        logger.info(f"Dados carregados - Shape X: {X.shape}, Shape y: {y.shape}")
        return X, y
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {str(e)}")
        logger.error(f"Traceback completo: {sys.exc_info()}")
        raise

def criar_diretorio_modelos():
    """
    Cria o diretório para salvar os modelos se não existir.
    """
    if not os.path.exists('models'):
        os.makedirs('models')
        logger.info("Diretório de modelos criado")

def dividir_dados(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Divide os dados em treino e teste.
    
    Args:
        X: Features
        y: Target
        test_size: Proporção do conjunto de teste
        random_state: Semente aleatória
        
    Returns:
        Tuple com X_train, X_test, y_train, y_test
    """
    logger.info("Dividindo dados em treino e teste...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
    
    logger.info(f"Shape treino: {X_train.shape}, Shape teste: {X_test.shape}")
    return X_train, X_test, y_train, y_test

def avaliar_modelo(
    y_true: pd.Series,
    y_pred: np.ndarray,
    y_proba: np.ndarray = None
) -> Dict[str, float]:
    """
    Calcula métricas de avaliação do modelo.
    
    Args:
        y_true: Valores reais
        y_pred: Valores preditos
        y_proba: Probabilidades preditas (opcional)
        
    Returns:
        Dicionário com as métricas
    """
    metricas = {
        'accuracy': accuracy_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred)
    }
    
    if y_proba is not None:
        metricas['roc_auc'] = roc_auc_score(y_true, y_proba)
    
    return metricas

def plotar_matriz_confusao(
    y_true: pd.Series,
    y_pred: np.ndarray,
    nome_modelo: str
):
    """
    Plota e salva a matriz de confusão.
    
    Args:
        y_true: Valores reais
        y_pred: Valores preditos
        nome_modelo: Nome do modelo para o título
    """
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_true, y_pred)
    
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=['<=50K', '>50K'],
        yticklabels=['<=50K', '>50K']
    )
    
    plt.title(f'Matriz de Confusão - {nome_modelo}')
    plt.ylabel('Real')
    plt.xlabel('Predito')
    
    plt.savefig(f'models/confusion_matrix_{nome_modelo.lower()}.png')
    plt.close()

def treinar_modelo_base(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    modelo: Any,
    nome_modelo: str
) -> Tuple[Any, Dict[str, float]]:
    """
    Treina e avalia um modelo base.
    
    Args:
        X_train: Features de treino
        y_train: Target de treino
        X_test: Features de teste
        y_test: Target de teste
        modelo: Modelo a ser treinado
        nome_modelo: Nome do modelo
        
    Returns:
        Tuple com o modelo treinado e suas métricas
    """
    logger.info(f"Treinando modelo base: {nome_modelo}")
    
    modelo.fit(X_train, y_train)
    
    y_pred = modelo.predict(X_test)
    y_proba = modelo.predict_proba(X_test)[:, 1]
    
    metricas = avaliar_modelo(y_test, y_pred, y_proba)
    
    plotar_matriz_confusao(y_test, y_pred, nome_modelo)
    
    logger.info(f"Métricas {nome_modelo}:")
    for metrica, valor in metricas.items():
        logger.info(f"- {metrica}: {valor:.4f}")
    
    return modelo, metricas

def otimizar_modelo(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    modelo: Any,
    param_grid: Dict[str, List[Any]],
    nome_modelo: str,
    cv: int = 5
) -> Tuple[Any, Dict[str, Any]]:
    """
    Otimiza hiperparâmetros do modelo usando GridSearchCV.
    
    Args:
        X_train: Features de treino
        y_train: Target de treino
        modelo: Modelo base
        param_grid: Grid de parâmetros
        nome_modelo: Nome do modelo
        cv: Número de folds para validação cruzada
        
    Returns:
        Tuple com melhor modelo e seus parâmetros
    """
    logger.info(f"Otimizando hiperparâmetros: {nome_modelo}")
    
    grid_search = GridSearchCV(
        modelo,
        param_grid,
        cv=cv,
        scoring='f1',
        n_jobs=-1
    )
    
    grid_search.fit(X_train, y_train)
    
    logger.info(f"Melhores parâmetros para {nome_modelo}:")
    for param, valor in grid_search.best_params_.items():
        logger.info(f"- {param}: {valor}")
    
    logger.info(f"Melhor score: {grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_, grid_search.best_params_

def main():
    """
    Função principal para executar a modelagem.
    """
    logger.info("Iniciando processo de modelagem...")
    
    try:
        logger.debug("Chamando função carregar_dados()...")
        X, y = carregar_dados()
        logger.debug("Dados carregados com sucesso")
        
        logger.debug("Criando diretório de modelos...")
        criar_diretorio_modelos()
        logger.debug("Diretório de modelos verificado/criado")
        
        logger.debug("Dividindo dados em treino e teste...")
        X_train, X_test, y_train, y_test = dividir_dados(X, y)
        logger.debug("Dados divididos com sucesso")
        
        logger.debug("Definindo modelos base...")
        modelos_base = {
            'Logistic Regression': LogisticRegression(max_iter=1000),
            'XGBoost': xgb.XGBClassifier()
        }
        logger.debug("Modelos base definidos")
        
        resultados = {}
        modelos_treinados = {}
        
        for nome, modelo in modelos_base.items():
            logger.info(f"\nIniciando treinamento do modelo base: {nome}")
            modelo_treinado, metricas = treinar_modelo_base(
                X_train, y_train,
                X_test, y_test,
                modelo, nome
            )
            resultados[nome] = metricas
            modelos_treinados[nome] = modelo_treinado
            logger.info(f"Treinamento do modelo {nome} concluído")
        
        df_resultados = pd.DataFrame(resultados).T
        logger.info("\nComparativo de modelos:")
        logger.info("\n" + str(df_resultados))
        
        param_grids = {
            'Logistic Regression': {
                'C': [0.001, 0.01, 0.1, 1.0, 10.0],
                'penalty': ['l1', 'l2'],
                'solver': ['liblinear', 'saga']
            },
            'XGBoost': {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1],
                'min_child_weight': [1, 3, 5],
                'subsample': [0.8, 0.9, 1.0]
            }
        }
        
        modelos_otimizados = {}
        for nome, modelo in modelos_treinados.items():
            logger.info(f"\nOtimizando {nome}...")
            melhor_modelo, melhores_params = otimizar_modelo(
                X_train, y_train,
                modelo,
                param_grids[nome],
                nome
            )
            modelos_otimizados[nome] = melhor_modelo
            logger.info(f"Otimização do modelo {nome} concluída")
        
        resultados_otimizados = {}
        for nome, modelo in modelos_otimizados.items():
            logger.info(f"\nAvaliando modelo otimizado: {nome}")
            y_pred = modelo.predict(X_test)
            y_proba = modelo.predict_proba(X_test)[:, 1]
            metricas = avaliar_modelo(y_test, y_pred, y_proba)
            resultados_otimizados[nome] = metricas
            
            plotar_matriz_confusao(y_test, y_pred, f"{nome}_otimizado")
            logger.info(f"Avaliação do modelo otimizado {nome} concluída")
        
        df_resultados_finais = pd.DataFrame({
            **resultados,
            **{f"{k}_otimizado": v for k, v in resultados_otimizados.items()}
        }).T
        
        logger.info("\nResultados finais:")
        logger.info("\n" + str(df_resultados_finais))
        
        melhor_modelo_nome = df_resultados_finais['f1'].idxmax()
        melhor_modelo = (
            modelos_otimizados.get(melhor_modelo_nome.replace('_otimizado', ''))
            if '_otimizado' in melhor_modelo_nome
            else modelos_treinados[melhor_modelo_nome]
        )
        
        logger.info(f"\nMelhor modelo: {melhor_modelo_nome}")
        logger.info("Salvando melhor modelo...")
        
        joblib.dump(melhor_modelo, 'models/melhor_modelo.joblib')
        df_resultados_finais.to_csv('models/resultados_modelos.csv')
        
        logger.info("Processo de modelagem concluído com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro durante a modelagem: {str(e)}")
        logger.error(f"Traceback completo: {sys.exc_info()}")
        raise

if __name__ == "__main__":
    main()