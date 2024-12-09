from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from utils import connect_to_database  # Importa a função de conexão com o banco

# Cria o blueprint para o login
login_bp = Blueprint('login_bp', __name__)

# Rota de login
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Verificar se o email e senha são válidos
        try:
            with connect_to_database() as mydb:
                mycursor = mydb.cursor(dictionary=True)
                sql = "SELECT * FROM usuarios WHERE email = %s"
                mycursor.execute(sql, (email,))
                usuario = mycursor.fetchone()

                # Verificar se o usuário foi encontrado e se a senha está correta
                if usuario and check_password_hash(usuario['senha'], senha):
                    # Armazenar informações do usuário na sessão
                    session['usuario_id'] = usuario['idusuario']
                    session['usuario_nome'] = usuario['nome']
                    
                    # Exibir mensagem de boas-vindas
                    flash(f'Bem-vindo, {usuario["nome"]}!', 'success')

                    # Redirecionar para a página inicial
                    return redirect(url_for('inicial'))  # Redireciona para a página inicial

                else:
                    flash('Email ou senha incorretos!', 'error')
                    return render_template('login.html')

        except Exception as e:
            flash(f'Ocorreu um erro ao fazer login: {str(e)}', 'error')
            return render_template('login.html')

    return render_template('login.html')
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from utils import connect_to_database  # Importa a função de conexão com o banco

# Cria o blueprint para o login
login_bp = Blueprint('login_bp', __name__)

# Rota de login
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Verificar se o email e senha são válidos
        try:
            with connect_to_database() as mydb:
                mycursor = mydb.cursor(dictionary=True)
                sql = "SELECT * FROM usuarios WHERE email = %s"
                mycursor.execute(sql, (email,))
                usuario = mycursor.fetchone()

                # Verificar se o usuário foi encontrado e se a senha está correta
                if usuario and check_password_hash(usuario['senha'], senha):
                    # Armazenar informações do usuário na sessão
                    session['usuario_id'] = usuario['idusuario']
                    session['usuario_nome'] = usuario['nome']
                    
                    # Exibir mensagem de boas-vindas
                    flash(f'Bem-vindo, {usuario["nome"]}!', 'success')

                    # Redirecionar para a página inicial
                    return redirect(url_for('inicial'))  # Redireciona para a página inicial

                else:
                    flash('Email ou senha incorretos!', 'error')
                    return render_template('login.html')

        except Exception as e:
            flash(f'Ocorreu um erro ao fazer login: {str(e)}', 'error')
            return render_template('login.html')

    return render_template('login.html')
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from utils import connect_to_database  # Importa a função de conexão com o banco

# Cria o blueprint para o login
login_bp = Blueprint('login_bp', __name__)

# Rota de login
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Verificar se o email e senha são válidos
        try:
            with connect_to_database() as mydb:
                mycursor = mydb.cursor(dictionary=True)
                sql = "SELECT * FROM usuarios WHERE email = %s"
                mycursor.execute(sql, (email,))
                usuario = mycursor.fetchone()

                # Verificar se o usuário foi encontrado e se a senha está correta
                if usuario and check_password_hash(usuario['senha'], senha):
                    # Armazenar informações do usuário na sessão
                    session['usuario_id'] = usuario['idusuario']
                    session['usuario_nome'] = usuario['nome']
                    
                    # Exibir mensagem de boas-vindas
                    flash(f'Bem-vindo, {usuario["nome"]}!', 'success')

                    # Redirecionar para a página inicial
                    return redirect(url_for('inicial'))  # Redireciona para a página inicial

                else:
                    flash('Email ou senha incorretos!', 'error')
                    return render_template('login.html')

        except Exception as e:
            flash(f'Ocorreu um erro ao fazer login: {str(e)}', 'error')
            return render_template('login.html')

    return render_template('login.html')
