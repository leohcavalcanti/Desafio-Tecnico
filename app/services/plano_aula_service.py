import time
import logging
from app.repositories.plano_aula_repository import PlanoAulaRepository
from app.services.ai_service import AIService

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


class PlanoAulaService:
    @staticmethod
    def criar_plano(dados):
        if "tags" in dados and isinstance(dados["tags"], list):
            dados["tags"] = [tag.strip().lower() for tag in dados["tags"]]

        novo_plano = PlanoAulaRepository.salvar(dados)
        logging.info(
            f"Plano de Aula '{novo_plano.titulo}' salvo com sucesso no banco de dados."
        )

        return novo_plano.to_dict()

    @staticmethod
    def listar_planos(filtros):
        logging.info(f"Listando planos de aula com os filtros: {filtros}")
        paginacao = PlanoAulaRepository.buscar_todos(filtros)

        return {
            "planos": [plano.to_dict() for plano in paginacao.items],
            "meta": {
                "pagina_atual": paginacao.page,
                "por_pagina": paginacao.per_page,
                "total_registros": paginacao.total,
                "total_paginas": paginacao.pages,
            },
        }

    @staticmethod
    def obter_por_id(plano_id):
        plano = PlanoAulaRepository.obter_por_id(plano_id)
        if not plano:
            raise ValueError(f"Plano de aula com ID {plano_id} não encontrado.")
        return plano.to_dict()

    @staticmethod
    def atualizar_plano(plano_id, novos_dados):
        plano_existente = PlanoAulaRepository.obter_por_id(plano_id)
        if not plano_existente:
            raise ValueError(f"Plano de aula com ID {plano_id} não encontrado.")

        if "tags" in novos_dados and isinstance(novos_dados["tags"], list):
            novos_dados["tags"] = [tag.strip().lower() for tag in novos_dados["tags"]]

        plano_atualizado = PlanoAulaRepository.atualizar(plano_existente, novos_dados)
        logging.info(f"Plano de aula ID {plano_id} atualizado com sucesso.")

        return plano_atualizado.to_dict()

    @staticmethod
    def excluir_plano(plano_id):
        plano_existente = PlanoAulaRepository.obter_por_id(plano_id)
        if not plano_existente:
            raise ValueError(f"Plano de aula com ID {plano_id} não encontrado.")

        PlanoAulaRepository.excluir(plano_existente)
        logging.info(f"Plano de aula ID {plano_id} foi removido permanentemente.")
        return True

    @staticmethod
    def gerar_recomendacoes_ia(titulo, disciplina, ementa):
        inicio = time.time()

        resposta_ia, tokens_usados = AIService.gerar_sugestoes(
            titulo, disciplina, ementa
        )

        latencia = round(time.time() - inicio, 2)

        logging.info(
            f'AI Request: Title="{titulo}", Discipline="{disciplina}", Token Usage={tokens_usados}, Latency={latencia}s.'
        )

        return resposta_ia
