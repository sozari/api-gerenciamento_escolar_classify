from flask import Blueprint, render_template, request
from utils import connect_to_database  # Importando a função de conexão do utils.py

# Criando o Blueprint
turma_bp = Blueprint('turma_bp', __name__, template_folder='templates')

# Endpoint para seleção de turma
@turma_bp.route('/turmas', methods=['GET'])
def selecionar_turma():
    id_turma = request.args.get('idTurma')  # Pega o idTurma da query string
    print(f"ID da Turma: {id_turma}")  # Imprimir ID da turma para verificação

    conn = connect_to_database()
    if conn is None:
        print("Falha ao conectar ao banco de dados.")  # Logar a falha na conexão
        return "Erro ao conectar ao banco de dados", 500
    else:
        print("Conexão bem-sucedida!")  # Logar a conexão bem-sucedida

    cursor = conn.cursor(dictionary=True)
    
    # Consulta para obter as turmas
    cursor.execute("SELECT idturma, nome_turma FROM turmas")
    turmas = cursor.fetchall()

    alunos = []  # Lista vazia de alunos
    if id_turma:  # Se uma turma foi selecionada
        # Consulta para buscar os alunos da turma
        query = """
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
        LEFT JOIN usuarios u ON a.idusuario = u.idusuario
        WHERE t.idturma = %s;
        """
        cursor.execute(query, (id_turma,))
        alunos = cursor.fetchall()

    conn.close()

    return render_template('turmas_list.html', turmas=turmas, alunos=alunos, id_turma=id_turma)
