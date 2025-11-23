from db import get_connection
import oracledb

# conn, cursor = get_connection()
# if conn is None or cursor is None:
#     print("Conexão com o banco falhou. Encerrando...")
#    exit()

# CREATE
def post_tarefa(titulo, descricao, status, data_inicio=None, data_conclusao=None):
    try:
        conn, cursor = get_connection()
        script = """
            INSERT INTO tarefas (titulo, descricao, status, data_inicio, data_conclusao)
            VALUES (:titulo, :descricao, :status, :data_inicio, :data_conclusao)
        """
        cursor.execute(script, {
            'titulo': titulo,
            'descricao': descricao,
            'status': status,
            'data_inicio': data_inicio,
            'data_conclusao': data_conclusao
        })
        conn.commit()
        print("Tarefa criada com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao criar tarefa:", e)
        conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# READ ALL
def get_all_tarefas():
    try:
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM tarefas")
        return cursor.fetchall()
    except oracledb.DatabaseError as e:
        print("Erro ao buscar tarefas:", e)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# READ BY ID
def get_tarefa_by_id(id_tar):
    try:
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM tarefas WHERE id = :id", {'id': id_tar})
        return cursor.fetchone()
    except oracledb.DatabaseError as e:
        print("Erro ao buscar tarefa:", e)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# UPDATE
def update_tarefa(id_tar, titulo, descricao, status, data_inicio=None, data_conclusao=None):
    try:
        conn, cursor = get_connection()
        script = """
            UPDATE tarefas
            SET titulo = :titulo,
                descricao = :descricao,
                status = :status,
                data_inicio = :data_inicio,
                data_conclusao = :data_conclusao
            WHERE id = :id
        """
        cursor.execute(script, {
            'id': id_tar,
            'titulo': titulo,
            'descricao': descricao,
            'status': status,
            'data_inicio': data_inicio,
            'data_conclusao': data_conclusao
        })
        conn.commit()
        print(f"Tarefa com id = '{id_tar}' atualizada com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao atualizar tarefa:", e)
        conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# DELETE
def delete_tarefa(id_tar):
    try:
        conn, cursor = get_connection()
        cursor.execute("DELETE FROM tarefas WHERE id = :id", {'id': id_tar})
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Tarefa com id = '{id_tar}' deletada com sucesso!")
        else:
            print(f"Nenhuma tarefa encontrada com id = '{id_tar}'.")
    except oracledb.DatabaseError as e:
        print("Erro ao deletar tarefa:", e)
        conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()