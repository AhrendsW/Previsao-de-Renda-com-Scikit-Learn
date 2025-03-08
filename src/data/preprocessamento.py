"""
Módulo responsável pelo pré-processamento dos dados.
Realiza limpeza, transformação e preparação das features para modelagem.
"""

import pandas as pd
from typing import Tuple, Dict, Any
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from src.utils.logger import configurar_logger

logger = configurar_logger('preprocessamento')

def remover_valores_nulos(
    X: pd.DataFrame,
    estrategia: Dict[str, str]
) -> pd.DataFrame:
    """
    Remove ou imputa valores nulos no DataFrame.
    
    Args:
        X: DataFrame com as features
        estrategia: Dicionário com a estratégia de imputação para cada coluna
                   Exemplo: {'coluna1': 'mean', 'coluna2': 'most_frequent'}
    
    Returns:
        DataFrame com valores nulos tratados
    """
    logger.info("Iniciando tratamento de valores nulos...")
    X_limpo = X.copy()
    
    try:
        for coluna, metodo in estrategia.items():
            if coluna in X_limpo.columns:
                logger.info(f"Tratando valores nulos em {coluna} usando {metodo}")
                
                if X_limpo[coluna].dtype in ['int64', 'float64']:
                    imputer = SimpleImputer(strategy=metodo)
                else:
                    imputer = SimpleImputer(strategy='most_frequent')
                
                valores_antes = X_limpo[coluna].isnull().sum()
                X_limpo.loc[:, coluna] = imputer.fit_transform(X_limpo[[coluna]]).ravel()
                valores_depois = X_limpo[coluna].isnull().sum()
                
                logger.info(f"Valores nulos em {coluna}: {valores_antes} -> {valores_depois}")
                
    except Exception as e:
        logger.error(f"Erro ao tratar valores nulos: {str(e)}")
        raise
            
    return X_limpo

def tratar_outliers(
    X: pd.DataFrame,
    colunas_numericas: list,
    metodo: str = 'iqr',
    limite: float = 1.5
) -> pd.DataFrame:
    """
    Trata outliers nas colunas numéricas especificadas.
    
    Args:
        X: DataFrame com as features
        colunas_numericas: Lista de colunas numéricas para tratar outliers
        metodo: 'iqr' para Interquartile Range ou 'zscore' para Z-Score
        limite: Limite para considerar outlier (1.5 para IQR, 3 para Z-Score)
    
    Returns:
        DataFrame com outliers tratados
    """
    logger.info(f"Iniciando tratamento de outliers usando método: {metodo}")
    X_limpo = X.copy()
    
    try:
        for coluna in colunas_numericas:
            if coluna not in X_limpo.columns:
                logger.warning(f"Coluna {coluna} não encontrada no DataFrame")
                continue
                
            logger.info(f"Tratando outliers em {coluna}")
            valores_antes = len(X_limpo)
            
            if metodo == 'iqr':
                Q1 = X_limpo[coluna].quantile(0.25)
                Q3 = X_limpo[coluna].quantile(0.75)
                IQR = Q3 - Q1
                
                limite_inferior = Q1 - limite * IQR
                limite_superior = Q3 + limite * IQR
                
                X_limpo[coluna] = X_limpo[coluna].clip(limite_inferior, limite_superior)
                
            elif metodo == 'zscore':
                mean = X_limpo[coluna].mean()
                std = X_limpo[coluna].std()
                
                X_limpo[coluna] = X_limpo[coluna].clip(
                    mean - limite * std,
                    mean + limite * std
                )
                
            valores_alterados = (X_limpo[coluna] != X[coluna]).sum()
            logger.info(f"Valores modificados em {coluna}: {valores_alterados}")
            
    except Exception as e:
        logger.error(f"Erro ao tratar outliers: {str(e)}")
        raise
            
    return X_limpo

def normalizar_features(
    X: pd.DataFrame,
    colunas_numericas: list
) -> Tuple[pd.DataFrame, StandardScaler]:
    """
    Normaliza as features numéricas usando StandardScaler.
    
    Args:
        X: DataFrame com as features
        colunas_numericas: Lista de colunas numéricas para normalizar
        
    Returns:
        Tuple com:
        - DataFrame com features normalizadas
        - Objeto StandardScaler ajustado
    """
    logger.info("Iniciando normalização das features...")
    X_norm = X.copy()
    
    try:
        colunas_faltantes = [col for col in colunas_numericas if col not in X_norm.columns]
        if colunas_faltantes:
            raise ValueError(f"Colunas não encontradas: {colunas_faltantes}")
        
        scaler = StandardScaler()
        X_norm[colunas_numericas] = scaler.fit_transform(X[colunas_numericas])
        
        for coluna in colunas_numericas:
            media = X_norm[coluna].mean()
            std = X_norm[coluna].std()
            logger.info(f"Coluna {coluna} normalizada - Média: {media:.2f}, Desvio Padrão: {std:.2f}")
        
    except Exception as e:
        logger.error(f"Erro ao normalizar features: {str(e)}")
        raise
    
    return X_norm, scaler

def codificar_categoricas(
    X: pd.DataFrame,
    colunas_categoricas: list
) -> Tuple[pd.DataFrame, Dict[str, LabelEncoder]]:
    """
    Codifica variáveis categóricas usando LabelEncoder.
    
    Args:
        X: DataFrame com as features
        colunas_categoricas: Lista de colunas categóricas para codificar
        
    Returns:
        Tuple com:
        - DataFrame com variáveis codificadas
        - Dicionário com os LabelEncoders ajustados
    """
    logger.info("Iniciando codificação de variáveis categóricas...")
    X_cod = X.copy()
    encoders = {}
    
    try:
        for coluna in colunas_categoricas:
            if coluna not in X_cod.columns:
                logger.warning(f"Coluna {coluna} não encontrada no DataFrame")
                continue
                
            logger.info(f"Codificando coluna: {coluna}")
            
            X_cod[coluna] = X_cod[coluna].fillna('MISSING')
            X_cod[coluna] = X_cod[coluna].astype(str)
            
            le = LabelEncoder()
            X_cod[coluna] = le.fit_transform(X_cod[coluna])
            encoders[coluna] = le
            
            num_classes = len(le.classes_)
            logger.info(f"Coluna {coluna}: {num_classes} classes únicas")
            
    except Exception as e:
        logger.error(f"Erro ao codificar variáveis categóricas: {str(e)}")
        raise
        
    return X_cod, encoders

def preprocessar_dados(
    X: pd.DataFrame,
    colunas_numericas: list,
    colunas_categoricas: list,
    estrategia_nulos: Dict[str, str]
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Realiza todo o pipeline de pré-processamento dos dados.
    
    Args:
        X: DataFrame com as features
        colunas_numericas: Lista de colunas numéricas
        colunas_categoricas: Lista de colunas categóricas
        estrategia_nulos: Dicionário com estratégia para tratamento de nulos
        
    Returns:
        Tuple com:
        - DataFrame processado
        - Dicionário com os objetos de transformação ajustados
    """
    logger.info("Iniciando pipeline de pré-processamento...")
    logger.info(f"Shape inicial dos dados: {X.shape}")
    
    try:
        X_processado = remover_valores_nulos(X, estrategia_nulos)
        logger.info("Valores nulos tratados com sucesso")
        
        X_processado = tratar_outliers(X_processado, colunas_numericas)
        logger.info("Outliers tratados com sucesso")
        
        X_processado, scaler = normalizar_features(X_processado, colunas_numericas)
        logger.info("Features normalizadas com sucesso")
        
        X_processado, encoders = codificar_categoricas(X_processado, colunas_categoricas)
        logger.info("Variáveis categóricas codificadas com sucesso")
        
        transformadores = {
            'scaler': scaler,
            'encoders': encoders
        }
        
        logger.info(f"Shape final dos dados: {X_processado.shape}")
        logger.info("Pipeline de pré-processamento concluído com sucesso!")
        
        return X_processado, transformadores
        
    except Exception as e:
        logger.error(f"Erro durante o pré-processamento: {str(e)}")
        raise