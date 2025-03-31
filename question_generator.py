import json
from claude_client import ClaudeClient

class QuestionGenerator:
    """Generate diverse example questions for the RAG system"""
    
    def __init__(self, db_info, claude_client=None):
        """Initialize with database information and optional Claude client"""
        self.db_info = db_info
        self.claude_client = claude_client
    
    def generate_questions(self, num_questions=30):
        """Generate diverse example questions using Claude API"""
        if not self.claude_client:
            print("Cliente Claude não fornecido. Não é possível gerar perguntas.")
            return self.get_default_questions()
        
        system_prompt = """
        Você é um assistente prestativo que gera perguntas diversas e realistas sobre um banco de dados.
        As perguntas devem abranger diferentes tipos de consultas, desde simples até complexas, e devem ser
        projetadas para testar a capacidade de um sistema RAG de interpretar linguagem natural e gerar consultas SQL.
        
        As perguntas devem ter complexidade e tópicos variados, abrangendo diferentes aspectos dos dados,
        tais como:
        - Análise temporal (tendências ao longo do tempo, comparações entre períodos)
        - Análise focada em entidades (informações sobre lojas específicas, produtos, etc.)
        - Agregação e agrupamento (totais, médias, contagens por categoria)
        - Ordenação e classificação (melhores desempenhos, piores desempenhos)
        - Condições de filtragem (períodos de tempo específicos, limiares)
        - Relações complexas (correlações, se existirem nos dados)
        
        Retorne exatamente o número solicitado de perguntas em formato de array JSON.
        """
        
        # Prepare database schema info as a prompt
        db_schema_str = json.dumps(self.db_info, indent=2)
        
        prompt = f"""
        Com base nas seguintes informações do banco de dados:
        
        {db_schema_str}
        
        Gere {num_questions} perguntas diversas e realistas que poderiam ser feitas sobre este banco de dados.
        As perguntas devem variar em complexidade e tópico, e devem ser projetadas para testar a capacidade
        de um sistema RAG de entender linguagem natural e gerar consultas SQL.
        
        Por favor, retorne as perguntas como um array JSON de strings em português brasileiro.
        """
        
        response = self.claude_client.generate_response(prompt, system_prompt=system_prompt, temperature=0.8)
        
        try:
            # Try to extract JSON from the response
            if "```json" in response:
                json_text = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_text = response.split("```")[1].split("```")[0].strip()
            else:
                json_text = response.strip()
            
            questions = json.loads(json_text)
            return questions
        except Exception as e:
            print(f"Erro ao analisar perguntas geradas: {e}")
            return self.get_default_questions()
    
    def get_default_questions(self):
        """Return default questions in case generation fails"""
        return [
            "Qual foi o total de vendas para cada loja em janeiro de 2025?",
            "Qual loja teve o maior volume de vendas em 2025?",
            "Quais são os horários de pico de vendas em todas as lojas?",
            "Como as vendas nos finais de semana se comparam às dos dias úteis?",
            "Qual método de pagamento é mais utilizado em cada loja?",
            "Qual é o valor médio do ticket para cada loja?",
            "Como os descontos afetam o volume total de vendas?",
            "Qual loja tem o maior número de entregas?",
            "Quais são as tendências de vendas ao longo do tempo para a loja Alpha?",
            "Como o ticket médio evolui ao longo do dia?",
            "Quais dias da semana têm os maiores volumes de vendas?",
            "Qual é a receita total gerada por cada método de pagamento?",
            "Como as vendas de dezembro de 2025 se comparam às de janeiro de 2025?",
            "Qual é o número médio de itens por transação em cada loja?",
            "Qual loja tem a maior taxa de desconto?",
            "Qual horário do dia tem as maiores vendas médias?",
            "Quantas transações ocorrem por hora em cada loja?",
            "Qual é o custo total versus a receita total para cada loja?",
            "Qual loja tem a maior margem de lucro?",
            "Como as taxas de entrega variam ao longo do dia?",
            "Qual porcentagem de vendas vem de cada método de pagamento?",
            "Qual loja mostrou o maior crescimento em vendas ao longo do tempo?",
            "Qual é a relação entre a porcentagem de desconto e o total de vendas?",
            "Como o número de itens por transação varia por loja?",
            "Qual é a hora mais movimentada para cada loja?",
            "Como as vendas se comparam entre a primeira e a segunda metade do mês?",
            "Qual loja tem a maior fidelidade do cliente com base em transações repetidas?",
            "Qual é o impacto dos benefícios PBM nas vendas totais?",
            "Como se comparam os pagamentos em dinheiro versus cartão nas lojas?",
            "Qual é o valor médio de transação por método de pagamento?"
        ] 