from banco_dados import gerar_hash_senha, validar_cpf_completo, buscar_cliente_por_id, validar_segundo_digito, validar_primeiro_digito, buscar_cliente,validar_cpf, depositar, sacar, consultar_saldo, cadastrar_cliente,  fechar_conexao
from banco_dados import autenticar_cliente


from banco_dados import buscar_cliente, autenticar_cliente, cursor

# Localiza o cliente de teste pelo nome

from banco_dados import (
    cursor,
    buscar_cliente,
    verificar_senha,
    autenticar_cliente
)

cursor.execute("""
    SELECT nome, cpf
    FROM cliente
    WHERE nome = 'Cliente Hash'
""")

print(cursor.fetchone())
# Buscar o cliente de teste
cursor.execute(
    "SELECT cpf FROM cliente WHERE nome = ?",
    ("Cliente Hash",)
)

resultado = cursor.fetchone()

if resultado is None:
    print("ERRO: Cliente Hash não encontrado.")
else:
    cpf = resultado[0]
    cliente = buscar_cliente(cpf)

    # Recuperar salt e hash do banco
    salt, hash_armazenado = cliente[3].split(":", 1)

    print("Cliente encontrado:", cliente is not None)
    print("Nome:", cliente[1])
    print("Formato salt:hash:", True)

    # Testar diretamente a senha
    print(
        "Verificação direta:",
        verificar_senha("senha123", salt, hash_armazenado)
    )

    # Testar a função de autenticação
    print(
        "Login correto:",
        autenticar_cliente(cpf, "senha123") is not None
    )

    print(
        "Senha incorreta rejeitada:",
        autenticar_cliente(cpf, "senha_errada") is None
    )




fechar_conexao()