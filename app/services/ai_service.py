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

        Retorne EXATAMENTE um JSON válido, sem NENHUM texto antes ou depois, com a seguinte estrutura:
        {{
            "conteudos_complementares": "Um parágrafo recomendando livros, vídeos ou artigos.",
            "topicos_relacionados": ["Tópico 1", "Tópico 2"],
            "tags_recomendadas": ["#tag1", "#tag2", "#tag3"]
        }}
        
        Atenção: Retorne sempre exatamente 3 tags_recomendadas, todas em letras minúsculas e sem espaços. Não inclua a formatação markdown ```json.
        """

        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            resposta = model.generate_content(prompt)
            
            conteudo_ia = resposta.text
            
            if conteudo_ia.strip().startswith("```json"):
                conteudo_ia = conteudo_ia.strip().strip("```json").strip("```").strip()

            tokens_entrada = model.count_tokens(prompt).total_tokens
            tokens_saida = model.count_tokens(conteudo_ia).total_tokens
            tokens_usados = tokens_entrada + tokens_saida

            dicionario_resposta = json.loads(conteudo_ia)
            
            return dicionario_resposta, tokens_usados

        except json.JSONDecodeError:
            logging.error(f"A IA não retornou um JSON válido. Retorno puro: {conteudo_ia}")
            raise Exception("Erro ao processar a resposta da IA. Formato inválido.")
        except Exception as e:
            logging.error(f"Erro na comunicação com o Gemini: {str(e)}")
            raise Exception(f"Falha no provedor de IA: {str(e)}")