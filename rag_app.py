import os
import json
import pandas as pd
from db_connector import DatabaseConnector
from query_executor import QueryExecutor
from claude_client import ClaudeClient
from question_generator import QuestionGenerator

class RAGSystem:
    def __init__(self, api_key=None, db_path="dados (2).db"):
        """Initialize the RAG system with all required components"""
        # Initialize database components
        self.db_connector = DatabaseConnector(db_path)
        self.query_executor = QueryExecutor(self.db_connector)
        
        # Initialize Claude API client
        self.claude_client = ClaudeClient(api_key)
        
        # Database schema information
        self.db_info = self.query_executor.get_database_info()
        
        # Initialize question generator
        self.question_generator = QuestionGenerator(self.db_info, self.claude_client)
        
        # System prompt for general queries
        self.system_prompt = """
        Você é um assistente prestativo que fornece informações precisas com base nos resultados de consultas ao banco de dados.
        Suas respostas devem ser claras, concisas e responder diretamente à pergunta do usuário com base nos dados fornecidos.
        
        Apresente apenas a resposta final, sem mostrar a consulta SQL ou explicações adicionais sobre como os dados foram obtidos.
        
        Apresente suas respostas de maneira profissional e informativa, usando marcadores ou tabelas quando apropriado
        para tornar as informações mais acessíveis.
        """
    
    def process_query(self, user_query, output_format="direct"):
        """
        Process a natural language query and return results
        
        Parameters:
        - user_query (str): The user's question in natural language
        - output_format (str): Format for the response. Options include:
          - "default": Full explanation
          - "direct": Only the data, no explanations
          - "summary": Very brief 1-2 sentence summary
          - "bullet": Bullet point format
        """
        try:
            # Generate SQL query from natural language
            sql_query = self.claude_client.generate_sql(user_query, self.db_info)
            
            # Clean up query if needed
            sql_query = sql_query.strip()
            if sql_query.startswith("```sql"):
                sql_query = sql_query.split("```sql")[1].split("```")[0].strip()
            elif sql_query.startswith("```"):
                sql_query = sql_query.split("```")[1].split("```")[0].strip()
            
            # Execute the SQL query
            results = self.query_executor.execute_sql(sql_query)
            
            # Generate explanation of results
            explanation = self.claude_client.explain_results(user_query, results, sql_query, output_format)
            
            return {
                "query": user_query,
                "sql_query": sql_query,
                "results": results,
                "explanation": explanation
            }
        except Exception as e:
            return {
                "query": user_query,
                "error": str(e),
                "explanation": f"Ocorreu um erro ao processar sua consulta: {str(e)}"
            }
    
    def generate_example_questions(self, num_questions=30):
        """Generate example questions for the RAG system"""
        return self.question_generator.generate_questions(num_questions)
    
    def save_example_questions(self, filename="perguntas_exemplo.json", num_questions=30):
        """Generate and save example questions to a file"""
        questions = self.generate_example_questions(num_questions)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        return questions
    
    def load_example_questions(self, filename="perguntas_exemplo.json"):
        """Load example questions from a file"""
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                questions = json.load(f)
            return questions
        else:
            return self.get_default_questions()
    
    def get_default_questions(self):
        """Return default example questions"""
        return self.question_generator.get_default_questions()
    
    def evaluate_on_examples(self, examples=None, save_results=True, output_format="direct"):
        """Evaluate the RAG system on example questions"""
        if examples is None:
            examples = self.get_default_questions()
        
        results = []
        
        for i, question in enumerate(examples):
            print(f"Processando pergunta {i+1}/{len(examples)}: {question}")
            try:
                result = self.process_query(question, output_format)
                results.append(result)
            except Exception as e:
                results.append({
                    "query": question,
                    "error": str(e)
                })
        
        if save_results:
            with open("resultados_avaliacao.json", "w", encoding="utf-8") as f:
                # Convert DataFrame to dictionary before serialization
                for result in results:
                    if "results" in result and isinstance(result["results"], pd.DataFrame):
                        result["results"] = result["results"].to_dict(orient="records")
                json.dump(results, f, indent=2, ensure_ascii=False)
        
        return results


if __name__ == "__main__":
    # Check for API key
    api_key = os.environ.get("CLAUDE_API_KEY")
    if not api_key:
        print("Aviso: CLAUDE_API_KEY não encontrada nas variáveis de ambiente.")
        print("Por favor, configure sua chave de API Claude como uma variável de ambiente ou forneça-a ao inicializar o sistema RAG.")
        api_key = input("Digite a chave de API Claude (ou pressione Enter para sair): ")
        if not api_key:
            print("Nenhuma chave de API fornecida. Saindo.")
            exit()
    
    # Initialize RAG system
    rag_system = RAGSystem(api_key=api_key)
    
    # Generate and save example questions
    print("Gerando perguntas de exemplo...")
    questions = rag_system.save_example_questions()
    print(f"Foram geradas {len(questions)} perguntas de exemplo.")
    
    # Interactive mode
    print("\nEntrando no modo interativo. Digite 'sair' para encerrar.")
    print("Para definir o formato: direct, summary, bullet (padrão: direct)")
    print("Para escolher um formato: 'formato: pergunta' (ex: 'bullet: Qual foi o total de vendas?')")
    
    while True:
        user_input = input("\nDigite sua pergunta: ")
        if user_input.lower() in ['sair', 'exit']:
            break
        
        # Check if format specified
        output_format = "direct"
        if ":" in user_input and user_input.split(":")[0].strip().lower() in ["default", "direct", "summary", "bullet"]:
            output_format, query = user_input.split(":", 1)
            output_format = output_format.strip().lower()
            query = query.strip()
        else:
            query = user_input
        
        result = rag_system.process_query(query, output_format)
        
        # Mostrar apenas a explicação/resposta final
        if "error" in result:
            print(f"Erro: {result['error']}")
        else:
            print(result["explanation"]) 