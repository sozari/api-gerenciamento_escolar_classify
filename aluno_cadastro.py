from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
from utils import connect_to_database
import mysql.connector

# Definindo o Blueprint
aluno_cadastro_bp = Blueprint('aluno_cadastro_bp', __name__)

# Rota para exibir o formulário de cadastro de aluno
@aluno_cadastro_bp.route('/aluno_cadastro', methods=['GET'])
def mostrar_formulario():
    return render_template('cadastro_aluno.html')  # Certifique-se de que o arquivo 'cadastro_aluno.html' está na pasta templates

# Rota para processar os dados do formulário via POST
@aluno_cadastro_bp.route('/aluno_cadastro', methods=['POST'])
def submit_formulario():
    # Capturando os dados do formulário
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    telefone_responsavel = request.form['telefone_responsavel']

    # Validando campos obrigatórios
    if not nome or not email or not senha or not telefone_responsavel:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios!'}), 400

    # Criptografando a senha
    senha_hash = generate_password_hash(senha)

    # Preparando as queries SQL
    sql_usuario = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
    sql_aluno = "INSERT INTO aluno (idusuario, telefone_responsavel) VALUES (%s, %s)"

    try:
        # Conectando ao banco de dados
        with connect_to_database() as mydb:
            mycursor = mydb.cursor()

            # Inserindo usuário na tabela 'usuarios'
            mycursor.execute(sql_usuario, (nome, email, senha_hash, 'aluno'))
            idusuario = mycursor.lastrowid  # Obtendo o ID gerado

            # Inserindo na tabela 'aluno' com o ID gerado
            mycursor.execute(sql_aluno, (idusuario, telefone_responsavel))
            mydb.commit()

            # Após o cadastro, redireciona para o formulário novamente
            return redirect(url_for('aluno_cadastro_bp.mostrar_formulario'))

    except mysql.connector.Error as error:
        return jsonify({'error': f'Erro ao processar os dados: {str(error)}'}), 500
