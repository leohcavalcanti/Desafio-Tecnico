from flask import Blueprint, request, jsonify
from app.services.plano_aula_service import PlanoAulaService

plano_aula_bp = Blueprint("plano_aula", __name__)


@plano_aula_bp.route("/plano", methods=["POST"])
def criar_plano():
    dados = request.get_json()

    campos_obrigatorios = [
        "titulo",
        "ementa",
        "data_prevista",
        "disciplina",
    ]
    for campo in campos_obrigatorios:
        if not dados or campo not in dados or not dados[campo]:
            return jsonify({"error": f'O campo "{campo}" é obrigatório.'}), 400

    try:
        resultado = PlanoAulaService.criar_plano(dados)
        return (
            jsonify(
                {"message": "Plano de aula criado com sucesso!", "dados": resultado}
            ),
            201,
        )
    except Exception as e:
        return jsonify({"erro": f"Erro interno ao salvar: {str(e)}"}), 500


@plano_aula_bp.route("/plano", methods=["GET"])
def listar_planos():
    filtros = {
        "pagina": request.args.get("page", default=1, type=int),
        "por_pagina": request.args.get("per_page", default=10, type=int),
        "filtro_disciplina": request.args.get("disciplina", type=str),
        "filtro_tag": request.args.get("tag", type=str),
        "filtro_data": request.args.get("data_prevista", type=str),
        "busca_titulo": request.args.get("titulo", type=str),
        "ordenar_por": request.args.get(
            "ordenar_por", default="data_prevista", type=str
        ),
    }

    try:
        resultado = PlanoAulaService.listar_planos(filtros)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@plano_aula_bp.route("/plano/<int:id>", methods=["GET"])
def obter_plano(id):
    try:
        resultado = PlanoAulaService.obter_por_id(id)
        return jsonify(resultado), 200
    except ValueError as ve:
        return jsonify({"erro": str(ve)}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@plano_aula_bp.route("/plano/<int:id>", methods=["PUT"])
def editar_plano(id):
    dados_atualizados = request.get_json()

    if not dados_atualizados:
        return jsonify({"error": "Nenhum dado fornecido para atualização."}), 400

    try:
        resultado = PlanoAulaService.atualizar_plano(id, dados_atualizados)
        return (
            jsonify(
                {"mensagem": f"Plano {id} atualizado com sucesso!", "dados": resultado}
            ),
            200,
        )
    except ValueError as ve:
        return jsonify({"erro": str(ve)}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@plano_aula_bp.route("/plano/<int:id>", methods=["DELETE"])
def excluir_plano(id):
    try:
        PlanoAulaService.excluir_plano(id)
        return (
            jsonify(
                {
                    "mensagem": f"Plano de aula {id} excluído com sucesso!",
                }
            ),
            200,
        )
    except ValueError as ve:
        return jsonify({"erro": str(ve)}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@plano_aula_bp.route("/plano/recomendar", methods=["POST"])
def gerar_recomendacoes_ia():
    dados = request.get_json()

    if (
        not dados
        or "titulo" not in dados
        or "disciplina" not in dados
        or "ementa" not in dados
    ):
        return (
            jsonify(
                {
                    "erro": "Para gerar recomendações, informe Título, Disciplina e Ementa/Resumo."
                }
            ),
            400,
        )

    try:
        resposta_ia = PlanoAulaService.gerar_recomendacoes_ia(
            titulo=dados["titulo"],
            disciplina=dados["disciplina"],
            ementa=dados["ementa"],
        )
        return jsonify(resposta_ia), 200
    except Exception as e:
        return (
            jsonify({"erro": f"Falha na comunicação com o assistente de IA: {str(e)}"}),
            504,
        )
