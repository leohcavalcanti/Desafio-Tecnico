from app.models import db
from app.models.plano_aula_model import PlanoAula

class PlanoAulaRepository:
    
    @staticmethod
    def salvar(dados):
        novo_plano = PlanoAula(
            titulo=dados['titulo'],
            disciplina=dados['disciplina'],
            ementa=dados['ementa'],
            data_prevista=dados['data_prevista'],
            objetivo=dados.get('objetivo'),
            conteudos=dados.get('conteudos'),
            recursos_apoio=dados.get('recursos_apoio'),
            tags=dados.get('tags')
        )
        db.session.add(novo_plano)
        db.session.commit()
        return novo_plano

    @staticmethod
    def buscar_todos(filtros):
        query = PlanoAula.query
        
        if filtros.get('busca_titulo'):
            query = query.filter(PlanoAula.titulo.ilike(f"%{filtros['busca_titulo']}%"))
            
        if filtros.get('filtro_disciplina'):
            query = query.filter(PlanoAula.disciplina.ilike(f"%{filtros['filtro_disciplina']}%"))
            
        if filtros.get('filtro_data'):
            query = query.filter(PlanoAula.data_prevista == filtros['filtro_data'])
            
        if filtros.get('filtro_tag'):
            query = query.filter(db.cast(PlanoAula.tags, db.String).ilike(f"%{filtros['filtro_tag']}%"))

        if filtros.get('ordenar_por') == 'titulo':
            query = query.order_by(PlanoAula.titulo.asc())
        else:
            query = query.order_by(PlanoAula.data_cadastro.desc())

        return query.paginate(
            page=filtros.get('pagina', 1),
            per_page=filtros.get('por_pagina', 10),
            error_out=False
        )

    @staticmethod
    def obter_por_id(plano_id):
        return db.session.get(PlanoAula, plano_id)

    @staticmethod
    def atualizar(plano_existente, novos_dados):
        for campo, valor in novos_dados.items():
            if hasattr(plano_existente, campo) and campo != 'id':
                setattr(plano_existente, campo, valor)
                
        db.session.commit()
        return plano_existente

    @staticmethod
    def excluir(plano_existente):
        db.session.delete(plano_existente)
        db.session.commit()
        return True