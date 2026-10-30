def sacar(cliente):

    while True:        
        
        try:

            valor_saque = float(input('Qual valor deseja sacar:'))
        except ValueError:
            
            print('Digite um valor válido')
            
            continue

        #verificanco se se o valor não é <= 0 
        if valor_saque <= 0:
            
            print('Digite um valor válido.')
        
        #verificando se o valor de saque ñ é > q o valor de saldo
        elif cliente['saldo'] < valor_saque:
            
            print('Saldo insuficiente.')
        
        else:
            
            cliente['saldo'] = cliente['saldo'] - valor_saque

            cliente['historico'].append(f"Saque: R$ {valor_saque:.2f} | Saldo após operação: R$ {cliente ['saldo']:.2f}")
            
            print(f'Saque de R$ {valor_saque:.2f} efetuado com sucesso!')
            
            print(f"Saldo:{cliente['saldo']:.2f}")
            
            break

def depositar(cliente):
    
    while True:    

       
        try:
            
            valor = float(input('Digite o valor que deseja depositar: '))
         
        except ValueError:
            
            print('Você deve digitar um número.')
            
            continue
        
        if valor <= 0:
            
            print('Deposite um valor válido.')

        else:
        
            cliente['saldo'] = cliente['saldo'] + valor

            cliente['historico'].append(f"Depósito: R$ {valor:.2f} | Saldo após operação: R$ {cliente['saldo']:.2f}")

            print(f"{cliente['saldo']:.2f}")
            
            break