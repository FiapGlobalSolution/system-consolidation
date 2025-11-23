from db import get_connection
import oracledb

# conn, cursor = get_connection()
# if conn is None or cursor is None:
#     print("Conexão com o banco falhou. Encerrando...")
#    exit()

def post_funcionario(nome, funcao):
    try:
        conn, cursor = get_connection()
        script = """INSERT INTO funcionarios (nome, funcao) VALUES (:nome, :funcao)"""
        
        cursor.execute(script, {'nome': nome, 'funcao': funcao})
        conn.commit()

    except oracledb.DatabaseError as e:
        print("Erro na transação do BD:", e)
        conn.rollback()
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_funcionarios():
    try:
        conn, cursor = get_connection()
        script = """SELECT * FROM funcionarios"""
        
        cursor.execute(script)
        resultado = cursor.fetchall()

        return resultado

    except oracledb.DatabaseError as e:
        print("Erro na consulta:", e)
        return None
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_funcionario_por_id(id):
    try:
        conn, cursor = get_connection()
        script = """SELECT * FROM funcionarios WHERE id = :id"""
        
        cursor.execute(script, {'id': id})
        resultado = cursor.fetchall()

        return resultado

    except oracledb.DatabaseError as e:
        print("Erro na consulta por id:", e)
        return None
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_funcionario_por_nome(nome):
    try:
        conn, cursor = get_connection()
        script = """SELECT * FROM funcionarios WHERE nome = :nome"""
        
        cursor.execute(script, {'nome': nome})
        resultado = cursor.fetchall()
        
        return resultado

    except oracledb.DatabaseError as e:
        print("Erro na consulta por nome:", e)
        return None
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
def get_funcionarios_por_funcao(funcao):
    try:
        conn, cursor = get_connection()
        script = """SELECT * FROM funcionarios WHERE funcao = :funcao"""
        
        cursor.execute(script, {'funcao': funcao})
        resultado = cursor.fetchall()
        
        return resultado

    except oracledb.DatabaseError as e:
        print("Erro na consulta por funcao:", e)
        return None
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
def update_funcionario(id_funcionario, campo, novo_valor):
    try:
        conn, cursor = get_connection()
        if campo.lower() not in ['nome', 'funcao']:
            print("Campo inválido. Só é permitido atualizar 'nome' ou 'funcao'.")
            return

        script = f"""UPDATE funcionarios SET {campo} = :valor WHERE id = :id"""
        
        cursor.execute(script, {'valor': novo_valor, 'id': id_funcionario})
        conn.commit()

        if cursor.rowcount > 0:
            print(f"{campo.capitalize()} atualizado com sucesso!")
        else:
            print("Nenhum funcionário encontrado com o ID informado.")

    except oracledb.DatabaseError as e:
        print("Erro ao atualizar funcionário:", e)
        conn.rollback()
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_funcionario(id):
    try:
        conn, cursor = get_connection()
        script = f"""DELETE FROM funcionarios WHERE id = :id"""

        cursor.execute(script, {'id': id})
        conn.commit()

        if cursor.rowcount > 0:
            print(f"Funcionário(s) com id = '{id}' deletado(s) com sucesso!")
        else:
            print(f"Nenhum funcionário encontrado com id = '{id}'.")

    except oracledb.DatabaseError as e:
        print("Erro ao deletar funcionário:", e)
        conn.rollback()
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            