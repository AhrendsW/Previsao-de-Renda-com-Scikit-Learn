"""
Módulo para análise exploratória dos dados (EDA).
Foco em visualizações e análise de correlações.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Tuple
from src.utils.logger import configurar_logger
import os

# Configurar logger
logger = configurar_logger('analise_exploratoria')

def carregar_dados_processados() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carrega os dados processados dos arquivos CSV.
    
    Returns:
        Tuple contendo features e target
    """
    logger.info("Carregando dados processados...")
    
    try:
        X = pd.read_csv('data/features_processadas.csv')
        y = pd.read_csv('data/target.csv')
        
        logger.info(f"Dados carregados com sucesso. Shape: {X.shape}")
        return X, y
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {str(e)}")
        raise

def criar_diretorio_visualizacoes():
    """
    Cria o diretório para salvar as visualizações se não existir.
    """
    if not os.path.exists('visualizations'):
        os.makedirs('visualizations')
        logger.info("Diretório de visualizações criado")

def gerar_matriz_correlacao(
    X: pd.DataFrame,
    colunas_numericas: list
) -> None:
    """
    Gera e salva a matriz de correlação das features numéricas.
    
    Args:
        X: DataFrame com as features
        colunas_numericas: Lista de colunas numéricas para análise
    """
    logger.info("Gerando matriz de correlação...")
    
    try:
        # Criar figura com tamanho adequado
        plt.figure(figsize=(12, 8))
        
        # Calcular correlações
        correlacoes = X[colunas_numericas].corr()
        
        # Gerar heatmap
        sns.heatmap(
            correlacoes,
            annot=True,  # Mostrar valores
            cmap='coolwarm',  # Esquema de cores
            center=0,  # Centralizar em 0
            fmt='.2f',  # Formato dos números
            square=True  # Células quadradas
        )
        
        plt.title('Matriz de Correlação - Features Numéricas')
        plt.tight_layout()
        
        # Salvar figura
        plt.savefig('visualizations/matriz_correlacao.png')
        plt.close()
        
        # Identificar correlações fortes
        correlacoes_fortes = []
        for i in range(len(colunas_numericas)):
            for j in range(i+1, len(colunas_numericas)):
                corr = abs(correlacoes.iloc[i, j])
                if corr > 0.5:  # Limiar para correlação forte
                    correlacoes_fortes.append({
                        'feature1': colunas_numericas[i],
                        'feature2': colunas_numericas[j],
                        'correlacao': corr
                    })
        
        if correlacoes_fortes:
            logger.info("Correlações fortes encontradas:")
            for corr in correlacoes_fortes:
                logger.info(
                    f"{corr['feature1']} x {corr['feature2']}: {corr['correlacao']:.2f}"
                )
        else:
            logger.info("Nenhuma correlação forte encontrada entre as features")
            
    except Exception as e:
        logger.error(f"Erro ao gerar matriz de correlação: {str(e)}")
        raise

def analisar_distribuicao_target(y: pd.DataFrame) -> None:
    """
    Analisa e visualiza a distribuição da variável target.
    
    Args:
        y: DataFrame com a variável target
    """
    logger.info("Analisando distribuição da variável target...")
    
    try:
        # Criar figura
        plt.figure(figsize=(10, 6))
        
        # Calcular distribuição
        distribuicao = y['income'].value_counts()
        
        # Criar gráfico de barras
        sns.barplot(x=distribuicao.index, y=distribuicao.values)
        
        plt.title('Distribuição da Variável Target (Income)')
        plt.xlabel('Faixa de Renda')
        plt.ylabel('Quantidade')
        
        # Adicionar valores sobre as barras
        for i, v in enumerate(distribuicao.values):
            plt.text(i, v, str(v), ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Salvar figura
        plt.savefig('visualizations/distribuicao_target.png')
        plt.close()
        
        # Calcular proporções
        proporcoes = (distribuicao / len(y) * 100).round(2)
        for classe, prop in proporcoes.items():
            logger.info(f"Classe {classe}: {prop}%")
            
    except Exception as e:
        logger.error(f"Erro ao analisar distribuição do target: {str(e)}")
        raise

def analisar_features_categoricas(
    X: pd.DataFrame,
    colunas_categoricas: list,
    max_categorias: int = 10
) -> None:
    """
    Analisa a distribuição das features categóricas.
    
    Args:
        X: DataFrame com as features
        colunas_categoricas: Lista de colunas categóricas
        max_categorias: Número máximo de categorias para mostrar no gráfico
    """
    logger.info("Analisando features categóricas...")
    
    try:
        for coluna in colunas_categoricas:
            if coluna not in X.columns:
                continue
                
            # Calcular distribuição
            distribuicao = X[coluna].value_counts()
            
            # Se houver muitas categorias, mostrar apenas as top N
            if len(distribuicao) > max_categorias:
                distribuicao = distribuicao.head(max_categorias)
                logger.info(f"Mostrando top {max_categorias} categorias para {coluna}")
            
            # Criar figura
            plt.figure(figsize=(12, 6))
            
            # Criar gráfico de barras
            sns.barplot(x=distribuicao.index, y=distribuicao.values)
            
            plt.title(f'Distribuição da Feature: {coluna}')
            plt.xlabel('Categorias')
            plt.ylabel('Quantidade')
            plt.xticks(rotation=45, ha='right')
            
            # Adicionar valores sobre as barras
            for i, v in enumerate(distribuicao.values):
                plt.text(i, v, str(v), ha='center', va='bottom')
            
            plt.tight_layout()
            
            # Salvar figura
            plt.savefig(f'visualizations/distribuicao_{coluna}.png')
            plt.close()
            
            # Logging das proporções
            proporcoes = (distribuicao / len(X) * 100).round(2)
            logger.info(f"\nDistribuição de {coluna}:")
            for cat, prop in proporcoes.items():
                logger.info(f"- {cat}: {prop}%")
                
    except Exception as e:
        logger.error(f"Erro ao analisar features categóricas: {str(e)}")
        raise

def main():
    """
    Função principal para executar a análise exploratória.
    """
    try:
        # 1. Carregar dados processados
        X, y = carregar_dados_processados()
        
        # 2. Criar diretório para visualizações
        criar_diretorio_visualizacoes()
        
        # 3. Definir colunas numéricas e categóricas
        colunas_numericas = [
            'age', 'fnlwgt', 'education-num',
            'capital-gain', 'capital-loss', 'hours-per-week'
        ]
        
        colunas_categoricas = [
            'workclass', 'education', 'marital-status',
            'occupation', 'relationship', 'race',
            'sex', 'native-country'
        ]
        
        # 4. Gerar matriz de correlação
        logger.info("Gerando visualizações...")
        gerar_matriz_correlacao(X, colunas_numericas)
        
        # 5. Analisar distribuição do target
        analisar_distribuicao_target(y)
        
        # 6. Analisar features categóricas
        analisar_features_categoricas(X, colunas_categoricas)
        
        logger.info("Análise exploratória concluída com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro durante a análise exploratória: {str(e)}")
        raise

if __name__ == "__main__":
    main() 