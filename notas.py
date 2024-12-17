from flask import Blueprint, render_template, request, redirect, url_for
from utils import connect_to_database  # Importando a função para conectar ao banco de dados

# Definindo o Blueprint para 'notas_bp'
notas_bp = Blueprint('notas_bp', __name__)

# Rota para listar os alunos e suas notas
@notas_bp.route('/alunos')
def listar_alunos():
    connection = connect_to_database()
    if connection is None:
        return "Erro ao conectar ao banco de dados."

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM aluno")  # Alterado de 'alunos' para 'aluno'
    alunos = cursor.fetchall()
    connection.close()

    # Verificando a estrutura dos dados para garantir que 'idaluno' é a chave correta
    print(alunos[0])  # Isso vai mostrar o primeiro aluno no console

    return render_template('lista_alunos.html', alunos=alunos)

@notas_bp.route('/editar/<int:aluno_id>', methods=['GET', 'POST'])
def editar_notas(aluno_id):
    connection = connect_to_database()
    if connection is None:
        return "Erro ao conectar ao banco de dados."

    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        nova_nota1 = request.form['nota1']
        nova_nota2 = request.form['nota2']
        nova_nota3 = request.form['nota3']

        # Atualiza as notas no banco de dados usando 'idaluno'
        cursor.execute("""
            UPDATE aluno
            SET nota1 = %s, nota2 = %s, nota3 = %s
            WHERE idaluno = %s
        """, (nova_nota1, nova_nota2, nova_nota3, aluno_id))

        connection.commit()
        connection.close()

        return redirect(url_for('notas_bp.listar_alunos'))

    cursor.execute("SELECT * FROM aluno WHERE idaluno = %s", (aluno_id,))
    aluno = cursor.fetchone()

    connection.close()

    if aluno is None:
        # Se aluno não encontrado, redireciona para a lista de alunos ou exibe uma mensagem de erro
        return "Aluno não encontrado", 404  # Pode redirecionar ou exibir uma página de erro

    return render_template('editar_notas.html', aluno=aluno)
