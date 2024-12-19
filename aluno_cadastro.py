from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
from utils import connect_to_database
import mysql.connector

# Definindo o Blueprint
aluno_cadastro_bp = Blueprint('aluno_cadastro_bp', __name__)

@aluno_cadastro_bp.route('/aluno_cadastro', methods=['GET'])
def mostrar_formulario():
    try:
        with connect_to_database() as mydb:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT idturma, nome_turma FROM turmas")
            turmas = mycursor.fetchall()
        return render_template('cadastro_aluno.html', turmas=turmas)
    except mysql.connector.Error as error:
        print(f"Erro ao carregar o formulário: {error}")
        return jsonify({'error': f"Erro ao carregar o formulário: {str(error)}"}), 500

@aluno_cadastro_bp.route('/aluno_cadastro', methods=['POST'])
def submit_formulario():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    telefone_responsavel = request.form['telefone_responsavel']
    idturma = request.form['idturma']

    if not nome or not email or not senha or not telefone_responsavel or not idturma:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios!'}), 400

    senha_hash = generate_password_hash(senha)

    # Queries SQL corrigidas
    sql_usuario = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
    sql_aluno = "INSERT INTO aluno (idusuario, telefone_responsavel, idturma) VALUES (%s, %s, %s)"
    sql_notas = "INSERT INTO notas (idusuario, idturma) VALUES (%s, %s)"

    try:
        with connect_to_database() as mydb:
            mycursor = mydb.cursor()

            # Inserindo na tabela 'usuarios'
            mycursor.execute(sql_usuario, (nome, email, senha_hash, 'aluno'))
            idusuario = mycursor.lastrowid  # Capturando o ID gerado
            print(f"Usuário inserido com ID: {idusuario}")

            # Inserindo na tabela 'aluno'
            mycursor.execute(sql_aluno, (idusuario, telefone_responsavel, idturma))
            print(f"Aluno inserido com idusuario={idusuario} e idturma={idturma}")

            # Inserindo na tabela 'notas'
            mycursor.execute(sql_notas, (idusuario, idturma))
            print(f"Notas iniciais criadas para idusuario={idusuario} e idturma={idturma}")

            # Confirmando transações
            mydb.commit()
            print("Cadastro finalizado com sucesso!")

            return redirect(url_for('aluno_cadastro_bp.mostrar_formulario'))

    except mysql.connector.Error as error:
        print(f"Erro no banco de dados: {error}")
        return jsonify({'error': f"Erro ao cadastrar aluno: {str(error)}"}), 500

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({'error': f"Erro inesperado: {str(e)}"}), 500
