from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
from utils import connect_to_database
import mysql.connector

# Definindo o Blueprint
professor_cadastro_bp = Blueprint('professor_cadastro_bp', __name__)

# Rota para exibir o formulário de cadastro de professor
@professor_cadastro_bp.route('/professor_cadastro', methods=['GET'])
def mostrar_formulario():
    return render_template('cadastro_professor.html')  # Certifique-se de que o arquivo 'cadastro_professor.html' está na pasta templates

# Rota para processar os dados do formulário via POST
@professor_cadastro_bp.route('/professor_cadastro', methods=['POST'])
def submit_formulario():
    # Capturando os dados do formulário
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    telefone = request.form['telefone']

    # Validando campos obrigatórios
    if not nome or not email or not senha or not telefone:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios!'}), 400

    # Criptografando a senha
    senha_hash = generate_password_hash(senha)

    # Preparando as queries SQL
    sql_usuario = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
    sql_professor = "INSERT INTO professor (idusuario, telefone) VALUES (%s, %s)"

    try:
        # Conectando ao banco de dados
        with connect_to_database() as mydb:
            mycursor = mydb.cursor()

            # Inserindo usuário na tabela 'usuarios'
            mycursor.execute(sql_usuario, (nome, email, senha_hash, 'professor'))
            idusuario = mycursor.lastrowid  # Obtendo o ID gerado

            # Inserindo na tabela 'professor' com o ID gerado
            mycursor.execute(sql_professor, (idusuario, telefone))
            mydb.commit()

            # Após o cadastro, redireciona para o formulário novamente
            return redirect(url_for('professor_cadastro_bp.mostrar_formulario'))

    except mysql.connector.Error as error:
        return jsonify({'error': f'Erro ao processar os dados: {str(error)}'}), 500
