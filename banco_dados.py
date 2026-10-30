import sqlite3
import hashlib
import secrets

conexao = sqlite3.connect('banco_dados.db')

cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        saldo REAL NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        valor REAL NOT NULL,
        data DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (cliente_id) REFERENCES cliente(id)
    )
""")

conexao.commit()

def gerar_hash_senha(senha):
    salt = secrets.token_bytes(16)

    hash_senha = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt,
        600000
    )

    return salt.hex(), hash_senha.hex()

def verificar_senha(senha_digitada, salt, hash_armazenado):
    salt_bytes = bytes.fromhex(salt)

    hash_calculado = hashlib.pbkdf2_hmac(
        "sha256",
        senha_digitada.encode("utf-8"),
        salt_bytes,
        600000
    )

    return secrets.compare_digest(
        hash_calculado.hex(),
        hash_armazenado
    )

def autenticar_cliente(cpf, senha_digitada):
    cliente = buscar_cliente(cpf)

    if cliente is None:
        return None

    senha_armazenada = cliente[3]

    if ":" not in senha_armazenada:
        return None

    salt, hash_armazenado = senha_armazenada.split(":", 1)

    senha_valida = verificar_senha(
        senha_digitada,
        salt,
        hash_armazenado
    )

    if senha_valida:
        return cliente

    return None

def validar_cpf_completo(cpf):
    if not validar_cpf(cpf):
        return False

    if not validar_primeiro_digito(cpf):
        return False

    if not validar_segundo_digito(cpf):
        return False

    return True

def validar_segundo_digito(cpf):
    numeros = cpf[:10]

    soma = 0

    for indice, numero in enumerate(numeros):
        
        peso = 11 - indice
        
        soma += int(numero) * peso
    
    resto = soma % 11

    if resto < 2:
        digito = 0
    else:
        digito = 11 - resto
    
    segundo_digito = int(cpf[10])
    
    if digito == segundo_digito:
        return True
    else:
        return False
    
    print(digito)

def validar_primeiro_digito(cpf):
    numeros = cpf[:9]

    soma = 0

    for indice, numero in enumerate(numeros):
        peso = 10 - indice
        soma += int(numero) * peso

    resto = soma % 11

    if resto < 2:
        digito = 0
    else:
        digito = 11 - resto

    primeiro_digito = int(cpf[9])

    if digito == primeiro_digito:
        return True
    else:
        return False

    print(digito)

def validar_cpf(cpf):
    if len(cpf) != 11:
        return False
    if not cpf.isdigit():
        return False

    return True

def cadastrar_cliente(nome, cpf, senha, saldo_inicial):

    if type(saldo_inicial) not in (int, float):
        print("Digite apenas números.")
        return

    if saldo_inicial < 0:
        print("O saldo inicial não pode ser menor que 0.")
        return

    if not nome.strip() or not cpf.strip() or not senha.strip():
        print('Preencha os campos nome, CPF e senha para continuar')
        return

    if not validar_cpf_completo(cpf):
        print("CPF inválido.")
        return
    
    try:

        salt, hash_senha = gerar_hash_senha(senha)
        cursor.execute("""
            INSERT INTO cliente (nome, cpf, senha, saldo)
            VALUES (?, ?, ?, ?)
    """,(nome, cpf, f"{salt}:{hash_senha}", saldo_inicial))
        conexao.commit()
        print("Cliente cadastrado com sucesso!")
    
    except sqlite3.IntegrityError:
        print("Este CPF  já está cadastrado")

def buscar_cliente(cpf):
    cursor.execute(
        "SELECT * FROM cliente WHERE cpf = ?",
        (cpf,)
    )
    return cursor.fetchone()

def buscar_cliente_por_id(cliente_id):
    
    if cliente_id <= 0:
        return
    cursor.execute(
        "SELECT * FROM cliente WHERE id = ?",
        (cliente_id,)
)

    #recupera o resultado da consulta
    cliente = cursor.fetchone()

    if cliente is None:
        return

    return cliente

def depositar(cliente_id, valor):

    if valor <= 0:
        print("O valor do depósito deve ser maior que zero.")
        return False

    cliente_existe = buscar_cliente_por_id(cliente_id)

    if cliente_existe is None:
        print("Cliente inexistente")
        return False
    
    cursor.execute("""
        UPDATE cliente
        SET saldo = saldo + ?
        WHERE id = ?
""", (valor, cliente_id))

    cursor.execute("""
    INSERT INTO transacoes (cliente_id, tipo, valor)
    VALUES (?, ?, ?)
""", (cliente_id, "Depósito", valor))
    
    conexao.commit()
    return True

def sacar(cliente_id, valor):
    
    if valor <= 0:
        
        print('O valor do saque deve ser maior que zero.')
        
        return False
    
    cliente = buscar_cliente_por_id(cliente_id)

    if cliente is None:
        print("Cliente não encontrado.")
        return False

    saldo_atual = cliente[4]
    
    if saldo_atual >= valor:
        cursor.execute("""
        UPDATE cliente
        SET saldo = saldo - ?
        WHERE id = ?

    """, (valor, cliente_id))

        cursor.execute("""
        INSERT INTO transacoes (cliente_id, tipo, valor)
        VALUES (?, ?, ?)
    """, (cliente_id, "Saque", valor))

        conexao.commit()
        return True
    
    else:
        print('Saldo insuficiente')
        return False

def consultar_saldo(cliente_id):

    cliente = buscar_cliente_por_id(cliente_id)

    if cliente is None:
        return None

    saldo_conta = cliente[4]

    return saldo_conta

def fechar_conexao():
    conexao.close()
