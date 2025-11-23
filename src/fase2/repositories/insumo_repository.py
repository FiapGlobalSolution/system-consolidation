from db import get_connection
import oracledb

# conn, cursor = get_connection()
# if conn is None or cursor is None:
#     print("Conexão com o banco falhou. Encerrando...")
#    exit()

def post_insumo(nome, quantidade, peso, tipo, data_validade):
    try:
        conn, cursor = get_connection()
        script = """INSERT INTO insumos (nome, quantidade, peso, tipo, data_validade) VALUES (:nome, :quantidade, :peso, :tipo, :data_validade)"""
        
        cursor.execute(script, {'nome': nome, 'quantidade': quantidade, 'peso': peso, 'tipo': tipo, 'data_validade': data_validade})
        conn.commit()

    except oracledb.DatabaseError as e:
        print("Erro na transação do BD:", e)
        conn.rollback()
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_insumos():
    try:
        conn, cursor = get_connection()
        script = """SELECT * FROM insumos"""
        
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
    
def get_insumo_por_id(id):
    try:
        conn, cursor = get_connection()
        script = """SELECT * FROM insumos WHERE id = :id"""
        
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
    
def get_insumo_por_nome(nome):
    try:
        conn, cursor = get_connection()
        script = """SELECT * FROM insumos WHERE nome = :nome"""
        
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

def get_insumos_por_data_validade(data_validade):
    try:
        conn, cursor = get_connection()
        script = """SELECT * FROM insumos WHERE data_validade = :data_validade"""
        
        cursor.execute(script, {'data_validade': data_validade})
        resultado = cursor.fetchall()
        
        return resultado

    except oracledb.DatabaseError as e:
        print("Erro na consulta por data de validade:", e)
        return None
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
def get_insumos_por_tipo(tipo):
    try:
        conn, cursor = get_connection()
        script = """SELECT * FROM insumos WHERE tipo = :tipo"""
        
        cursor.execute(script, {'tipo': tipo})
        resultado = cursor.fetchall()
        
        return resultado

    except oracledb.DatabaseError as e:
        print("Erro na consulta por tipo:", e)
        return None
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_insumo(id_insumo, campo, novo_valor):
    try:
        conn, cursor = get_connection()
        script = f"""UPDATE insumos SET {campo} = :novo_valor WHERE id = :id_insumo"""
        
        cursor.execute(script, {'id_insumo': id_insumo, 'novo_valor': novo_valor})
        conn.commit()

        if cursor.rowcount > 0:
            print(f"{campo.capitalize()} atualizado com sucesso!")
        else:
            print("Nenhum insumo encontrado com o ID informado.")

    except oracledb.DatabaseError as e:
        print("Erro na transação do BD:", e)
        conn.rollback()
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_insumo(id_insumo):
    try:
        conn, cursor = get_connection()
        script = """DELETE FROM insumos WHERE id = :id_insumo"""
        
        cursor.execute(script, {'id_insumo': id_insumo})
        conn.commit()

        if cursor.rowcount > 0:
            print(f"Insumo(s) com id = '{id_insumo}' deletado(s) com sucesso!")
        else:
            print(f"Nenhum insumo encontrado com id = '{id_insumo}'.")

    except oracledb.DatabaseError as e:
        print("Erro na transação do BD:", e)
        conn.rollback()
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()