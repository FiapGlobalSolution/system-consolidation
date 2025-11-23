import repositories.tarefas_repository as tar_repo

def cadastrar_tarefa():
    try:
        titulo = input("Digite o título da tarefa: ")
        descricao = input("Digite a descrição (ou deixe vazio): ") or None
        status = input("Digite o status (pendente/em andamento/concluída): ")
        data_inicio = input("Digite a data de início (YYYY-MM-DD) ou deixe vazio: ") or None
        data_conclusao = input("Digite a data de conclusão (YYYY-MM-DD) ou deixe vazio: ") or None

        tar_repo.post_tarefa(titulo, descricao, status, data_inicio, data_conclusao)
        print("Tarefa cadastrada com sucesso!")
    except ValueError:
        print("Erro: valores inválidos inseridos.")
    except Exception as e:
        print("Erro ao cadastrar tarefa:", e)


def consultar_tarefa():
    try:
        todos = input("Deseja consultar todas as tarefas? (s/n): ")
        if todos.lower() == 's':
            resultados = tar_repo.get_all_tarefas()
        else:
            id_val = int(input("Digite o ID da tarefa: "))
            resultados = tar_repo.get_tarefa_by_id(id_val)

        if resultados:
            print("Resultado da consulta:")
            if isinstance(resultados, list):
                for row in resultados:
                    print(f"ID: {row[0]}, Título: {row[1]}, Descrição: {row[2]}, Status: {row[3]}, Início: {row[4]}, Conclusão: {row[5]}")
            else:
                row = resultados
                print(f"ID: {row[0]}, Título: {row[1]}, Descrição: {row[2]}, Status: {row[3]}, Início: {row[4]}, Conclusão: {row[5]}")
        else:
            print("Nenhuma tarefa encontrada.")
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro na consulta de tarefas:", e)


def atualizar_tarefa():
    try:
        id_val = int(input("Digite o ID da tarefa a ser atualizada: "))
        titulo = input("Digite o novo título: ")
        descricao = input("Digite a nova descrição (ou deixe vazio): ") or None
        status = input("Digite o novo status (pendente/em andamento/concluída): ")
        data_inicio = input("Digite a nova data de início (YYYY-MM-DD) ou deixe vazio: ") or None
        data_conclusao = input("Digite a nova data de conclusão (YYYY-MM-DD) ou deixe vazio: ") or None

        tar_repo.update_tarefa(id_val, titulo, descricao, status, data_inicio, data_conclusao)
        print("Tarefa atualizada com sucesso!")
    except ValueError:
        print("Erro: valores inválidos inseridos.")
    except Exception as e:
        print("Erro ao atualizar tarefa:", e)


def remover_tarefa():
    try:
        id_val = int(input("Digite o ID da tarefa a ser removida: "))
        tar_repo.delete_tarefa(id_val)
        print("Tarefa removida com sucesso!")
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro ao remover tarefa:", e)
