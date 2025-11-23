from db import get_connection
import oracledb

# conn, cursor = get_connection()
# if conn is None or cursor is None:
#     print("Conexão com o banco falhou. Encerrando...")
#    exit()

def post_talhao(nome, area, cultura, data_plantio=None, data_colheita=None):
    try:
        conn, cursor = get_connection()
        script = """
            INSERT INTO talhoes (nome, area, cultura, data_plantio, data_colheita)
            VALUES (:nome, :area, :cultura, :data_plantio, :data_colheita)
        """
        cursor.execute(script, {
            'nome': nome,
            'area': area,
            'cultura': cultura,
            'data_plantio': data_plantio,
            'data_colheita': data_colheita
        })
        conn.commit()
        print("Talhão inserido com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao inserir talhão:", e)
        conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_all_talhoes():
    try:
        conn, cursor = get_connection()
        script = "SELECT * FROM talhoes"
        cursor.execute(script)
        return cursor.fetchall()
    except oracledb.DatabaseError as e:
        print("Erro ao buscar talhões:", e)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_talhao_by_id(id_talhao):
    try:
        conn, cursor = get_connection()
        script = "SELECT * FROM talhoes WHERE id = :id"
        cursor.execute(script, {'id': id_talhao})
        return cursor.fetchone()
    except oracledb.DatabaseError as e:
        print("Erro ao buscar talhão:", e)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def update_talhao(id_talhao, nome, area, cultura, data_plantio=None, data_colheita=None):
    try:
        conn, cursor = get_connection()
        script = """
            UPDATE talhoes
            SET nome = :nome,
                area = :area,
                cultura = :cultura,
                data_plantio = :data_plantio,
                data_colheita = :data_colheita
            WHERE id = :id
        """
        cursor.execute(script, {
            'id': id_talhao,
            'nome': nome,
            'area': area,
            'cultura': cultura,
            'data_plantio': data_plantio,
            'data_colheita': data_colheita
        })
        conn.commit()
        print(f"Talhão com id = '{id_talhao}' atualizado com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao atualizar talhão:", e)
        conn.rollback()

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_talhao(id_talhao):
    try:
        conn, cursor = get_connection()
        script = "DELETE FROM talhoes WHERE id = :id"
        cursor.execute(script, {'id': id_talhao})
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Talhão com id = '{id_talhao}' deletado com sucesso!")
        else:
            print(f"Nenhum talhão encontrado com id = '{id_talhao}'.")
    except oracledb.DatabaseError as e:
        print("Erro ao deletar talhão:", e)
        conn.rollback()
    finally:
        if cursor: cursor.close()
        if conn: conn.close()