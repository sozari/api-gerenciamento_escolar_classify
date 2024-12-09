from flask import Blueprint, jsonify
from utils import connect_to_database

aluno_delete_bp = Blueprint('aluno_delete_bp', __name__)

@aluno_delete_bp.route('/aluno_delete/<int:idusuario>/<string:tipo_usuario>', methods=['DELETE'])
def deletar_aluno(idusuario, tipo_usuario):
    try:
        with connect_to_database() as mydb:
            if not mydb:
                return jsonify({'error': 'Erro ao conectar ao banco de dados.'}), 500

            mycursor = mydb.cursor()

            # Verifica se o tipo_usuario é 'aluno'
            if tipo_usuario == 'aluno':
                # Deletar o registro relacionado na tabela aluno
                delete_aluno_sql = "DELETE FROM aluno WHERE idusuario = %s"
                mycursor.execute(delete_aluno_sql, (idusuario,))
                
                # Verificar se o registro na tabela 'aluno' foi excluído
                if mycursor.rowcount == 0:
                    return jsonify({'mensagem': 'Nenhum aluno encontrado com este ID na tabela aluno.'}), 404
                
                # Agora, deletar o registro correspondente na tabela 'usuarios'
                delete_usuario_sql = "DELETE FROM usuarios WHERE idusuario = %s AND tipo_usuario = %s"
                mycursor.execute(delete_usuario_sql, (idusuario, tipo_usuario))

                # Verifica se algum registro foi excluído
                if mycursor.rowcount == 0:
                    return jsonify({'mensagem': 'Nenhum aluno encontrado com este ID na tabela usuarios.'}), 404

            else:
                return jsonify({'mensagem': 'O tipo de usuário informado não é "aluno".'}), 400

            mydb.commit()
            return jsonify({'mensagem': 'Aluno e seus dados excluídos com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
