from datetime import datetime, timezone
from app.models import db

class PlanoAula(db.Model):
    __tablename__ = 'planos_aula'

    id = db.Column(db.Integer, primary_key=True)

    # Cammpos obrigatórios
    titulo = db.Column(db.String(255), nullable=False)
    disciplina = db.Column(db.String(100), nullable=False)
    ementa = db.Column(db.Text, nullable=False)
    data_prevista = db.Column(db.Date, nullable=False)

    # Camppos complementares
    objetivo = db.Column(db.Text, nullable=True)
    conteudos = db.Column(db.Text, nullable=True)
    recursos_apoio = db.Column(db.Text, nullable=True)

    tags = db.Column(db.JSON, nullable=True)

    data_cadastro = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "disciplina": self.disciplina,
            "ementa": self.ementa,
            "data_prevista": self.data_prevista.isoformat() if self.data_prevista else None,
            "objetivo": self.objetivo,
            "conteudos": self.conteudos,
            "recursos_apoio": self.recursos_apoio,
            "tags": self.tags,
            "data_cadastro": self.data_cadastro.isoformat() if self.data_cadastro else None
        }