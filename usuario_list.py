from flask import Flask, jsonify, Blueprint, render_template
import mysql.connector

app = Flask(__name__)

# Blueprint
usuario_list_bp = Blueprint('usuario_list_bp', __name__)

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'gerenciamento_escolar'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Rota para listar usuários via API
@usuario_list_bp.route('/usuario_list', methods=['GET'])
def listar_usuarios():
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT idusuario, nome, email, tipo_usuario FROM usuarios")
            usuarios = cursor.fetchall()

            return jsonify([
                {'idusuario': idusuario, 'nome': nome, 'email': email, 'tipo_usuario': tipo_usuario}
                for idusuario, nome, email, tipo_usuario in usuarios
            ]), 200
    except mysql.connector.Error as e:
        return jsonify({'error': f'Erro ao listar os usuários: {str(e)}'}), 500

# Rota para renderizar a página de listagem de usuários
@usuario_list_bp.route('/usuario_list.html', methods=['GET'])
def listar_usuarios_html():
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT idusuario, nome, email, tipo_usuario FROM usuarios")
            usuarios = cursor.fetchall()

            return render_template('usuario_list.html', usuarios=usuarios)
    except mysql.connector.Error as e:
        return jsonify({'error': f'Erro ao listar os usuários: {str(e)}'}), 500

# Registrar Blueprint
app.register_blueprint(usuario_list_bp)

if __name__ == '__main__':
    app.run(debug=True)
