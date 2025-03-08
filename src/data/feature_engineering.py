"""
Módulo responsável pelo Feature Engineering.
Implementa transformações e criação de novas features.
"""

import pandas as pd
from typing import Tuple, Dict, Any, List
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_selection import SelectKBest, f_classif
from src.utils.logger import configurar_logger
import joblib

logger = configurar_logger('feature_engineering')

def criar_features_idade(X: pd.DataFrame) -> pd.DataFrame:
    """
    Cria features baseadas na idade.
    
    Args:
        X: DataFrame com as features originais
        
    Returns:
        DataFrame com as novas features
    """
    logger.info("Criando features baseadas na idade...")
    X_novo = X.copy()
    
    bins = [0, 25, 35, 45, 55, 65, 100]
    labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    X_novo['faixa_etaria'] = pd.cut(X_novo['age'], bins=bins, labels=labels)
    
    X_novo['idade_aposentadoria'] = (X_novo['age'] >= 65).astype(int)
    
    logger.info("Features de idade criadas com sucesso")
    return X_novo

def criar_features_trabalho(X: pd.DataFrame) -> pd.DataFrame:
    """
    Cria features baseadas em informações de trabalho.
    
    Args:
        X: DataFrame com as features originais
        
    Returns:
        DataFrame com as novas features
    """
    logger.info("Criando features baseadas em trabalho...")
    X_novo = X.copy()
    
    X_novo['tipo_jornada'] = pd.cut(
        X_novo['hours-per-week'],
        bins=[0, 20, 40, 60, 168],
        labels=['Parcial', 'Normal', 'Extra', 'Extenso']
    )
    
    X_novo['tem_ganho_capital'] = (X_novo['capital-gain'] > 0).astype(int)
    X_novo['tem_perda_capital'] = (X_novo['capital-loss'] > 0).astype(int)
    
    X_novo['razao_capital'] = X_novo['capital-gain'] / (X_novo['capital-loss'] + 1)
    
    logger.info("Features de trabalho criadas com sucesso")
    return X_novo

def criar_features_educacao(X: pd.DataFrame) -> pd.DataFrame:
    """
    Cria features baseadas em educação.
    
    Args:
        X: DataFrame com as features originais
        
    Returns:
        DataFrame com as novas features
    """
    logger.info("Criando features baseadas em educação...")
    X_novo = X.copy()
    
    X_novo['nivel_educacao'] = pd.qcut(
        X_novo['education-num'],
        q=4,
        labels=['Básico', 'Médio', 'Superior', 'Avançado']
    )
    
    logger.info("Features de educação criadas com sucesso")
    return X_novo

def aplicar_one_hot_encoding(
    X: pd.DataFrame,
    colunas_categoricas: List[str]
) -> Tuple[pd.DataFrame, OneHotEncoder]:
    """
    Aplica One-Hot Encoding nas features categóricas.
    
    Args:
        X: DataFrame com as features
        colunas_categoricas: Lista de colunas para aplicar OHE
        
    Returns:
        Tuple com:
        - DataFrame com features codificadas
        - Objeto OneHotEncoder ajustado
    """
    logger.info("Aplicando One-Hot Encoding...")
    
    try:
        encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
        features_encoded = encoder.fit_transform(X[colunas_categoricas])
        
        feature_names = encoder.get_feature_names_out(colunas_categoricas)
        X_encoded = pd.DataFrame(
            features_encoded,
            columns=feature_names,
            index=X.index
        )
        
        X_final = X.drop(columns=colunas_categoricas)
        X_final = pd.concat([X_final, X_encoded], axis=1)
        
        n_features = len(feature_names)
        logger.info(f"One-Hot Encoding gerou {n_features} novas features")
        
        return X_final, encoder
        
    except Exception as e:
        logger.error(f"Erro ao aplicar One-Hot Encoding: {str(e)}")
        raise

def selecionar_melhores_features(
    X: pd.DataFrame,
    y: pd.DataFrame,
    k: int = 20
) -> Tuple[pd.DataFrame, SelectKBest]:
    """
    Seleciona as k melhores features usando o teste F-ANOVA.
    
    Args:
        X: DataFrame com as features
        y: Series com a variável target
        k: Número de features para selecionar
        
    Returns:
        Tuple com:
        - DataFrame com as features selecionadas
        - Objeto SelectKBest ajustado
    """
    logger.info(f"Selecionando as {k} melhores features...")
    
    try:
        selector = SelectKBest(score_func=f_classif, k=k)
        X_selected = selector.fit_transform(X, y)
        
        mask = selector.get_support()
        features_selecionadas = X.columns[mask]
        
        X_final = pd.DataFrame(X_selected, columns=features_selecionadas, index=X.index)
        
        scores = pd.DataFrame({
            'feature': X.columns,
            'score': selector.scores_
        }).sort_values('score', ascending=False)
        
        logger.info("\nTop 10 features mais importantes:")
        for _, row in scores.head(10).iterrows():
            logger.info(f"- {row['feature']}: {row['score']:.2f}")
        
        return X_final, selector
        
    except Exception as e:
        logger.error(f"Erro ao selecionar features: {str(e)}")
        raise

def engenharia_features(
    X: pd.DataFrame,
    y: pd.DataFrame = None,
    colunas_numericas: List[str] = None,
    colunas_categoricas: List[str] = None,
    k_features: int = 20
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Aplica todo o pipeline de feature engineering.
    
    Args:
        X: DataFrame com as features originais
        y: DataFrame com a variável target (opcional)
        colunas_numericas: Lista de colunas numéricas
        colunas_categoricas: Lista de colunas categóricas
        k_features: Número de features para selecionar
        
    Returns:
        Tuple com:
        - DataFrame com features transformadas
        - Dicionário com os objetos de transformação
    """
    logger.info("Iniciando pipeline de feature engineering...")
    logger.info(f"Shape inicial: {X.shape}")
    
    try:
        X_transformed = criar_features_idade(X)
        X_transformed = criar_features_trabalho(X_transformed)
        X_transformed = criar_features_educacao(X_transformed)
        
        logger.info(f"Shape após criação de features: {X_transformed.shape}")
        
        if colunas_categoricas:
            X_transformed, encoder = aplicar_one_hot_encoding(
                X_transformed,
                colunas_categoricas + ['faixa_etaria', 'tipo_jornada', 'nivel_educacao']
            )
            logger.info(f"Shape após One-Hot Encoding: {X_transformed.shape}")
        else:
            encoder = None
            
        if y is not None and k_features:
            X_transformed, selector = selecionar_melhores_features(
                X_transformed,
                y,
                k=k_features
            )
            logger.info(f"Shape final após seleção: {X_transformed.shape}")
        else:
            selector = None
            
        transformadores = {
            'one_hot_encoder': encoder,
            'selector': selector
        }
        
        logger.info("Pipeline de feature engineering concluído com sucesso!")
        return X_transformed, transformadores
        
    except Exception as e:
        logger.error(f"Erro durante feature engineering: {str(e)}")
        raise

def main():
    """
    Função principal para executar o feature engineering.
    """
    try:
        logger.info("Carregando dados processados...")
        X = pd.read_csv('data/features_processadas.csv')
        y = pd.read_csv('data/target.csv')
        
        colunas_numericas = [
            'age', 'fnlwgt', 'education-num',
            'capital-gain', 'capital-loss', 'hours-per-week'
        ]
        
        colunas_categoricas = [
            'workclass', 'education', 'marital-status',
            'occupation', 'relationship', 'race',
            'sex', 'native-country'
        ]
        
        X_transformed, transformadores = engenharia_features(
            X=X,
            y=y,
            colunas_numericas=colunas_numericas,
            colunas_categoricas=colunas_categoricas,
            k_features=20
        )
        
        logger.info("Salvando dados transformados...")
        X_transformed.to_csv('data/features_engineered.csv', index=False)
        joblib.dump(transformadores, 'data/transformadores_features.joblib')
        
        logger.info("Processo concluído com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro no processo: {str(e)}")
        raise

if __name__ == "__main__":
    main()