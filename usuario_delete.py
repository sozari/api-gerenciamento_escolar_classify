from flask import Blueprint, jsonify
from utils import connect_to_database

usuario_delete_bp = Blueprint('usuario_delete_bp', __name__)

@usuario_delete_bp.route('/usuario_delete/<int:idusuario>', methods=['DELETE'])
def usuario_delete(idusuario):
    try:
        with connect_to_database() as db:
            cursor = db.cursor()

            cursor.execute("DELETE FROM aluno WHERE idusuario = %s", (idusuario,))
            cursor.execute("DELETE FROM professor WHERE idusuario = %s", (idusuario,))
            cursor.execute("DELETE FROM usuarios WHERE idusuario = %s", (idusuario,))
            db.commit()

            if cursor.rowcount == 0:
                return jsonify({'mensagem': 'Nenhum usuário encontrado com este ID.'}), 404

            return jsonify({'mensagem': 'Usuário excluído com sucesso!'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
