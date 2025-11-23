import repositories.talhoes_repository as talhao_repo

def cadastrar_talhao():
    try:
        nome = input("Digite o nome do talhão: ")
        area = float(input("Digite a área (ha): "))
        cultura = input("Digite a cultura: ")
        data_plantio = input("Digite a data de plantio (YYYY-MM-DD) ou deixe vazio: ") or None
        data_colheita = input("Digite a data de colheita (YYYY-MM-DD) ou deixe vazio: ") or None

        talhao_repo.post_talhao(nome, area, cultura, data_plantio, data_colheita)
        print("Talhão cadastrado com sucesso!")
    except ValueError:
        print("Erro: valores inválidos inseridos.")
    except Exception as e:
        print("Erro ao cadastrar talhão:", e)


def consultar_talhao():
    try:
        todos = input("Deseja consultar todos os talhões? (s/n): ")
        if todos.lower() == 's':
            resultados = talhao_repo.get_all_talhoes()
        else:
            id_val = int(input("Digite o ID do talhão: "))
            resultados = talhao_repo.get_talhao_by_id(id_val)

        if resultados:
            print("Resultado da consulta:")
            if isinstance(resultados, list):
                for row in resultados:
                    print(f"ID: {row[0]}, Nome: {row[1]}, Área: {row[2]}, Cultura: {row[3]}, Plantio: {row[4]}, Colheita: {row[5]}")
            else:
                row = resultados
                print(f"ID: {row[0]}, Nome: {row[1]}, Área: {row[2]}, Cultura: {row[3]}, Plantio: {row[4]}, Colheita: {row[5]}")
        else:
            print("Nenhum talhão encontrado.")
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro na consulta de talhões:", e)


def update_talhao():
    try:
        id_val = int(input("Digite o ID do talhão a ser atualizado: "))
        nome = input("Digite o novo nome: ")
        area = float(input("Digite a nova área (ha): "))
        cultura = input("Digite a nova cultura: ")
        data_plantio = input("Digite a nova data de plantio (YYYY-MM-DD) ou deixe vazio: ") or None
        data_colheita = input("Digite a nova data de colheita (YYYY-MM-DD) ou deixe vazio: ") or None

        talhao_repo.update_talhao(id_val, nome, area, cultura, data_plantio, data_colheita)
        print("Talhão atualizado com sucesso!")
    except ValueError:
        print("Erro: valores inválidos inseridos.")
    except Exception as e:
        print("Erro ao atualizar talhão:", e)


def delete_talhao():
    try:
        id_val = int(input("Digite o ID do talhão a ser removido: "))
        talhao_repo.delete_talhao(id_val)
        print("Talhão removido com sucesso!")
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro ao remover talhão:", e)