# Sistema Bancário em POO - Python

Este repositório contém a minha resolução para o desafio de projeto
"Modelando um Sistema Bancário em POO com Python", parte do Bootcamp
da LuizaLabs pela **DIO (Digital Innovation One)**.

## Objetivo do Projeto

O objetivo principal foi converter um sistema bancário estrutural em um
sistema completamente Orientado a Objetos, seguindo um diagrama de classes UML fornecido.

Para garantir a máxima fixação do aprendizado, **este código foi
construído inteiramente do zero**, sem a cópia de gabaritos, focando
em entender o porquê de cada decisão arquitetural.

## Conceitos e Práticas Aplicadas

**Abstração (ABC):** `Transacao` é definida como classe abstrata,
garantindo que qualquer nova transação futura seja obrigada a
implementar o método `registrar()`.

**Encapsulamento:** Atributos sensíveis como `_saldo` e `_historico`
são protegidos com `_` e expostos de forma controlada via `@property`,
evitando modificações externas acidentais.

**Herança:** Hierarquias lógicas com reuso via `super().__init__()` —
`PessoaFisica` herda de `Cliente` e `ContaCorrente` herda de `Conta`.

**Polimorfismo:** `Saque` e `Deposito` implementam o mesmo método
`registrar(conta)` da interface `Transacao`, mas com comportamentos
distintos. Isso permite que `Cliente.realizar_transacao()` execute
qualquer tipo de transação sem precisar saber qual é.

**Factory Method (`nova_conta`):** Criação de contas centralizada via
`@classmethod`, permitindo que subclasses criem instâncias de si
mesmas sem expor o construtor diretamente.

**Design Defensivo (Early Return):** Blocos condicionais estruturados
para barrar cenários de erro antes da lógica principal, garantindo que
o estado da conta nunca fique inconsistente.

## Como testar o sistema

No final do arquivo, há uma suíte de testes manual simulando o
comportamento de um usuário real. Os cenários cobertos são:

1. Instanciação do cliente e da conta corrente
2. Depósito válido
3. Saque válido dentro do limite de saldo
4. Bloqueio por valor excedente ao limite por transação
5. Bloqueio por limite diário de saques estourado

Para rodar na sua máquina, clone o repositório e execute:

```bash
python dados_banco.py
```
