import os
import requests
import json
import time

class ClaudeClient:
    def __init__(self, api_key=None):
        """Initialize Claude API client"""
        self.api_key = api_key or os.environ.get("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("A chave da API Claude é necessária. Configure-a como variável de ambiente CLAUDE_API_KEY ou passe-a como parâmetro api_key.")
        
        self.api_url = "https://api.anthropic.com/v1/messages"
        
    def generate_response(self, prompt, system_prompt=None, model="claude-3-5-sonnet-20240620", max_tokens=1000, temperature=0.7):
        """Generate a response from Claude"""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        if system_prompt:
            data["system"] = system_prompt
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"]
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer requisição para a API Claude: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Código de status da resposta: {e.response.status_code}")
                print(f"Corpo da resposta: {e.response.text}")
            return None
        except (KeyError, IndexError) as e:
            print(f"Erro ao analisar resposta da API Claude: {e}")
            return None
            
    def generate_sql(self, question, db_info):
        """Generate SQL query for a given question"""
        system_prompt = """
        Você é um assistente SQL prestativo. Sua tarefa é gerar uma consulta SQL válida para a pergunta fornecida,
        com base no esquema de banco de dados fornecido.
        
        A resposta deve conter APENAS a consulta SQL, sem explicações ou texto adicional.
        """
        
        # Prepare database schema info as a prompt
        db_schema_str = json.dumps(db_info, indent=2)
        
        prompt = f"""
        Com base nas seguintes informações do banco de dados:
        
        {db_schema_str}
        
        Gere uma consulta SQL para responder a esta pergunta: "{question}"
        
        Retorne APENAS a consulta SQL, sem explicações ou texto adicional.
        """
        
        return self.generate_response(prompt, system_prompt=system_prompt, temperature=0.1)
    
    def explain_results(self, question, query_results, query, output_format="direct"):
        """Generate an explanation of the query results"""
        system_prompt = """
        Você é um assistente analista de dados prestativo. Sua tarefa é fornecer APENAS as informações solicitadas
        com base nos resultados da consulta SQL, sem mostrar a consulta SQL ou dar explicações sobre como as informações
        foram obtidas.
        
        Não mencione SQL, consultas, banco de dados ou qualquer termo técnico em sua resposta.
        
        NÃO inclua introduções ou conclusões como "Aqui está o resultado" ou "Espero ter ajudado".
        
        A resposta deve ser direta, objetiva e conter APENAS as informações solicitadas pelo usuário.
        """
        
        # Convert query results to string representation
        if isinstance(query_results, str):
            results_str = query_results
        else:
            try:
                results_str = query_results.to_string()
            except:
                results_str = str(query_results)
        
        # Adjust prompt based on output format
        format_instruction = """
        IMPORTANTE: Sua resposta deve conter APENAS as informações solicitadas.
        Não inclua a consulta SQL ou explicações sobre como os dados foram obtidos.
        Não use frases como "Os resultados mostram que" ou "A resposta é".
        Não faça introduções ou conclusões. Seja direto e objetivo.
        """
        
        if output_format == "summary":
            format_instruction += """
            Apresente um resumo extremamente conciso dos resultados em 1-2 frases apenas.
            """
        elif output_format == "bullet":
            format_instruction += """
            Apresente os resultados em forma de marcadores (bullet points) curtos e diretos.
            """
        
        prompt = f"""
        Pergunta original: "{question}"
        
        Resultados da consulta:
        ```
        {results_str}
        ```
        
        {format_instruction}
        """
        
        return self.generate_response(prompt, system_prompt=system_prompt) 