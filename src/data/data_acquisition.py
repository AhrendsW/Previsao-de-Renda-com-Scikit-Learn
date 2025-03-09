"""
Módulo responsável pela aquisição dos dados do UCI Machine Learning Repository.
Este módulo contém funções para carregar e realizar a validação inicial dos dados.

Dataset: Adult Income (Census Income)
URL: https://archive.ics.uci.edu/dataset/2/adult
"""

import pandas as pd
from ucimlrepo import fetch_ucirepo
from typing import Tuple, Dict, Any
from src.utils.logger import configurar_logger

logger = configurar_logger('aquisicao_dados')

def carregar_dados() -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Carrega os dados do UCI ML Repository e retorna as features, target e metadados.
    
    Dataset utilizado: Adult Income (id=2)
    URL: https://archive.ics.uci.edu/dataset/2/adult
    
    Returns:
        Tuple contendo:
        - DataFrame com as features
        - DataFrame com o target
        - Dicionário com os metadados do dataset
    """
    logger.info("Iniciando carregamento dos dados do UCI ML Repository...")
    
    adult = fetch_ucirepo(id=2)
    
    X = adult.data.features
    y = adult.data.targets
    metadados = {
        "nome": adult.metadata.name,
        "descricao": adult.metadata.description,
        "variaveis": adult.variables
    }
    
    logger.info(f"Dados carregados com sucesso. Shape do dataset: {X.shape}")
    return X, y, metadados

def validar_dados(X: pd.DataFrame, y: pd.DataFrame) -> Dict[str, Any]:
    """
    Realiza uma validação inicial dos dados carregados.
    
    Args:
        X: DataFrame com as features
        y: DataFrame com o target
        
    Returns:
        Dicionário com informações sobre a qualidade dos dados
    """
    logger.info("Iniciando validação dos dados...")
    
    info_dados = {
        "num_amostras": len(X),
        "num_features": X.shape[1],
        "colunas": list(X.columns),
        "valores_nulos": X.isnull().sum().to_dict(),
        "tipos_dados": X.dtypes.to_dict(),
        "distribuicao_classes": y.value_counts().to_dict()
    }
    
    logger.info(f"Número total de amostras: {info_dados['num_amostras']}")
    logger.info(f"Número de features: {info_dados['num_features']}")
    
    colunas_com_nulos = {k: v for k, v in info_dados['valores_nulos'].items() if v > 0}
    if colunas_com_nulos:
        logger.warning(f"Encontrados valores nulos nas colunas: {colunas_com_nulos}")
    
    return info_dados

def main():
    """
    Função principal para executar o processo de aquisição de dados.
    """
    logger.info("Iniciando processo de aquisição de dados...")
    
    try:
        X, y, metadados = carregar_dados()
        logger.info(f"Dataset carregado: {metadados['nome']}")
        
        info = validar_dados(X, y)
        
        logger.info("Processo de aquisição de dados concluído com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro durante a aquisição dos dados: {str(e)}")
        raise

if __name__ == "__main__":
    main()