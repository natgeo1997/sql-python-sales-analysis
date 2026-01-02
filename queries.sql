-- Total de vendas por categoria
SELECT
    Category,
    SUM(Sales) AS total_vendas
FROM sales
GROUP BY Category
ORDER BY total_vendas DESC;

-- Lucro total por região
SELECT
    Region,
    SUM(Profit) AS lucro_total
FROM sales
GROUP BY Region
ORDER BY lucro_total DESC;
