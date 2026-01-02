import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("../database/sales.db")

query = """
SELECT
    Category,
    SUM(Sales) AS total_vendas
FROM sales
GROUP BY Category
ORDER BY total_vendas DESC;
"""

df = pd.read_sql_query(query, conn)
print(df)

plt.figure(figsize=(8,5))
plt.bar(df["Category"], df["total_vendas"])
plt.title("Total de Vendas por Categoria")
plt.xlabel("Categoria")
plt.ylabel("Total de Vendas")
plt.tight_layout()
plt.savefig("grafico_vendas_por_categoria.png")
plt.show()

df.to_csv("total_vendas_por_categoria.csv", index=False)
print("Arquivo CSV gerado com sucesso!")

conn.close()

