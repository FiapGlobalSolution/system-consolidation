import repositories.financeiro_repository as fin_repo


def cadastrar_financeiro():
    try:
        descricao = input("Digite a descrição do lançamento financeiro: ")
        tipo_movimentacao = input("Digite o tipo (receita/despesa): ")
        valor = float(input("Digite o valor: "))
        data = input("Digite a data (YYYY-MM-DD): ")

        fin_repo.post_financeiro(descricao, tipo_movimentacao, valor, data)
        print("Lançamento financeiro cadastrado com sucesso!")
    except ValueError:
        print("Erro: valores inválidos inseridos.")
    except Exception as e:
        print("Erro ao cadastrar lançamento financeiro:", e)


def consultar_financeiro():
    try:
        todos = input("Deseja consultar todos os lançamentos financeiros? (s/n): ")
        if todos.lower() == 's':
            resultados = fin_repo.get_all_financeiros()
        else:
            id_val = int(input("Digite o ID do lançamento: "))
            resultados = fin_repo.get_financeiro_by_id(id_val)

        if resultados:
            print("Resultado da consulta:")
            # get_all retorna lista, get_by retorna tupla
            if isinstance(resultados, list):
                for row in resultados:
                    print(f"ID: {row[0]}, Descrição: {row[1]}, Tipo: {row[2]}, Valor: {row[3]}, Data: {row[4]}")
            else:
                row = resultados
                print(f"ID: {row[0]}, Descrição: {row[1]}, Tipo: {row[2]}, Valor: {row[3]}, Data: {row[4]}")
        else:
            print("Nenhum lançamento financeiro encontrado.")
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro na consulta financeira:", e)


def atualizar_financeiro():
    try:
        id_val = int(input("Digite o ID do lançamento a ser atualizado: "))
        descricao = input("Digite a nova descrição: ")
        tipo_movimentacao = input("Digite o novo tipo (receita/despesa): ")
        valor = float(input("Digite o novo valor: "))
        data = input("Digite a nova data (YYYY-MM-DD): ")

        fin_repo.update_financeiro(id_val, descricao, tipo_movimentacao, valor, data)
        print("Lançamento financeiro atualizado com sucesso!")
    except ValueError:
        print("Erro: valores inválidos inseridos.")
    except Exception as e:
        print("Erro ao atualizar lançamento financeiro:", e)


def remover_financeiro():
    try:
        id_val = int(input("Digite o ID do lançamento a ser removido: "))
        fin_repo.delete_financeiro(id_val)
        print("Lançamento financeiro removido com sucesso!")
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro ao remover lançamento financeiro:", e)
