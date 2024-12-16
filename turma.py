from flask import Blueprint, render_template, request
from utils import connect_to_database  # Importando a função de conexão do utils.py

# Criando o Blueprint
turma_bp = Blueprint('turma_bp', __name__, template_folder='templates')

# Endpoint para seleção de turma
@turma_bp.route('/turmas', methods=['GET'])
def selecionar_turma():
    conn = connect_to_database()  # Usando a função de conexão do utils.py
    if conn is None:
        return "Erro ao conectar ao banco de dados", 500

    cursor = conn.cursor(dictionary=True)  # Usando dictionary=True para obter resultados como dicionários
    
    # Consulta para obter as turmas
    query = "SELECT idturma, nome_turma FROM turmas"
    cursor.execute(query)
    turmas = cursor.fetchall()
    conn.close()

    return render_template('turma_select.html', turmas=turmas)


# Endpoint para listar alunos de uma turma
@turma_bp.route('/turmas/alunos', methods=['GET'])
def listar_alunos_turma():
    id_turma = request.args.get('idTurma')  # Pega o idTurma da query string
    if not id_turma:
        return "Turma não especificada", 400

    conn = connect_to_database()  # Usando a função de conexão do utils.py
    if conn is None:
        return "Erro ao conectar ao banco de dados", 500

    cursor = conn.cursor(dictionary=True)

    # Consulta para obter os alunos da turma selecionada
    query = """
    SELECT
        u.nome AS nome_aluno,
        n.nota1,
        n.nota2,
        n.nota3,
        n.media
    FROM
        aluno a
    JOIN
        usuarios u ON a.idusuario = u.idusuario
    LEFT JOIN
        notas n ON a.idaluno = n.idaluno AND n.idturma = %s
    WHERE
        a.idturma = %s
    """
    cursor.execute(query, (id_turma, id_turma))
    alunos = cursor.fetchall()
    conn.close()

    return render_template('lista_alunos.html', alunos=alunos, id_turma=id_turma)
