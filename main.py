from banco_dados import autenticar_cliente, consultar_saldo, depositar, sacar

def login():
    while True:
        cpf = input('Digite seu CPF: ').strip()
        senha = input("Digite sua senha: ")

        cliente = autenticar_cliente(cpf, senha)

        if cliente is not None:
            print(f"Bem-vindo, {cliente[1]}!")
            return cliente

        print("CPF ou senha inválidos. tente novamente.")

def escolher_opcao():
    while True:
        try:
            opcao = int(input("""1-Depósito
2-Saque
3-Ver saldo
4-Histórico de transações
5-Trocar de conta
6-Sair
Escolha uma opção: """))
            return opcao
        except ValueError:
            print('Digite um número.')




cliente = login()

opcao = 0

while opcao != 6:

    opcao = escolher_opcao()

    if opcao == 1:

        try:
            valor = float(input("Digite o valor de depósito: R$"))

            if depositar(cliente[0], valor):
                print("Depósito realizado com sucesso!")
            else:
                print("Não foi possível realizar o depósito.")

        except ValueError:
            print("Digite um valor numérico válido.")

    elif opcao == 2:
        
        try:
            valor = float(input("Digite o valor do saque: R$"))

            if sacar(cliente[0], valor):
                
                print("Saque realizado com sucesso!")
            
            else:
                
                print("Não foi possível realizar o saque.")

        except ValueError:
            
            print("Digite um valor numérico válido.")
   
    elif opcao == 3:
        
        saldo = consultar_saldo(cliente[0])

        if saldo is not None:
            
            print(f"Nome: {cliente[1]}\nSaldo: R$ {saldo:.2f}")

        else:
            
            print("Não foi possivel consultar saldo")
        
    elif opcao == 4:

        if not cliente['historico']:
            
            print('Você não possui nenhuma transação.')
        
        else:
            
            for numero,transacao in enumerate(cliente['historico'], start=1):
            
                print(f'{numero}. {transacao}')
    
    elif opcao == 5:
        
        cliente = escolher_cliente()

    elif opcao == 6:
        
         print('Saindo...')

    else:
       
        print('Escolha uma opção válida')
    
    
    