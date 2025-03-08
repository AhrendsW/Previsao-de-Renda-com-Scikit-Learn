"""
API FastAPI para servir o modelo de previsão de renda.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
from typing import Dict, Any
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Previsão de Renda",
    description="API para prever a faixa de renda de uma pessoa",
    version="1.0.0"
)

try:
    logger.info("Carregando modelo e transformadores...")
    model = joblib.load("models/melhor_modelo.joblib")
    transformers = joblib.load("data/transformadores_features.joblib")
    logger.info(f"Modelo carregado com sucesso! Tipo: {type(model)}")
    logger.info(f"Transformadores carregados: {transformers.keys()}")
except Exception as e:
    logger.error(f"Erro ao carregar modelo ou transformadores: {str(e)}")
    raise

class InputData(BaseModel):
    age: int
    workclass: int
    education: int
    marital_status: int = Field(alias='marital-status')
    occupation: int
    relationship: int
    race: int
    sex: int
    capital_gain: int
    capital_loss: int
    hours_per_week: int
    native_country: int = Field(alias='native-country')

    class Config:
        allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "age": 39,
                "workclass": 4,
                "education": 11,
                "marital-status": 2,
                "occupation": 10,
                "relationship": 0,
                "race": 4,
                "sex": 1,
                "capital_gain": 2174,
                "capital_loss": 0,
                "hours_per_week": 40,
                "native-country": 39
            }
        }

def criar_features_idade(df: pd.DataFrame) -> pd.DataFrame:
    """Cria features baseadas na idade."""
    df_novo = df.copy()
    
    bins = [0, 25, 35, 45, 55, 65, 100]
    labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    df_novo['faixa_etaria'] = pd.cut(df_novo['age'], bins=bins, labels=labels)
    
    return df_novo

def criar_features_trabalho(df: pd.DataFrame) -> pd.DataFrame:
    """Cria features baseadas em trabalho."""
    df_novo = df.copy()
    
    df_novo['tipo_jornada'] = pd.cut(
        df_novo['hours-per-week'],
        bins=[0, 20, 40, 60, 168],
        labels=['Parcial', 'Normal', 'Extra', 'Extenso']
    )
    
    return df_novo

def criar_features_educacao(df: pd.DataFrame) -> pd.DataFrame:
    """Cria features baseadas em educação."""
    df_novo = df.copy()
    
    bins = [0, 8, 12, 14, 16, 20]
    labels = ['Básico', 'Médio', 'Superior Incompleto', 'Superior Completo', 'Pós-Graduação']
    
    df_novo['nivel_educacao'] = pd.cut(
        df_novo['education-num'],
        bins=bins,
        labels=labels,
        include_lowest=True
    )
    
    return df_novo

def education_to_num(education: int) -> int:
    """Converte o código de educação para education_num."""
    mapping = {
        0: 1,   # Preschool
        1: 2,   # 1st-4th
        2: 16,  # Superior Completo
        3: 7,   # 7th-8th
        4: 8,   # 9th
        5: 9,   # 10th
        6: 10,  # 11th
        7: 11,  # 12th
        8: 12,  # HS-grad
        9: 13,  # Some-college
        10: 14, # Assoc-voc
        11: 15, # Assoc-acdm
        12: 16, # Bachelors
        13: 17, # Masters
        14: 18, # Doctorate
        15: 16, # Prof-school
    }
    return mapping.get(education, 8)

def transformar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica todas as transformações nas features."""
    try:
        logger.debug("Iniciando transformação das features...")
        
        df['education_num'] = df['education'].apply(education_to_num)
        
        df = df.rename(columns={
            'marital_status': 'marital-status',
            'native_country': 'native-country',
            'capital_gain': 'capital-gain',
            'capital_loss': 'capital-loss',
            'education_num': 'education-num',
            'hours_per_week': 'hours-per-week'
        })
        
        logger.debug(f"Colunas após renomear: {df.columns.tolist()}")
        
        df['fnlwgt'] = 0
        
        df['razao_capital'] = df['capital-gain'] / (df['capital-loss'] + 1)
        df['tem_ganho_capital'] = (df['capital-gain'] > 0).astype(int)
        df['tem_perda_capital'] = (df['capital-loss'] > 0).astype(int)
        df['idade_aposentadoria'] = 65 - df['age']
        
        df = criar_features_idade(df)
        df = criar_features_trabalho(df)
        
        df['nivel_educacao'] = pd.cut(
            df['education-num'],
            bins=[0, 8, 12, 14, 16, 20],
            labels=['Básico', 'Médio', 'Superior Incompleto', 'Superior Completo', 'Pós-Graduação'],
            include_lowest=True
        )
        
        logger.debug("Features criadas com sucesso")
        logger.debug(f"Colunas após criar features: {df.columns.tolist()}")
        
        colunas_numericas = [
            'age', 'fnlwgt', 'education-num', 'capital-gain', 
            'capital-loss', 'hours-per-week', 'razao_capital', 
            'idade_aposentadoria', 'tem_ganho_capital', 'tem_perda_capital'
        ]
        df_numericas = df[colunas_numericas].copy()
        
        colunas_categoricas = [
            'workclass', 'education', 'marital-status',
            'occupation', 'relationship', 'race', 'sex',
            'native-country', 'faixa_etaria', 'tipo_jornada',
            'nivel_educacao'
        ]
        
        encoder = transformers.get('one_hot_encoder')
        if encoder:
            logger.debug("Aplicando One-Hot Encoding...")
            features_encoded = encoder.transform(df[colunas_categoricas])
            feature_names = encoder.get_feature_names_out(colunas_categoricas)
            
            df_encoded = pd.DataFrame(
                features_encoded,
                columns=feature_names,
                index=df.index
            )
            
            logger.debug(f"Features após encoding: {df_encoded.columns.tolist()}")
            
            df_final = pd.concat([df_numericas, df_encoded], axis=1)
            logger.debug(f"Features combinadas: {df_final.shape}")
            
            selector = transformers.get('selector')
            if selector:
                colunas_esperadas = selector.feature_names_in_
                logger.debug(f"Colunas esperadas pelo selector: {colunas_esperadas.tolist()}")
                
                df_final = df_final.reindex(columns=colunas_esperadas)
                logger.debug(f"Colunas após reordenação: {df_final.columns.tolist()}")
                
                df_final = selector.transform(df_final)
                logger.debug(f"Features finais após seleção: {df_final.shape}")
                return df_final
            
            return df_final
            
        logger.error("Encoder não encontrado nos transformadores")
        raise ValueError("Encoder não encontrado")
        
    except Exception as e:
        logger.error(f"Erro ao transformar features: {str(e)}")
        raise

@app.get("/")
def read_root():
    """
    Endpoint raiz para verificar se a API está funcionando.
    """
    return {
        "message": "API de Previsão de Renda",
        "status": "online",
        "model_loaded": model is not None
    }

@app.post("/predict")
def predict(data: InputData):
    """
    Endpoint para fazer previsões.
    
    Args:
        data: Dados de entrada no formato definido pelo schema InputData
        
    Returns:
        Dicionário com a previsão e probabilidades
    """
    try:
        logger.debug(f"Dados recebidos: {data.dict()}")
        df = pd.DataFrame([data.dict()])
        logger.debug(f"DataFrame criado: {df.shape}")
        
        X = transformar_features(df)
        logger.debug(f"Features transformadas: {X.shape}")
        
        logger.debug("Iniciando predição...")
        prediction = model.predict(X)
        logger.debug(f"Predição realizada: {prediction}")
        
        probabilities = model.predict_proba(X)
        logger.debug(f"Probabilidades calculadas: {probabilities}")
        
        response = {
            "prediction": int(prediction[0]),
            "prediction_label": ">50K" if prediction[0] == 1 else "<=50K",
            "probability_<=50K": float(probabilities[0][0]),
            "probability_>50K": float(probabilities[0][1])
        }
        
        logger.info(f"Previsão realizada com sucesso: {response}")
        return response
        
    except Exception as e:
        logger.error(f"Erro ao fazer previsão: {str(e)}")
        logger.error("Traceback completo:", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """
    Endpoint para verificar a saúde da API.
    """
    try:
        test_data = InputData(**{
            "age": 39,
            "workclass": 4,
            "education": 11,
            "marital-status": 2,
            "occupation": 10,
            "relationship": 0,
            "race": 4,
            "sex": 1,
            "capital_gain": 2174,
            "capital_loss": 0,
            "hours_per_week": 40,
            "native-country": 39
        })
        
        _ = predict(test_data)
        
        return {
            "status": "healthy",
            "model_loaded": model is not None,
            "prediction_test": "ok"
        }
    except Exception as e:
        logger.error(f"Erro no health check: {str(e)}")
        return {
            "status": "unhealthy",
            "model_loaded": model is not None,
            "error": str(e)
        }