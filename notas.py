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

    # Selecionando alunos, suas notas e o nome do aluno da tabela 'usuarios'
    cursor.execute("""
    SELECT a.idaluno, u.nome AS nome_aluno, n.nota1, n.nota2, n.nota3, n.media, t.nome_turma, n.idnota
    FROM aluno a
    LEFT JOIN notas n ON a.idusuario = n.idusuario
    LEFT JOIN turmas t ON a.idturma = t.idturma
    LEFT JOIN usuarios u ON a.idusuario = u.idusuario
""")
    alunos = cursor.fetchall()

    connection.close()

    return render_template('lista_alunos.html', alunos=alunos)


@notas_bp.route('/editar/<int:idnota>', methods=['GET', 'POST'])
def editar_notas(idnota):
    connection = connect_to_database()
    if connection is None:
        return "Erro ao conectar ao banco de dados."

    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        nova_nota1 = request.form['nota1']
        nova_nota2 = request.form['nota2']
        nova_nota3 = request.form['nota3']

        # Atualizando as notas no banco de dados usando 'idnota'
        cursor.execute("""
            UPDATE notas
            SET nota1 = %s, nota2 = %s, nota3 = %s
            WHERE idnota = %s
        """, (nova_nota1, nova_nota2, nova_nota3, idnota))

        connection.commit()
        connection.close()

        return redirect(url_for('notas_bp.listar_alunos'))

    # Buscando as notas do aluno com o 'idnota'
    cursor.execute("""
        SELECT n.idnota, n.nota1, n.nota2, n.nota3, n.media, u.nome AS nome_aluno, t.nome_turma 
        FROM notas n
        LEFT JOIN aluno a ON n.idusuario = a.idusuario
        LEFT JOIN turmas t ON a.idturma = t.idturma
        LEFT JOIN usuarios u ON a.idusuario = u.idusuario
        WHERE n.idnota = %s
    """, (idnota,))
    nota = cursor.fetchone()

    connection.close()

    if nota is None:
        return "Nota não encontrada", 404  # Retorna erro se a nota não for encontrada

    return render_template('editar_notas.html', nota=nota)

