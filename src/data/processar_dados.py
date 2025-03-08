"""
Script para executar o pipeline de pré-processamento nos dados.
"""

from src.data.data_acquisition import carregar_dados
from src.data.preprocessamento import preprocessar_dados
from src.utils.logger import configurar_logger
import joblib
import os

logger = configurar_logger('processar_dados')

COLUNAS_NUMERICAS = [
    'age', 'fnlwgt', 'education-num', 
    'capital-gain', 'capital-loss', 'hours-per-week'
]

COLUNAS_CATEGORICAS = [
    'workclass', 'education', 'marital-status', 
    'occupation', 'relationship', 'race', 
    'sex', 'native-country'
]

ESTRATEGIA_NULOS = {
    'workclass': 'most_frequent',
    'occupation': 'most_frequent',
    'native-country': 'most_frequent'
}

def main():
    """
    Função principal para executar o processamento dos dados.
    """
    try:
        logger.info("Carregando dados...")
        X, y, metadados = carregar_dados()
        
        logger.info("Aplicando pré-processamento...")
        X_processado, transformadores = preprocessar_dados(
            X=X,
            colunas_numericas=COLUNAS_NUMERICAS,
            colunas_categoricas=COLUNAS_CATEGORICAS,
            estrategia_nulos=ESTRATEGIA_NULOS
        )
        
        if not os.path.exists('data'):
            os.makedirs('data')
            
        logger.info("Salvando dados processados e transformadores...")
        X_processado.to_csv('data/features_processadas.csv', index=False)
        y.to_csv('data/target.csv', index=False)
        joblib.dump(transformadores, 'data/transformadores.joblib')
        
        logger.info(f"Shape final dos dados: {X_processado.shape}")
        logger.info("Processamento concluído com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro durante o processamento: {str(e)}")
        raise

if __name__ == "__main__":
    main()