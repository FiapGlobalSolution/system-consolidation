from db import get_connection
import oracledb

# conn, cursor = get_connection()
# if conn is None or cursor is None:
#     print("Conexão com o banco falhou. Encerrando...")
#    exit()

# CREATE
def post_financeiro(descricao, tipo_movimentacao, valor, data):
    try:
        conn, cursor = get_connection()
        script = """
            INSERT INTO financeiro (descricao, tipo_movimentacao, valor, data)
            VALUES (:descricao, :tipo_movimentacao, :valor, :data)
        """
        cursor.execute(script, {
            'descricao': descricao,
            'tipo_movimentacao': tipo_movimentacao,
            'valor': valor,
            'data': data
        })
        conn.commit()
        print("Lançamento financeiro inserido com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao inserir financeiro:", e)
        conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# READ ALL
def get_all_financeiros():
    try:
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM financeiro")
        return cursor.fetchall()
    except oracledb.DatabaseError as e:
        print("Erro ao buscar lançamentos:", e)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# READ BY ID
def get_financeiro_by_id(id_finan):
    try:
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM financeiro WHERE id = :id", {'id': id_finan})
        return cursor.fetchone()
    except oracledb.DatabaseError as e:
        print("Erro ao buscar lançamento:", e)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# UPDATE
def update_financeiro(id_finan, descricao, tipo_movimentacao, valor, data):
    try:
        conn, cursor = get_connection()
        script = """
            UPDATE financeiro
            SET descricao = :descricao,
                tipo_movimentacao = :tipo_movimentacao,
                valor = :valor,
                data = :data
            WHERE id = :id
        """
        cursor.execute(script, {
            'id': id_finan,
            'descricao': descricao,
            'tipo_movimentacao': tipo_movimentacao,
            'valor': valor,
            'data': data
        })
        conn.commit()
        print(f"Lançamento com id = '{id_finan}' atualizado com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao atualizar lançamento:", e)
        conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# DELETE
def delete_financeiro(id_finan):
    try:
        conn, cursor = get_connection()
        cursor.execute("DELETE FROM financeiro WHERE id = :id", {'id': id_finan})
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Lançamento com id = '{id_finan}' deletado com sucesso!")
        else:
            print(f"Nenhum lançamento encontrado com id = '{id_finan}'.")
    except oracledb.DatabaseError as e:
        print("Erro ao deletar lançamento:", e)
        conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()