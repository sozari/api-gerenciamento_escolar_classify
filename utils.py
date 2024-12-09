import mysql.connector

# Função para conectar ao banco de dados
def connect_to_database():
    db_host = 'localhost'  # Endereço do banco de dados
    db_user = 'root'       # Usuário do banco
    db_password = ''       # Senha do banco
    db_name = 'gerenciamento_escolar'  # Nome do banco de dados

    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
