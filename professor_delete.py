from flask import Blueprint, jsonify
from utils import connect_to_database

professor_delete_bp = Blueprint('professor_delete_bp', __name__)

@professor_delete_bp.route('/professor_delete/<int:idusuario>/<string:tipo_usuario>', methods=['DELETE'])
def deletar_professor(idusuario, tipo_usuario):
    try:
        with connect_to_database() as mydb:
            if not mydb:
                return jsonify({'error': 'Erro ao conectar ao banco de dados.'}), 500

            mycursor = mydb.cursor()

            # Verifica se o tipo_usuario é 'professor'
            if tipo_usuario == 'professor':
                # Deleta o registro correspondente na tabela 'professor'
                delete_professor_sql = "DELETE FROM professor WHERE idusuario = %s"
                mycursor.execute(delete_professor_sql, (idusuario,))
                
                # Verifica se algum registro foi excluído
                if mycursor.rowcount == 0:
                    return jsonify({'mensagem': 'Nenhum professor encontrado com este ID.'}), 404

                # Deleta o registro na tabela 'usuarios'
                delete_usuario_sql = "DELETE FROM usuarios WHERE idusuario = %s AND tipo_usuario = %s"
                mycursor.execute(delete_usuario_sql, (idusuario, tipo_usuario))

            else:
                return jsonify({'mensagem': 'O tipo de usuário informado não é "professor".'}), 400

            mydb.commit()
            return jsonify({'mensagem': 'professor excluído com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
