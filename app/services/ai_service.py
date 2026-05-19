import os
import json
import logging
import google.generativeai as genai

class AIService:
    @staticmethod
    def gerar_sugestoes(titulo, disciplina, ementa):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Chave da API do Gemini não configurada no .env.")

        genai.configure(api_key=api_key)

        prompt = f"""
        Você é um Assistente Pedagógico especialista em planejamento de aulas.
        Seu objetivo é sugerir conteúdos para enriquecer a aula do professor.
        
        Disciplina: {disciplina}
        Título da Aula: {titulo}
        Ementa/Resumo: {ementa}

        Preencha e retorne as seguintes informações:
        1. "conteudos_complementares": Um parágrafo recomendando livros, vídeos ou artigos.
        2. "topicos_relacionados": Uma lista com 2 a 3 tópicos.
        3. "tags_recomendadas": Exatamente 3 tags, todas em letras minúsculas e sem espaços (ex: ["#tag1", "#tag2", "#tag3"]).
        """

        try:
            nome_do_modelo = "gemini-2.5-flash"
            
            model = genai.GenerativeModel(nome_do_modelo)

            resposta = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json"
                )
            )

            conteudo_ia = resposta.text

            tokens_entrada = model.count_tokens(prompt).total_tokens
            tokens_saida = model.count_tokens(conteudo_ia).total_tokens
            tokens_usados = tokens_entrada + tokens_saida

            dicionario_resposta = json.loads(conteudo_ia)

            return dicionario_resposta, tokens_usados

        except json.JSONDecodeError as e:
            logging.error(f"A IA não retornou um JSON válido. Retorno puro: {conteudo_ia}")
            raise Exception("Erro ao processar a resposta da IA. Formato inválido.")
        except Exception as e:
            logging.error(f"Erro na comunicação com o Gemini: {str(e)}")
            raise Exception(f"Falha no provedor de IA: {str(e)}")