from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
from utils import connect_to_database

usuario_update_bp = Blueprint('usuario_update_bp', __name__)

# Rota para exibir o formulário de edição
@usuario_update_bp.route('/usuario_update.html', methods=['GET'])
def usuario_update_page():
    idusuario = request.args.get('idusuario')  # Pegando o id do usuário da URL
    tipo_usuario = request.args.get('tipo_usuario')

    try:
        with connect_to_database() as db:
            cursor = db.cursor()

            cursor.execute("SELECT idusuario, nome, email, tipo_usuario FROM usuarios WHERE idusuario = %s", (idusuario,))
            usuario = cursor.fetchone()

            if usuario is None:
                return "Usuário não encontrado", 404

            return render_template('usuario_update.html', usuario=usuario, tipo_usuario=tipo_usuario)
    except Exception as e:
        return str(e), 500

# Rota para atualizar os dados do usuário
@usuario_update_bp.route('/usuario_update/<int:idusuario>', methods=['POST'])
def usuario_update(idusuario):
    dados = request.form
    nome = dados.get('name')
    email = dados.get('email')
    senha = dados.get('password')
    
    # Criptografando a senha
    senha_criptografada = generate_password_hash(senha)

    try:
        with connect_to_database() as db:
            cursor = db.cursor()

            sql = """
                UPDATE usuarios
                SET nome = %s, email = %s, senha = %s
                WHERE idusuario = %s
            """
            valores = (nome, email, senha_criptografada, idusuario)
            cursor.execute(sql, valores)

            if cursor.rowcount == 0:
                return jsonify({'mensagem': 'Nenhum usuario encontrado com este ID.'}), 404

            db.commit()

            # Após atualizar, redireciona para a lista de usuários
            return redirect('/usuario_list.html')

    except Exception as e:
        return jsonify({'erro': str(e)}), 500
