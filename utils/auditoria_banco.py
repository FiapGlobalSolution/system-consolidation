import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Pega a string de conexão do Oracle das variáveis de ambiente
DB_URL = os.getenv("DB_URL")

if not DB_URL:
    print("❌ Erro: a variável de ambiente DB_URL não está definida.")
    exit(1)

# Inicializa a engine
engine = create_engine(DB_URL)

def testar_conexao():
    """Testa a conexão com o banco"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 FROM DUAL"))
            print("✅ Conexão com o Oracle bem-sucedida! Resultado do teste:", result.scalar())
    except SQLAlchemyError as e:
        print("❌ Erro na conexão com o banco:", e)

def testar_insercao_tabela():
    """Testa inserção e leitura em tabela de teste"""
    from sqlalchemy import Table, Column, Integer, String, MetaData

    metadata = MetaData()
    tabela_teste = Table(
        "TEST_AUDITORIA", metadata,
        Column("ID", Integer, primary_key=True),
        Column("NOME", String(50))
    )

    # Cria a tabela se não existir
    metadata.create_all(engine)

    try:
        with engine.connect() as conn:
            # Inserção teste
            conn.execute(tabela_teste.insert().values(NOME="Teste Auditoria"))
            # Leitura teste
            result = conn.execute(tabela_teste.select())
            print("✅ Dados na tabela de teste:")
            for row in result:
                print(row)
    except SQLAlchemyError as e:
        print("❌ Erro durante teste de inserção/leitura:", e)

def main():
    testar_conexao()
    testar_insercao_tabela()

if __name__ == "__main__":
    main()
