"""Aggregate sales by category from a user-supplied SQLite database."""
import argparse
from pathlib import Path
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, required=True, help='SQLite database containing a sales table')
    parser.add_argument('--output-dir', type=Path, default=Path('.'))
    parser.add_argument('--no-show', action='store_true', help='Save the chart without opening a window')
    args = parser.parse_args()
    if not args.database.is_file():
        parser.error(f'Database not found: {args.database}. The source database is not included in this repository.')
    query = """
    SELECT Category, SUM(Sales) AS total_vendas
    FROM sales
    GROUP BY Category
    ORDER BY total_vendas DESC;
    """
    # Read-only access avoids creating or modifying the source database.
    with sqlite3.connect(args.database.resolve().as_uri() + '?mode=ro', uri=True) as conn:
        df = pd.read_sql_query(query, conn)
    print(df)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df['Category'], df['total_vendas'])
    ax.set(title='Total Sales by Category', xlabel='Category', ylabel='Total Sales (source units)')
    fig.tight_layout()
    fig.savefig(args.output_dir / 'grafico_vendas_por_categoria.png')
    df.to_csv(args.output_dir / 'total_vendas_por_categoria.csv', index=False)
    if not args.no_show:
        plt.show()
    plt.close(fig)


if __name__ == '__main__':
    main()
