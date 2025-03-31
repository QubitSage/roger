import sqlite3
from pprint import pprint

conn = sqlite3.connect("dados.db")

# a = conn.execute("""
# SELECT t1.data, t1.loja_nome, t1.total_liquido, t1.hora FROM dados_diarios t1 WHERE t1.data !=
#                  (SELECT t2.data FROM dados_diarios t2) ORDER BY total_liquido DESC LIMIT 20
# """)
a = conn.execute("""

""")
b = a.fetchall()
pprint(b)
print(len(str(b)))

# SELECT GROUP_CONCAT(CONCAT('SELECT * FROM ', table_name) SEPARATOR ' UNION ALL ') 
# INTO @query
# FROM INFORMATION_SCHEMA.TABLES 
# WHERE table_name LIKE 'clientes_%';
conn.close()