clientes = [{ 
    'nome' : 'João Miguel Lages',
    'cpf'  : '15042045732',
    'senha': '12345',
    'saldo': 1000,
    'historico' : []
},
{
    'nome' : 'Jade Picon',
    'cpf'  : '12345678901',
    'senha': '12345',
    'saldo': 1300,
    'historico' : []
}]

def escolher_cliente():
    
    while True:

        try:
        
            cliente = int(input('0 - joao\n1 - jade\nQual cliente?'))

        except ValueError:

            print('Digite um número válido')

            continue

        if cliente == 0:
            cliente = clientes[0]
            break

        elif cliente == 1:
            cliente = clientes[1]
            break

        else:
            print('Escolha uma opção válida')
            
    return cliente
