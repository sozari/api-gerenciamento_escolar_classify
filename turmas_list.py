from flask import Blueprint, render_template, request
from utils import connect_to_database

# Criando o Blueprint
turma_bp = Blueprint('turma_bp', __name__, template_folder='templates')

# Endpoint para seleção de turma (já existe)
@turma_bp.route('/turmas', methods=['GET'])
def selecionar_turma():
    conn = connect_to_database()
    if conn is None:
        return "Erro ao conectar ao banco de dados", 500

    cursor = conn.cursor(dictionary=True)

    # Consulta para obter as turmas
    query = "SELECT idturma, nome_turma FROM turmas"
    cursor.execute(query)
    turmas = cursor.fetchall()
    conn.close()

    # Recupera o id da turma selecionada da query string (se houver)
    id_turma = request.args.get('idTurma', type=int)
    if not id_turma:
        return "Turma não encontrada", 404  # Se não encontrar a turma, retorna erro

    # Consulta para obter os alunos da turma selecionada
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT
        u.nome AS nome_aluno,
        n.nota1,
        n.nota2,
        n.nota3,
        n.media,
        a.idaluno
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

    return render_template('turmas_list.html', turmas=turmas, alunos=alunos, id_turma=id_turma)

# Endpoint para salvar notas (ajuste conforme a necessidade)
@turma_bp.route('/salvar_notas', methods=['POST'])
def salvar_notas():
    # Aqui você pode pegar os dados e salvar no banco de dados
    # Exemplo de como pegar as notas:
    # dados = request.get_json()
    pass
