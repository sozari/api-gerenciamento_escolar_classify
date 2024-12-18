from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
from utils import connect_to_database
import mysql.connector

# Definindo o Blueprint
aluno_cadastro_bp = Blueprint('aluno_cadastro_bp', __name__)

# Rota para exibir o formulário de cadastro de aluno
@aluno_cadastro_bp.route('/aluno_cadastro', methods=['GET'])
def mostrar_formulario():
    try:
        with connect_to_database() as mydb:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT idturma, nome_turma FROM turmas")
            turmas = mycursor.fetchall()  # Retorna lista de turmas

        return render_template('cadastro_aluno.html', turmas=turmas)  # Passa a lista de turmas para o template
    except mysql.connector.Error as error:
        return jsonify({'error': f'Erro ao carregar formulário: {error}'}), 500

# Rota para processar os dados do formulário
@aluno_cadastro_bp.route('/aluno_cadastro', methods=['POST'])
def submit_formulario():
    try:
        # Captura dos dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        telefone_responsavel = request.form['telefone_responsavel']
        idturma = request.form['idturma']

        print("Dados recebidos:", nome, email, senha, telefone_responsavel, idturma)

        # Criptografia da senha
        senha_hash = generate_password_hash(senha)

        # Queries SQL
        sql_usuario = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
        sql_aluno = "INSERT INTO aluno (idusuario, telefone_responsavel, idturma) VALUES (%s, %s, %s)"
        sql_notas = """
        INSERT INTO notas (idusuario, idturma, nota1, nota2, nota3, media)
        VALUES (%s, %s, NULL, NULL, NULL, NULL)
        """

        with connect_to_database() as mydb:
            mycursor = mydb.cursor()

            # Inserção na tabela 'usuarios'
            print("Executando query de usuario")
            mycursor.execute(sql_usuario, (nome, email, senha_hash, 'aluno'))
            idusuario = mycursor.lastrowid  # Obtém o ID do usuário
            print("Usuario inserido com ID:", idusuario)

            # Inserção na tabela 'aluno'
            print("Executando query de aluno")
            mycursor.execute(sql_aluno, (idusuario, telefone_responsavel, idturma))

            # Inserção na tabela 'notas'
            print("Executando query de notas")
            mycursor.execute(sql_notas, (idusuario, idturma))

            # Confirma alterações
            mydb.commit()
            print("Cadastro concluído com sucesso!")

            return redirect(url_for('aluno_cadastro_bp.mostrar_formulario'))

    except mysql.connector.Error as error:
        print("Erro ao cadastrar aluno:", error)
        return jsonify({'error': f'Erro ao cadastrar aluno: {error}'}), 500

