"""
Gerenciador de conexão com banco de dados
Refatorado da Fase 2 (db.py) com suporte para SQLite e Oracle
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


class DatabaseHandler:
    """Gerenciador de conexão com banco de dados"""
    
    def __init__(self, db_type: str = "sqlite"):
        """
        Inicializa conexão com banco de dados
        
        Args:
            db_type: Tipo de banco ('sqlite' ou 'oracle')
        """
        self.db_type = db_type
        self.engine = None
        self.SessionLocal = None
        self._setup_connection()
    
    def _setup_connection(self):
        """Configura conexão baseado no tipo de banco"""
        try:
            if self.db_type == "sqlite":
                self._setup_sqlite()
            elif self.db_type == "oracle":
                self._setup_oracle()
            else:
                raise ValueError(f"Tipo de banco '{self.db_type}' não suportado")
            
            # Criar sessionmaker
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
        except Exception as e:
            print(f"❌ Erro ao configurar conexão com banco de dados: {e}")
            raise
    
    def _setup_sqlite(self):
        """Configura conexão SQLite"""
        db_path = os.getenv("SQLITE_DB_PATH", "database/farmtech.db")
        
        # Garantir que o diretório existe
        db_file = Path(db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)
        
        connection_string = f"sqlite:///{db_path}"
        self.engine = create_engine(
            connection_string,
            echo=False,  # Mude para True para debug
            connect_args={"check_same_thread": False}
        )
        print(f"✅ Conexão SQLite configurada: {db_path}")
    
    def _setup_oracle(self):
        """Configura conexão Oracle"""
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT", "1521")
        db_service = os.getenv("DB_SERVICE")
        
        if not all([db_user, db_password, db_host, db_service]):
            raise ValueError(
                "Variáveis de ambiente para Oracle não configuradas. "
                "Verifique DB_USER, DB_PASSWORD, DB_HOST e DB_SERVICE no arquivo .env"
            )
        
        try:
            import oracledb
        except ImportError:
            raise ImportError(
                "Biblioteca 'oracledb' não instalada. "
                "Execute: pip install oracledb"
            )
        
        connection_string = (
            f"oracle+oracledb://{db_user}:{db_password}@"
            f"{db_host}:{db_port}/{db_service}"
        )
        
        self.engine = create_engine(connection_string, echo=False)
        print(f"✅ Conexão Oracle configurada: {db_host}:{db_port}/{db_service}")
    
    def get_session(self) -> Session:
        """
        Retorna uma sessão do banco de dados
        
        Returns:
            Sessão SQLAlchemy
        """
        if not self.SessionLocal:
            raise RuntimeError("Database não foi inicializado corretamente")
        return self.SessionLocal()
    
    def create_tables(self, base):
        """
        Cria todas as tabelas definidas nos models
        
        Args:
            base: Classe Base do SQLAlchemy com os models
        """
        try:
            base.metadata.create_all(bind=self.engine)
            print("✅ Tabelas criadas/verificadas com sucesso")
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            raise
    
    def drop_tables(self, base):
        """
        Remove todas as tabelas (use com cuidado!)
        
        Args:
            base: Classe Base do SQLAlchemy com os models
        """
        try:
            base.metadata.drop_all(bind=self.engine)
            print("⚠️ Todas as tabelas foram removidas")
        except Exception as e:
            print(f"❌ Erro ao remover tabelas: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Testa a conexão com o banco de dados
        
        Returns:
            True se a conexão está funcionando
        """
        try:
            from sqlalchemy import text
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("✅ Conexão com banco de dados OK")
            return True
        except Exception as e:
            print(f"❌ Erro ao testar conexão: {e}")
            return False
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.engine:
            self.engine.dispose()
            print("🔒 Conexão com banco de dados fechada")
