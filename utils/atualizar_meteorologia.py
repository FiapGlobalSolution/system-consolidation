from datetime import datetime
from sqlalchemy import create_engine, Table, Column, String, Float, DateTime, MetaData
from sqlalchemy.exc import SQLAlchemyError
from fase1.climate_service import ClimaService

# Configurações do Banco de Dados (substitua pelos seus dados)
DB_URL = "oracle+cx_oracle://RM563810:270506@ORACLE.FIAP.COM.BR:1521/ORCL"


# Inicializando SQLAlchemy
engine = create_engine(DB_URL)
metadata = MetaData()

# Definindo tabela para armazenar previsões
meteo_table = Table(
    "METEO_DATA", metadata,
    Column("CIDADE", String(50), nullable=False),
    Column("TEMPERATURA", Float, nullable=False),
    Column("UMIDADE", Float, nullable=False),
    Column("CONDICAO", String(100), nullable=False),
    Column("DATAHORA", DateTime, nullable=False)
)

metadata.create_all(engine)  # Cria a tabela caso não exista

# Inicializando o serviço de clima
API_KEY = "c7d2cf1a2b68e7acac01b2ad0de3b433"
clima_service = ClimaService(API_KEY)

def obter_dados_para_banco(cidade: str):
    """Pega os dados atuais do clima e transforma no formato do banco"""
    dados_clima = clima_service.buscar_clima_atual(cidade)
    if not dados_clima:
        return None

    return {
        "CIDADE": cidade,
        "TEMPERATURA": dados_clima["main"]["temp"],
        "UMIDADE": dados_clima["main"]["humidity"],
        "CONDICAO": dados_clima["weather"][0]["description"].capitalize(),
        "DATAHORA": datetime.now()
    }

def salvar_no_banco(dados):
    """Insere os dados no banco com tratamento de erro"""
    if not dados:
        print("❌ Nenhum dado válido para inserir.")
        return

    try:
        with engine.connect() as conn:
            conn.execute(meteo_table.insert(), [dados])
            print(f"[{datetime.now()}] Dados inseridos com sucesso!")
    except SQLAlchemyError as e:
        print(f"❌ Erro ao inserir no banco: {e}")

def main():
    cidade = "São Paulo"
    dados = obter_dados_para_banco(cidade)
    salvar_no_banco(dados)

if __name__ == "__main__":
    main()
