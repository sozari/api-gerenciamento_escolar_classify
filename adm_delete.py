from flask import Blueprint, jsonify
from utils import connect_to_database

adm_delete_bp = Blueprint('adm_delete_bp', __name__)

@adm_delete_bp.route('/adm_delete/<int:idusuario>/<string:tipo_usuario>', methods=['DELETE'])
def deletar_administrador(idusuario, tipo_usuario):
    try:
        with connect_to_database() as mydb:
            if not mydb:
                return jsonify({'error': 'Erro ao conectar ao banco de dados.'}), 500

            mycursor = mydb.cursor()

            # Verifica se o tipo_usuario é 'administrador'
            if tipo_usuario == 'administrador':
                # Deleta o registro correspondente na tabela 'usuarios'
                delete_adm_sql = "DELETE FROM usuarios WHERE idusuario = %s AND tipo_usuario = %s"
                mycursor.execute(delete_adm_sql, (idusuario, tipo_usuario))
                
                # Verifica se algum registro foi excluído
                if mycursor.rowcount == 0:
                    return jsonify({'mensagem': 'Nenhum administrador encontrado com este ID.'}), 404

            else:
                return jsonify({'mensagem': 'O tipo de usuário informado não é "administrador".'}), 400

            mydb.commit()
            return jsonify({'mensagem': 'Administrador excluído com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
