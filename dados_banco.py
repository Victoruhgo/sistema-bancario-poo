from abc import ABC, abstractmethod

class Transacao(ABC):
    
    @abstractmethod
    def registrar (self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar (self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    def registrar (self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)

class Historico():
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)
    
    @property
    def transacoes(self):
        return list(self._transacoes)

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco): # endereco aqui porque herda de Cliente
        super().__init__(endereco) # Usa o construtor do Cliente para montar o mesmo objeto
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()
        self._agencia = "0001"
        self._saldo = 0
    
    @property
    def historico(self):
        return self._historico

    @property
    def saldo(self):
        return self._saldo
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
        
        if valor > self._saldo: # Early Return
            print("Saldo insuficiente!")
            return False
        
        elif valor <= 0:
            print("Valor inserido é inválido, tente novamente por favor")
            return False
            
        else: # Após testar os cenários, continua a operação
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
            return True
        else:
            print("Valor inserido é inválido, tente novamente por favor")
            return False
        
class ContaCorrente(Conta):
    def __init__(self, limite, limite_saques, numero, cliente):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0

    def sacar(self, valor): # Override para substituir o da classe mãe
        if valor <= 0:
            print("Valor inválido")
            return False
         
        if valor > self._saldo: # Early Return
            print("Valor excede o seu saldo atual!")
            return False
        
        elif valor > self._limite:
            print(f"Saque de R$ {valor:.2f} bloqueado! Limite por transação: R$ {self._limite:.2f}")
            return False
        
        elif self._numero_saques >= self._limite_saques:
            print("Número de saques excede o seu limite permitido")
            return False
        
        sucesso = super().sacar(valor)  # delega a dedução do saldo ao pai
        if sucesso:
            self._numero_saques += 1
        return sucesso
        
if __name__ == "__main__":
    print("=== INICIANDO TESTES DO SISTEMA BANCÁRIO ===")

    # Criar o Cliente (PessoaFisica)
    # Argumentos sempre na ordem do construtor: cpf, nome, data_nascimento, endereco
    cliente = PessoaFisica("123.456.789-00", "Victor Hugo", "10/10/2004", "Piracicaba, SP")

    # Criar a Conta Corrente vinculada a esse cliente
    # Números fictícios apenas para teste
    conta = ContaCorrente(limite=500.0, limite_saques=3, numero=1001, cliente=cliente)

    # Registrar a conta dentro da lista de contas do cliente
    cliente.adicionar_conta(conta)


    # Cenário 1: Teste de depósito pelo cliente
    print("\nRealizando depósito de R$ 1000.00...")
    deposito = Deposito(1000.0)
    # O cliente delega a ação para a transação rodar na conta
    cliente.realizar_transacao(conta, deposito)
    print(f"Saldo atual: R$ {conta.saldo:.2f}")


    # Cenário 2: Teste de saque válido ou não
    print("\nRealizando saque válido de R$ 200.00...")
    saque_valido = Saque(200.0)
    cliente.realizar_transacao(conta, saque_valido)
    print(f"Saldo atual: R$ {conta.saldo:.2f}")


    # Cenário 3: Bloqueio por exceder o limite
    print("\nTentativa de saque R$ 600.00")
    saque_alto = Saque(600.0)
    cliente.realizar_transacao(conta, saque_alto)
    print(f"Saldo atual: R$ {conta.saldo:.2f}")


    # Cenário 4: Bloqueio por exceder o limite de saques
    print("\nForçando o limite de saques diários...") # Máximo estipulado foram 3
    # Até aqui contamos já 1 saque válido com sucesso (Cenário 2)
    print("-> Executando o 2º saque válido...")
    cliente.realizar_transacao(conta, Saque(50.0))
    
    print("-> Executando o 3º saque válido...")
    cliente.realizar_transacao(conta, Saque(50.0))
    
    print("-> Tentando o 4º saque do dia...") # Deve ser bloqueado por quantidade
    cliente.realizar_transacao(conta, Saque(50.0))
    
    print(f"Saldo final: R$ {conta.saldo:.2f}")