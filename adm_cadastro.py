from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
from utils import connect_to_database
import mysql.connector

# Definindo o Blueprint
adm_cadastro_bp = Blueprint('adm_cadastro_bp', __name__)

# Rota para exibir o formulário de cadastro de administrador
@adm_cadastro_bp.route('/adm_cadastro', methods=['GET'])
def mostrar_formulario():
    return render_template('cadastro_adm.html')  # Certifique-se de que o arquivo 'cadastro_adm.html' está na pasta templates

# Rota para processar os dados do formulário via POST
@adm_cadastro_bp.route('/adm_cadastro', methods=['POST'])
def submit_formulario():
    # Capturando os dados do formulário
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    # Validando campos obrigatórios
    if not nome or not email or not senha:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios!'}), 400

    # Criptografando a senha
    senha_hash = generate_password_hash(senha)

    # Preparando a query SQL
    sql_usuario = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"

    try:
        # Conectando ao banco de dados
        with connect_to_database() as mydb:
            mycursor = mydb.cursor()

            # Inserindo usuário na tabela 'usuarios'
            mycursor.execute(sql_usuario, (nome, email, senha_hash, 'administrador'))
            mydb.commit()

            # Após o cadastro, redireciona para o formulário novamente
            return redirect(url_for('adm_cadastro_bp.mostrar_formulario'))

    except mysql.connector.Error as error:
        return jsonify({'error': f'Erro ao processar os dados: {str(error)}'}), 500
