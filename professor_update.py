from flask import Blueprint, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash

professor_update_bp = Blueprint('professor_update_bp', __name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'gerenciamento_escolar'

@professor_update_bp.route('/professor_update/<int:idusuario>/<string:tipo_usuario>', methods=['PUT'])
def atualizar_aluno(idusuario, tipo_usuario):
    # Verifica se o tipo_usuario é "administrador"
    if tipo_usuario != 'professor':
        return jsonify({'mensagem': 'Atualização permitida apenas para professores.'}), 403

    dados = request.json
    senha_criptografada = generate_password_hash(dados['senha'])  # Criptografa a nova senha

    sql = """
        UPDATE usuarios 
        SET nome = %s, email = %s, senha = %s 
        WHERE idusuario = %s AND tipo_usuario = %s
    """
    valores = (dados['nome'], dados['email'], senha_criptografada, idusuario, tipo_usuario)

    try:
        with mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        ) as mydb:
            mycursor = mydb.cursor()
            mycursor.execute(sql, valores)
            if mycursor.rowcount == 0:  # Nenhum registro atualizado
                return jsonify({'mensagem': 'Nenhum professor encontrado com este ID e tipo de usuário.'}), 404

            mydb.commit()
            return jsonify({'mensagem': 'Dados do professor atualizados com sucesso!'}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500
