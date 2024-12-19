from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import mysql.connector

from aluno_update import aluno_update_bp
from aluno_cadastro import aluno_cadastro_bp
from aluno_delete import aluno_delete_bp
from professor_cadastro import professor_cadastro_bp
from usuario_update import usuario_update_bp
from usuario_delete import usuario_delete_bp
from adm_cadastro import adm_cadastro_bp
from adm_delete import adm_delete_bp
from adm_update import adm_update_bp
from professor_update import professor_update_bp
from professor_delete import professor_delete_bp
from usuario_list import usuario_list_bp
from login import login_bp
from turma_cadastro import turma_cadastro_bp
from turma import turma_bp 
from turma_routes import turma_routes_bp
from notas import notas_bp




app = Flask(__name__)

# Registro de Blueprints
app.register_blueprint(aluno_update_bp)
app.register_blueprint(aluno_cadastro_bp)
app.register_blueprint(aluno_delete_bp)
app.register_blueprint(professor_cadastro_bp)
app.register_blueprint(usuario_update_bp)
app.register_blueprint(usuario_delete_bp)
app.register_blueprint(adm_cadastro_bp)
app.register_blueprint(adm_delete_bp)
app.register_blueprint(adm_update_bp)
app.register_blueprint(professor_update_bp)
app.register_blueprint(professor_delete_bp)
app.register_blueprint(usuario_list_bp)
app.register_blueprint(login_bp)
app.register_blueprint(turma_cadastro_bp)
app.register_blueprint(turma_bp, url_prefix='/')
app.register_blueprint(turma_routes_bp)  # Nome atualizado, sem conflitos
app.register_blueprint(notas_bp, url_prefix='/notas')  # Opcional: Usar um prefixo para as rotas do Blueprint

# Definição de uma chave secreta simples
app.secret_key = 'minha_chave_secreta_123'

# Rota inicial para redirecionar ao login
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login_bp.login'))  # Redireciona para a página de login

# Rota para a página inicial
@app.route('/inicial', methods=['GET'])
def inicial():
    # Verifica se o usuário está logado
    if 'usuario_nome' in session:
        return render_template('inicial.html', nome=session['usuario_nome'])  # Passa o nome do usuário para o template
    return redirect(url_for('login_bp.login'))  # Redireciona para o login se não estiver logado

if __name__ == '__main__':
    app.run(debug=True)


    '''teste2'''
