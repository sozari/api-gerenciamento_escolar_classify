from flask import Blueprint, render_template
import sqlite3

# Nome único para o Blueprint
turma_routes_bp = Blueprint('turma_routes_bp', __name__, template_folder='templates')

def obter_turmas():
    """Função para buscar as turmas do banco de dados."""
    conn = sqlite3.connect('gerenciamento_escolar.db')  # Conecta ao banco
    cursor = conn.cursor()
    cursor.execute("SELECT nome_turma FROM turmas")  # Consulta apenas os nomes das turmas
    turmas = cursor.fetchall()  # Busca todos os resultados
    conn.close()  # Fecha a conexão
    return [turma[0] for turma in turmas]  # Retorna uma lista com os nomes das turmas

@turma_routes_bp.route('/turmas')
def selecionar_turma():
    turmas = obter_turmas()  # Busca as turmas no banco
    return render_template('turma_select.html', turmas=turmas)
