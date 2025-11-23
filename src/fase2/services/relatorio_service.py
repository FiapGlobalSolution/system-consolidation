import repositories.relatorio_repository as rel_repo

def cadastrar_relatorio():
    try:
        nome = input("Digite o nome do relatório: ")
        tipo = input("Digite o tipo de relatório: ")
        descricao = input("Digite a descrição (ou deixe vazio): ") or None
        data_geracao = input("Digite a data de geração (YYYY-MM-DD): ")

        rel_repo.post_relatorio(nome, tipo, descricao, data_geracao)
        print("Relatório cadastrado com sucesso!")
    except ValueError:
        print("Erro: valores inválidos inseridos.")
    except Exception as e:
        print("Erro ao cadastrar relatório:", e)


def consultar_relatorio():
    try:
        todos = input("Deseja consultar todos os relatórios? (s/n): ")
        if todos.lower() == 's':
            resultados = rel_repo.get_all_relatorios()
        else:
            id_val = int(input("Digite o ID do relatório: "))
            resultados = rel_repo.get_relatorio_by_id(id_val)

        if resultados:
            print("Resultado da consulta:")
            if isinstance(resultados, list):
                for row in resultados:
                    print(f"ID: {row[0]}, Nome: {row[1]}, Tipo: {row[2]}, Descrição: {row[3]}, Gerado em: {row[4]}")
            else:
                row = resultados
                print(f"ID: {row[0]}, Nome: {row[1]}, Tipo: {row[2]}, Descrição: {row[3]}, Gerado em: {row[4]}")
        else:
            print("Nenhum relatório encontrado.")
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro na consulta de relatórios:", e)


def update_relatorio():
    try:
        id_val = int(input("Digite o ID do relatório a ser atualizado: "))
        nome = input("Digite o novo nome: ")
        tipo = input("Digite o novo tipo: ")
        descricao = input("Digite a nova descrição (ou deixe vazio): ") or None
        data_geracao = input("Digite a nova data de geração (YYYY-MM-DD): ")

        rel_repo.update_relatorio(id_val, nome, tipo, descricao, data_geracao)
        print("Relatório atualizado com sucesso!")
    except ValueError:
        print("Erro: valores inválidos inseridos.")
    except Exception as e:
        print("Erro ao atualizar relatório:", e)


def delete_relatorio():
    try:
        id_val = int(input("Digite o ID do relatório a ser removido: "))
        rel_repo.delete_relatorio(id_val)
        print("Relatório removido com sucesso!")
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro ao remover relatório:", e)