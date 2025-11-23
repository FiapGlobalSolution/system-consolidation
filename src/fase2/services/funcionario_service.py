import repositories.funcionario_repository as func_repo

def cadastrar_funcionario():
    try:
        nome   = input("Digite o nome: ")
        funcao = input("Digite a função: ")

        func_repo.post_funcionario(nome, funcao)
        print("Cadastrado com sucesso!")

    except ValueError:
        print("Erro: valores inválidos inseridos.")

def consultar_funcionario():
    try: 
        todos = input("Deseja consultar todos os funcionários? (s/n): ")
        if todos.lower() == 's':
            result = func_repo.get_funcionarios()
        else:
            campo = input("Digite o campo para consulta (id, nome, funcao): ")
            valor = input("Digite o valor para consulta: ")

            if campo == 'id':
                result = func_repo.get_funcionario_por_id(valor)
            elif campo == 'nome':
                result = func_repo.get_funcionario_por_nome(valor)
            elif campo == 'funcao':
                result = func_repo.get_funcionarios_por_funcao(valor)
            else:
                print("Campo inválido. Tente novamente.")

        if result is not None:
            print("Resultado da consulta:")
            for row in result:
                id, nome, funcao = row
                print(f"Id: {id}, Nome: {nome}, Função: {funcao}")
        else:
            print("Nenhum resultado encontrado.")
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro na consulta:", e)

def atualizar_funcionario():
    try:
        id_funcionario = input("Digite o ID do funcionário: ")
        campo = input("Digite o campo para atualização (nome, funcao): ")
        novo_valor = input("Digite o novo valor: ")

        func_repo.update_funcionario(id_funcionario, campo, novo_valor)
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro na atualização:", e)

def remover_funcionario():
    try:
        id_funcionario = input("Digite o ID do funcionário: ")

        func_repo.delete_funcionario(id_funcionario)
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro na remoção:", e)