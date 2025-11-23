"""
Configurações globais do sistema FarmTech
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    """Classe de configuração centralizada"""
    
    # Diretórios do projeto
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = BASE_DIR / "models"
    DATABASE_DIR = BASE_DIR / "database"
    
    # API Keys
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "207d471599cab6f442a27a1ece9643cb")
    
    # Banco de Dados Oracle (Fase 2)
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "1521")
    DB_SERVICE = os.getenv("DB_SERVICE")
    
    # Banco de Dados SQLite (Fase 4)
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", str(DATABASE_DIR / "farmtech.db"))
    
    # AWS (Fase 5)
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")
    
    # Configurações Gerais
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # Modelo ML
    ML_MODEL_PATH = str(MODELS_DIR / "modelo_irrigacao.pkl")
    
    # Criar diretórios se não existirem
    @classmethod
    def create_directories(cls):
        """Cria diretórios necessários se não existirem"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.MODELS_DIR.mkdir(exist_ok=True)
        cls.DATABASE_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def validate_config(cls) -> dict:
        """Valida configurações e retorna status"""
        status = {
            'api_weather': bool(cls.OPENWEATHER_API_KEY),
            'db_oracle': all([cls.DB_USER, cls.DB_PASSWORD, cls.DB_HOST]),
            'db_sqlite': bool(cls.SQLITE_DB_PATH),
            'aws': all([cls.AWS_ACCESS_KEY_ID, cls.AWS_SECRET_ACCESS_KEY]),
        }
        return status

# Inicializa diretórios na importação
Config.create_directories()
