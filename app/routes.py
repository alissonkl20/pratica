from sqlar import db
from model import Tarefa  # Nome corrigido
from flask import Blueprint, request, jsonify
from datetime import datetime

routes = Blueprint('routes', __name__)

# Helper para tratamento de erros
def validate_tarefa_data(data, required_fields=['titulo']):
    errors = []
    for field in required_fields:
        if field not in data or not data[field].strip():
            errors.append(f"O campo '{field}' é obrigatório")
    return errors

@routes.route('/tarefas', methods=['GET'])
def get_tarefas():
    try:
        # Filtro por status (opcional)
        status_filter = request.args.get('status')
        if status_filter:
            tarefas = Tarefa.query.filter_by(status=status_filter).all()
        else:
            tarefas = Tarefa.query.all()
        
        return jsonify({
            'tarefas': [t.to_dict() for t in tarefas],
            'total': len(tarefas)
        })
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@routes.route('/tarefas', methods=['POST'])
def add_tarefa():
    try:
        data = request.get_json()
        
        # Validação
        errors = validate_tarefa_data(data)
        if errors:
            return jsonify({'errors': errors}), 400
        
        new_tarefa = Tarefa(
            titulo=data['titulo'].strip(),
            descricao=data.get('descricao', '').strip(),
            status=data.get('status', 'pendente')
        )
        
        db.session.add(new_tarefa)
        db.session.commit()
        
        return jsonify({
            'message': 'Tarefa criada com sucesso!',
            'tarefa': new_tarefa.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar tarefa'}), 500

@routes.route('/tarefas/<int:id>', methods=['GET'])
def get_tarefa(id):
    try:
        t = Tarefa.query.get_or_404(id)
        return jsonify({'tarefa': t.to_dict()})
    except Exception as e:
        return jsonify({'error': 'Tarefa não encontrada'}), 404

@routes.route('/tarefas/<int:id>', methods=['PUT'])
def update_tarefa(id):
    try:
        data = request.get_json()
        t = Tarefa.query.get_or_404(id)
        
        # Validação para atualização
        if 'titulo' in data and not data['titulo'].strip():
            return jsonify({'error': 'Título não pode ser vazio'}), 400
        
        # Atualiza apenas os campos fornecidos
        if 'titulo' in data:
            t.titulo = data['titulo'].strip()
        if 'descricao' in data:
            t.descricao = data['descricao'].strip()
        if 'completed' in data:
            t.completed = data['completed']
            if data['completed']:
                t.status = 'concluida'
                t.completed_at = datetime.utcnow()
            else:
                t.status = 'pendente'
                t.completed_at = None
        
        db.session.commit()
        
        return jsonify({
            'message': 'Tarefa atualizada com sucesso!',
            'tarefa': t.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar tarefa'}), 500

@routes.route('/tarefas/<int:id>', methods=['DELETE'])
def delete_tarefa(id):
    try:
        t = Tarefa.query.get_or_404(id)
        db.session.delete(t)
        db.session.commit()
        return jsonify({'message': 'Tarefa deletada com sucesso!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao deletar tarefa'}), 500

@routes.route('/tarefas/status/<string:status>', methods=['GET'])
def get_tarefas_by_status(status):
    try:
        # Validação do status
        valid_statuses = ['pendente', 'concluida']
        if status not in valid_statuses:
            return jsonify({'error': 'Status inválido'}), 400
            
        tarefas = Tarefa.query.filter_by(status=status).all()
        return jsonify({
            'tarefas': [t.to_dict() for t in tarefas],
            'total': len(tarefas)
        })
    except Exception as e:
        return jsonify({'error': 'Erro ao buscar tarefas'}), 500

@routes.route('/tarefas/<int:id>/complete', methods=['PATCH'])
def mark_tarefa_complete(id):
    try:
        t = Tarefa.query.get_or_404(id)
        
        if t.completed:
            return jsonify({'message': 'Tarefa já estava concluída'})
            
        t.completed = True
        t.status = 'concluida'
        t.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Tarefa marcada como concluída!',
            'tarefa': t.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao marcar tarefa como concluída'}), 500