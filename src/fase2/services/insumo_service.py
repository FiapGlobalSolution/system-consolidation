import repositories.insumo_repository as insu_repo
from datetime import datetime

def cadastrar_insumo():
    try:
        nome = input("Digite o nome: ")
        quantidade = int(input("Digite a quantidade de pacotes: "))
        data_validade = input("Digite a data de validade (dd/mm/aaaa): ")
        data_validade = datetime.strptime(data_validade, "%d/%m/%Y")
        if quantidade <= 0:
            raise ValueError("Quantidade inválida.")
        peso = float(input("Digite o peso de cada pacote em Kg: "))
        if peso <= 0:
            raise ValueError("Peso inválido.")
        tipo = input("Digite o tipo do insumo (semente, adubo, defensivo): ")
        tipo = tipo.lower()
        if tipo not in ["semente", "adubo", "defensivo"]:
            raise ValueError("Tipo de insumo inválido.")

        insu_repo.post_insumo(nome, quantidade, peso, tipo, data_validade)
        print("Cadastrado com sucesso!")

    except ValueError as e:
        print("Erro: valores inválidos inseridos.", e)
    except Exception as e:
        print("Erro na transação:", e)

def consultar_insumo():
    try: 
        todos = input("Deseja consultar todos os insumos? (s/n): ")
        if todos.lower() == 's':
            result = insu_repo.get_insumos()
        else:
            campo = input("Digite o campo para consulta (id, nome, tipo, data_validade): ")
            valor = input("Digite o valor para consulta: ")

            if campo == 'id':
                result = insu_repo.get_insumo_por_id(valor)
            elif campo == 'nome':
                result = insu_repo.get_insumo_por_nome(valor)
            elif campo == 'tipo':
                result = insu_repo.get_insumos_por_tipo(valor)
            elif campo == 'data_validade':
                valor = datetime.strptime(valor, "%d/%m/%Y")
                result = insu_repo.get_insumos_por_data_validade(valor)
            else:
                print("Campo inválido. Tente novamente.")

        if result is not None:
            print("Resultado da consulta:")
            for row in result:
                id, nome, tipo, quantidade, peso, data_validade = row
                data_validade = data_validade.strftime("%d/%m/%Y")
                print(f"Id: {id}, Nome: {nome}, Tipo: {tipo}, Quantidade: {quantidade}, Peso: {peso}, Validade: {data_validade}")
        else:
            print("Nenhum resultado encontrado.")
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro na consulta:", e)

def atualizar_insumo():
    try:
        id_insumo = input("Digite o ID do insumo: ")
        campo = input("Digite o campo para atualização (nome, quantidade, peso, tipo, data_validade): ")
        novo_valor = input("Digite o novo valor: ")

        if campo == 'data_validade':
            valor = datetime.strptime(valor, "%d/%m/%Y")

        insu_repo.update_insumo(id_insumo, campo, novo_valor)
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro na atualização:", e)

def remover_insumo():
    try:
        id_insumo = input("Digite o ID do insumo: ")

        insu_repo.delete_insumo(id_insumo)
    except ValueError:
        print("Erro: valor inválido inserido.")
    except Exception as e:
        print("Erro na remoção:", e)