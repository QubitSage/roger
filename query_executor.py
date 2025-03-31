from db_connector import DatabaseConnector
import re
import pandas as pd

class QueryExecutor:
    def __init__(self, db_connector=None):
        """Initialize with a database connector instance or create a new one"""
        self.db_connector = db_connector if db_connector else DatabaseConnector()
        
        # Common SQL query patterns for this database
        self.query_patterns = {
            "vendas_mensais": "SELECT loja_nome, total_liquido, data FROM dados_mensais",
            "vendas_diarias": "SELECT loja_nome, total_liquido, data, hora FROM dados_diarios",
            "vendas_por_mes": "SELECT loja_nome, SUM(total_liquido) as total FROM dados_mensais WHERE data LIKE '{year}-{month}-%' GROUP BY loja_nome",
            "vendas_por_dia": "SELECT loja_nome, SUM(total_liquido) as total FROM dados_mensais WHERE data LIKE '{year}-{month}-{day}' GROUP BY loja_nome",
            "max_vendas_por_hora": "SELECT d1.loja_nome, d1.total_liquido, d1.data, d1.hora FROM dados_diarios d1 WHERE d1.data LIKE '{pattern}' AND d1.total_liquido = (SELECT MAX(d2.total_liquido) FROM dados_diarios d2 WHERE d2.loja_nome = d1.loja_nome AND d2.data LIKE '{pattern}')",
            "metodos_pagamento": "SELECT data, loja_nome, MAX(dinheiro) as dinheiro, MAX(cheque) as cheque, MAX(cartao) as cartao, MAX(convenio) as convenio, MAX(deposito) as deposito, MAX(outros) as outros FROM dados_mensais GROUP BY loja_nome, data ORDER BY hora DESC",
            "evolucao_ticket": "SELECT data, loja_nome, tiket_medio, hora FROM dados_diarios ORDER BY data DESC, loja_nome LIMIT {limit}",
            "horas_entrega": "SELECT data, loja_nome, MAX(entregas_req) as max_entregas, hora FROM dados_diarios GROUP BY loja_nome ORDER BY hora DESC"
        }
    
    def execute_sql(self, query):
        """Execute a SQL query directly"""
        return self.db_connector.execute_query(query)
    
    def execute_pattern(self, pattern_name, **kwargs):
        """Execute a query using a predefined pattern with parameter substitution"""
        if pattern_name not in self.query_patterns:
            raise ValueError(f"Padrão de consulta desconhecido: {pattern_name}")
        
        query_template = self.query_patterns[pattern_name]
        query = query_template.format(**kwargs)
        return self.execute_sql(query)
    
    def extract_date_parts(self, date_string):
        """Extract year, month, day from a date string"""
        # Try different formats
        patterns = [
            r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})',  # yyyy-mm-dd or yyyy/mm/dd
            r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})',  # dd-mm-yyyy or dd/mm/yyyy
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_string)
            if match:
                groups = match.groups()
                if len(groups[0]) == 4:  # yyyy-mm-dd
                    return {"year": groups[0], "month": groups[1], "day": groups[2]}
                else:  # dd-mm-yyyy
                    return {"year": groups[2], "month": groups[1], "day": groups[0]}
        
        return None
    
    def extract_month_name(self, month_string):
        """Convert month name to number"""
        months = {
            "janeiro": "01", "jan": "01", "january": "01",
            "fevereiro": "02", "fev": "02", "february": "02",
            "março": "03", "mar": "03", "march": "03",
            "abril": "04", "abr": "04", "april": "04",
            "maio": "05", "mai": "05", "may": "05",
            "junho": "06", "jun": "06", "june": "06",
            "julho": "07", "jul": "07", "july": "07",
            "agosto": "08", "ago": "08", "august": "08",
            "setembro": "09", "set": "09", "september": "09",
            "outubro": "10", "out": "10", "october": "10",
            "novembro": "11", "nov": "11", "november": "11",
            "dezembro": "12", "dez": "12", "december": "12"
        }
        
        for month_name, month_num in months.items():
            if month_name in month_string.lower():
                return month_num
        
        return None
    
    def get_database_info(self):
        """Get information about the database structure"""
        tables = self.db_connector.get_tables()
        db_info = {"tables": []}
        
        for table in tables:
            schema = self.db_connector.get_table_schema(table)
            sample = self.db_connector.get_sample_data(table)
            
            # Convert sample data to a serializable format
            if sample is not None:
                sample_dict = sample.to_dict(orient="records")
            else:
                sample_dict = []
            
            table_info = {
                "name": table,
                "schema": schema,
                "sample_data": sample_dict
            }
            
            db_info["tables"].append(table_info)
        
        return db_info 