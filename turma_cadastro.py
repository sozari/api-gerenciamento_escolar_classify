from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from utils import connect_to_database
import mysql.connector

# Definindo o Blueprint
turma_cadastro_bp = Blueprint('turma_cadastro_bp', __name__)

# Rota para exibir o formulário de cadastro de turma
@turma_cadastro_bp.route('/turma_cadastro', methods=['GET'])
def mostrar_formulario():
    # Obtém a lista de usuários do tipo 'professor' da tabela 'usuarios'
    with connect_to_database() as mydb:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT idusuario, nome FROM usuarios WHERE tipo_usuario = 'professor'")
        professores = mycursor.fetchall()

    return render_template('cadastro_turma.html', professores=professores)

# Rota para processar o formulário via POST
@turma_cadastro_bp.route('/cadastro_turma', methods=['POST'])
def submit_formulario():
    nome_turma = request.form['nome_turma']
    idprofessor = request.form['idprofessor']

    # Validando os campos
    if not nome_turma or not idprofessor:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios!'}), 400

    # Preparando a query para inserir a turma
    sql_turma = "INSERT INTO turmas (nome_turma, idusuario) VALUES (%s, %s)"
    
    print(f"Valores para inserção: nome_turma = {nome_turma}, idprofessor = {idprofessor}")  # Logando os dados antes de executar a query

    try:
        # Conectando ao banco de dados
        with connect_to_database() as mydb:
            mycursor = mydb.cursor()
            mycursor.execute(sql_turma, (nome_turma, idprofessor))
            mydb.commit()

        return redirect(url_for('turma_cadastro_bp.mostrar_formulario'))  # Redireciona de volta após o cadastro

    except mysql.connector.Error as error:
        print(f"Erro ao cadastrar turma: {error}")  # Adicionando print do erro
        return jsonify({'error': f'Erro ao processar os dados: {str(error)}'}), 500
