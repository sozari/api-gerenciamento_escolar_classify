from flask import Blueprint, render_template, request, redirect, url_for
from utils import connect_to_database

# Definindo o Blueprint para 'notas_bp'
notas_bp = Blueprint('notas_bp', __name__)

# Rota para listar os alunos e suas notas
@notas_bp.route('/alunos')
def listar_alunos():
    connection = connect_to_database()
    if connection is None:
        return "Erro ao conectar ao banco de dados."

    cursor = connection.cursor(dictionary=True)

    # Selecionando alunos, suas notas, e o nome da turma
    cursor.execute("""
        SELECT 
            a.idaluno, 
            u.nome AS nome_aluno, 
            n.idnota, 
            n.nota1, 
            n.nota2, 
            n.nota3, 
            n.media, 
            t.nome_turma
        FROM aluno a
        LEFT JOIN notas n ON a.idusuario = n.idusuario
        LEFT JOIN turmas t ON a.idturma = t.idturma
        LEFT JOIN usuarios u ON a.idusuario = u.idusuario;
    """)
    alunos = cursor.fetchall()

    connection.close()

    return render_template('lista_alunos.html', alunos=alunos)

# Rota para editar notas
@notas_bp.route('/editar/<int:idnota>', methods=['GET', 'POST'])
def editar_notas(idnota):
    connection = connect_to_database()
    if connection is None:
        return "Erro ao conectar ao banco de dados."

    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        # Pegando os valores das novas notas
        try:
            nova_nota1 = float(request.form.get('nota1', 0))
            nova_nota2 = float(request.form.get('nota2', 0))
            nova_nota3 = float(request.form.get('nota3', 0))

            # Calculando a média
            media = (nova_nota1 + nova_nota2 + nova_nota3) / 3

            # Atualizando as notas e a média no banco de dados
            cursor.execute("""
                UPDATE notas
                SET nota1 = %s, nota2 = %s, nota3 = %s, media = %s
                WHERE idnota = %s
            """, (nova_nota1, nova_nota2, nova_nota3, media, idnota))

            connection.commit()
        except ValueError:
            return "Erro ao processar as notas. Certifique-se de inserir números válidos.", 400
        finally:
            connection.close()

        # Redirecionar para a página de lista de turmas após salvar as notas
        return redirect(url_for('notas_bp.listar_turmas'))  # Alteração aqui

    # Buscando as informações das notas para edição
    cursor.execute("""
        SELECT 
            n.idnota, 
            n.nota1, 
            n.nota2, 
            n.nota3, 
            n.media, 
            u.nome AS nome_aluno, 
            t.nome_turma 
        FROM notas n
        LEFT JOIN aluno a ON n.idusuario = a.idusuario
        LEFT JOIN turmas t ON a.idturma = t.idturma
        LEFT JOIN usuarios u ON a.idusuario = u.idusuario
        WHERE n.idnota = %s;
    """, (idnota,))
    nota = cursor.fetchone()

    connection.close()

    if nota is None:
        return "Nota não encontrada", 404

    return render_template('editar_notas.html', nota=nota)

# Rota para criar notas
@notas_bp.route('/criar/<int:idaluno>', methods=['GET', 'POST'])
def criar_notas(idaluno):
    connection = connect_to_database()
    if connection is None:
        return "Erro ao conectar ao banco de dados."

    cursor = connection.cursor(dictionary=True)

    # Obter informações do aluno
    cursor.execute("""
        SELECT a.idusuario, u.nome AS nome_aluno, t.nome_turma
        FROM aluno a
        LEFT JOIN usuarios u ON a.idusuario = u.idusuario
        LEFT JOIN turmas t ON a.idturma = t.idturma
        WHERE a.idaluno = %s
    """, (idaluno,))
    aluno = cursor.fetchone()

    if aluno is None:
        connection.close()
        return "Aluno não encontrado", 404

    if request.method == 'POST':
        nota1 = float(request.form['nota1'])
        nota2 = float(request.form['nota2'])
        nota3 = float(request.form['nota3'])

        # Calcular a média
        media = (nota1 + nota2 + nota3) / 3

        # Criar entrada na tabela de notas
        cursor.execute("""
            INSERT INTO notas (idusuario, nota1, nota2, nota3, media)
            VALUES (%s, %s, %s, %s, %s)
        """, (aluno['idusuario'], nota1, nota2, nota3, media))
        connection.commit()

        # Pegar o id da última nota inserida
        idnota_criado = cursor.lastrowid

        connection.close()

        # Redirecionar para a página de lista de turmas após criar a nota
        return redirect(url_for('notas_bp.listar_turmas'))  # Alteração aqui

    connection.close()
    return render_template('criar_notas.html', aluno=aluno)




@notas_bp.route('/turmas')
def listar_turmas():
    connection = connect_to_database()
    if connection is None:
        return "Erro ao conectar ao banco de dados."

    cursor = connection.cursor(dictionary=True)

    # Selecionando todas as turmas
    cursor.execute("""
        SELECT idturma, nome_turma 
        FROM turmas;
    """)
    turmas = cursor.fetchall()

    connection.close()

    return render_template('turmas_list.html', turmas=turmas)
