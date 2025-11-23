from db import get_connection
import oracledb

# conn, cursor = get_connection()
# if conn is None or cursor is None:
#     print("Conexão com o banco falhou. Encerrando...")
#    exit()

# CREATE
def post_relatorio(nome, tipo, descricao, data_geracao):
    try:
        conn, cursor = get_connection()
        script = """
            INSERT INTO relatorios (nome, tipo, descricao, data_geracao)
            VALUES (:nome, :tipo, :descricao, :data_geracao)
        """
        cursor.execute(script, {
            'nome': nome,
            'tipo': tipo,
            'descricao': descricao,
            'data_geracao': data_geracao
        })
        conn.commit()
        print("Relatório gerado e salvo com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao inserir relatório:", e)
        conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# READ ALL
def get_all_relatorios():
    try:
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM relatorios")
        return cursor.fetchall()
    except oracledb.DatabaseError as e:
        print("Erro ao buscar relatórios:", e)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# READ BY ID
def get_relatorio_by_id(id_rel):
    try:
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM relatorios WHERE id = :id", {'id': id_rel})
        return cursor.fetchone()
    except oracledb.DatabaseError as e:
        print("Erro ao buscar relatório:", e)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# UPDATE
def update_relatorio(id_rel, nome, tipo, descricao, data_geracao):
    try:
        conn, cursor = get_connection()
        script = """
            UPDATE relatorios
            SET nome = :nome,
                tipo = :tipo,
                descricao = :descricao,
                data_geracao = :data_geracao
            WHERE id = :id
        """
        cursor.execute(script, {
            'id': id_rel,
            'nome': nome,
            'tipo': tipo,
            'descricao': descricao,
            'data_geracao': data_geracao
        })
        conn.commit()
        print(f"Relatório com id = '{id_rel}' atualizado com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao atualizar relatório:", e)
        conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# DELETE
def delete_relatorio(id_rel):
    try:
        conn, cursor = get_connection()
        cursor.execute("DELETE FROM relatorios WHERE id = :id", {'id': id_rel})
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Relatório com id = '{id_rel}' deletado com sucesso!")
        else:
            print(f"Nenhum relatório encontrado com id = '{id_rel}'.")
    except oracledb.DatabaseError as e:
        print("Erro ao deletar relatório:", e)
        conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()