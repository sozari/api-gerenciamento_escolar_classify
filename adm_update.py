from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash
from utils import connect_to_database

adm_update_bp = Blueprint('adm_update_bp', __name__)

@adm_update_bp.route('/adm_update/<int:idusuario>/<string:tipo_usuario>', methods=['GET', 'POST'])
def atualizar_administrador(idusuario, tipo_usuario):
    if tipo_usuario != 'administrador':
        return jsonify({'mensagem': 'Atualização permitida apenas para administradores.'}), 403

    if request.method == 'POST':
        # Dados vindos do formulário
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not email or not senha:
            return jsonify({'mensagem': 'Todos os campos são obrigatórios.'}), 400

        senha_criptografada = generate_password_hash(senha)  # Criptografa a nova senha

        sql = """
            UPDATE usuarios 
            SET nome = %s, email = %s, senha = %s 
            WHERE idusuario = %s AND tipo_usuario = %s
        """
        valores = (nome, email, senha_criptografada, idusuario, tipo_usuario)

        try:
            connection = connect_to_database()
            if connection is None:
                return jsonify({'mensagem': 'Erro ao conectar ao banco de dados.'}), 500

            with connection as mydb:
                mycursor = mydb.cursor()
                mycursor.execute(sql, valores)
                
                if mycursor.rowcount == 0:
                    return jsonify({'mensagem': 'Nenhum administrador encontrado com este ID e tipo de usuário.'}), 404

                mydb.commit()
                return jsonify({'mensagem': 'Dados do administrador atualizados com sucesso!'}), 200
        except mysql.connector.Error as error:
            return jsonify({'error': str(error)}), 500

    # Se for GET, apenas exibe a página de edição
    return render_template('aluno_update.html', idusuario=idusuario, tipo_usuario=tipo_usuario)
