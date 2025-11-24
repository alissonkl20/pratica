from sqlar import db

class Tarefa(db.Model):  # Nome de classe em PascalCase
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)  # Deve ser opcional
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    completed_at = db.Column(db.DateTime, nullable=True)  # Adicionar campo de data de conclusão
    completed = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='pendente')  # Corrigido: apenas um status

    def to_dict(self):
        """Método para serializar o objeto"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'completed': self.completed,
            'status': self.status
        }

    def __repr__(self):
        return f"<Tarefa {self.titulo}>"