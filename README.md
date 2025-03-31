# Sistema RAG para Banco de Dados com API Claude

Um sistema de Recuperação Aumentada por Geração (RAG) que interage com bancos de dados existentes, interpreta consultas em linguagem natural e fornece respostas precisas com base nas informações do banco de dados.

## Funcionalidades

- Conversão de linguagem natural para SQL
- Integração com banco de dados SQLite
- Integração com API Claude para interpretação de consultas e geração de respostas
- Geração de perguntas de exemplo para testes e avaliação
- Modo interativo para consultar o banco de dados

## Requisitos

- Python 3.8+
- Chave da API Claude
- Dependências do arquivo requirements.txt

## Instalação

1. Clone este repositório ou baixe os arquivos
2. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

3. Configure sua chave da API Claude como uma variável de ambiente:

```bash
# Windows
set CLAUDE_API_KEY=sua_chave_api_aqui

# macOS/Linux
export CLAUDE_API_KEY=sua_chave_api_aqui
```

## Uso

### Executando o Sistema RAG

Para executar o sistema RAG em modo interativo:

```bash
python rag_app.py
```

Isso irá:
1. Inicializar o sistema RAG
2. Gerar 30 perguntas de exemplo e salvá-las em `perguntas_exemplo.json`
3. Entrar no modo interativo onde você pode fazer perguntas sobre o banco de dados

### Fluxo de Trabalho de Exemplo

Quando você executa o aplicativo, pode fazer perguntas como:

- "Qual foi o total de vendas para cada loja em janeiro de 2025?"
- "Qual loja teve o maior volume de vendas em 2025?"
- "Quais são os horários de pico de vendas em todas as lojas?"
- "Como as vendas nos finais de semana se comparam às dos dias úteis?"

O sistema irá:
1. Converter sua consulta em linguagem natural para SQL
2. Executar a consulta no banco de dados
3. Formatar e explicar os resultados

### Perguntas de Exemplo

O sistema gera automaticamente 30 perguntas de exemplo diversas que podem ser usadas para testar as capacidades do sistema. Essas perguntas são salvas em `perguntas_exemplo.json`.

Para avaliar o sistema com esses exemplos, você pode usar:

```python
from rag_app import RAGSystem

rag_system = RAGSystem(api_key="sua_chave_api_aqui")
resultados = rag_system.evaluate_on_examples()
```

Isso processará todas as perguntas de exemplo e salvará os resultados em `resultados_avaliacao.json`.

## Estrutura de Arquivos

- `rag_app.py`: Aplicativo principal
- `db_connector.py`: Utilitários de conexão com o banco de dados
- `query_executor.py`: Lógica de execução de consultas SQL
- `claude_client.py`: Cliente da API Claude
- `question_generator.py`: Gerador de perguntas de exemplo
- `perguntas_exemplo.json`: Perguntas de exemplo geradas
- `resultados_avaliacao.json`: Resultados da avaliação com perguntas de exemplo

## Personalização

Você pode personalizar o sistema modificando o seguinte:

- `RAGSystem.__init__`: Alterar o prompt do sistema ou o caminho do banco de dados
- `QuestionGenerator.get_default_questions`: Adicionar ou modificar perguntas padrão
- `claudeApp.ClaudeClient.generate_sql`: Modificar o prompt do sistema para geração de SQL

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter detalhes. 