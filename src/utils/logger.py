"""
Módulo de logging para o projeto.
"""

import logging
from datetime import datetime
import os

def configurar_logger(nome: str) -> logging.Logger:
    """
    Configura e retorna um logger personalizado.
    
    Args:
        nome: Nome do logger
        
    Returns:
        Logger configurado
    """
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    logger = logging.getLogger(nome)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    data_atual = datetime.now().strftime('%Y%m%d')
    file_handler = logging.FileHandler(
        f'logs/{nome}_{data_atual}.log',
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 