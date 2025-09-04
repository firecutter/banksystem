class ContaBase:
    def __init__(self, numero_conta, titular, saldo_inicial=0):
        self.numero_conta = numero_conta
        self.titular = titular
        self.saldo = saldo_inicial
        self.historico = []  # Guardar transações

    def registrar_transacao(self, descricao):
        self.historico.append(descricao)

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            descricao = f"Depósito de R${valor:.2f}"
            self.registrar_transacao(descricao)
            print(descricao + " realizado com sucesso.")
        else:
            print("Valor de depósito inválido.")

    def sacar(self, valor):
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            descricao = f"Saque de R${valor:.2f}"
            self.registrar_transacao(descricao)
            print(descricao + " realizado com sucesso.")
        else:
            print("Saldo insuficiente ou valor de saque inválido.")

    def consultar_saldo(self):
        print(f"Saldo atual: R${self.saldo:.2f}")

    def exibir_historico(self):
        print("\n📜 Histórico de transações:")
        if not self.historico:
            print("Nenhuma transação registrada.")
        else:
            for i, transacao in enumerate(self.historico, start=1):
                print(f"{i}. {transacao}")


class ContaCorrente(ContaBase):
    def transferir(self, valor, conta_destino):
        if not isinstance(conta_destino, ContaCorrente):
            print("Transferência permitida apenas entre contas correntes.")
            return

        if 0 < valor <= self.saldo:
            self.sacar(valor)
            conta_destino.depositar(valor)
            descricao = f"Transferência de R${valor:.2f} para conta {conta_destino.numero_conta}"
            self.registrar_transacao(descricao)
            conta_destino.registrar_transacao(f"Recebido {descricao}")
            print(descricao + " realizada com sucesso.")
        else:
            print("Saldo insuficiente ou valor de transferência inválido.")


class ContaPoupanca(ContaBase):
    def aplicar_juros(self, taxa_juros):
        if taxa_juros > 0:
            juros = self.saldo * (taxa_juros / 100)
            self.saldo += juros
            descricao = f"Juros de R${juros:.2f} aplicados"
            self.registrar_transacao(descricao)
            print(descricao + " com sucesso.")
        else:
            print("Taxa de juros inválida.")


class CadastroCliente:
    def __init__(self, nome, cpf, endereco, telefone):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.telefone = telefone

    def atualizar_endereco(self, novo_endereco):
        self.endereco = novo_endereco
        print("Endereço atualizado com sucesso.")

    def atualizar_telefone(self, novo_telefone):
        self.telefone = novo_telefone
        print("Telefone atualizado com sucesso.")

    def exibir_informacoes(self):
        print(f"Nome: {self.nome}")
        print(f"CPF: {self.cpf}")
        print(f"Endereço: {self.endereco}")
        print(f"Telefone: {self.telefone}")

    def criar_conta(self, tipo_conta, numero_conta, saldo_inicial=0):
        if tipo_conta.lower() == "corrente":
            return ContaCorrente(numero_conta, self.nome, saldo_inicial)
        elif tipo_conta.lower() == "poupança":
            return ContaPoupanca(numero_conta, self.nome, saldo_inicial)
        else:
            print("Tipo de conta inválido.")
            return None


# ---------------- MENU INTERATIVO ---------------- #

clientes = {}
contas = {}

def menu():
    while True:
        print("\n===== SISTEMA BANCÁRIO =====")
        print("1 - Cadastrar cliente")
        print("2 - Criar conta")
        print("3 - Depositar")
        print("4 - Sacar")
        print("5 - Transferir (apenas corrente → corrente)")
        print("6 - Consultar saldo")
        print("7 - Aplicar juros (poupança)")
        print("8 - Exibir informações do cliente")
        print("9 - Exibir histórico de transações")
        print("10 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            endereco = input("Endereço: ")
            telefone = input("Telefone: ")
            clientes[cpf] = CadastroCliente(nome, cpf, endereco, telefone)
            print("Cliente cadastrado com sucesso.")

        elif opcao == "2":
            cpf = input("Informe o CPF do cliente: ")
            if cpf in clientes:
                tipo = input("Tipo de conta (corrente/poupança): ")
                numero_conta = input("Número da conta: ")
                saldo = float(input("Saldo inicial: "))
                conta = clientes[cpf].criar_conta(tipo, numero_conta, saldo)
                if conta:
                    contas[numero_conta] = conta
                    print("Conta criada com sucesso.")
            else:
                print("Cliente não encontrado.")

        elif opcao == "3":
            numero = input("Número da conta: ")
            if numero in contas:
                valor = float(input("Valor do depósito: "))
                contas[numero].depositar(valor)
            else:
                print("Conta não encontrada.")

        elif opcao == "4":
            numero = input("Número da conta: ")
            if numero in contas:
                valor = float(input("Valor do saque: "))
                contas[numero].sacar(valor)
            else:
                print("Conta não encontrada.")

        elif opcao == "5":
            origem = input("Número da conta de origem (corrente): ")
            destino = input("Número da conta de destino (corrente): ")
            if origem in contas and destino in contas:
                valor = float(input("Valor da transferência: "))
                contas[origem].transferir(valor, contas[destino])
            else:
                print("Conta de origem ou destino não encontrada.")

        elif opcao == "6":
            numero = input("Número da conta: ")
            if numero in contas:
                contas[numero].consultar_saldo()
            else:
                print("Conta não encontrada.")

        elif opcao == "7":
            numero = input("Número da conta poupança: ")
            if numero in contas and isinstance(contas[numero], ContaPoupanca):
                taxa = float(input("Taxa de juros (%): "))
                contas[numero].aplicar_juros(taxa)
            else:
                print("Conta não encontrada ou não é poupança.")

        elif opcao == "8":
            cpf = input("Informe o CPF do cliente: ")
            if cpf in clientes:
                clientes[cpf].exibir_informacoes()
            else:
                print("Cliente não encontrado.")

        elif opcao == "9":
            numero = input("Número da conta: ")
            if numero in contas:
                contas[numero].exibir_historico()
            else:
                print("Conta não encontrada.")

        elif opcao == "10":
            print("Saindo do sistema. Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")


# Executa o menu
menu()
