"""Create a new SQLite database from the repository's explicitly fictional CSV."""
import argparse
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
import sqlite3

SAMPLE = Path(__file__).resolve().parent / 'data/sample_sales.csv'


def create_database(output):
    output = Path(output)
    if output.exists():
        raise FileExistsError(f'Refusing to replace an existing database: {output}')
    with SAMPLE.open(newline='') as source:
        rows = list(csv.DictReader(source))
    if not rows:
        raise ValueError('Sample data is empty')
    records = []
    seen = set()
    for row in rows:
        identifier = row['OrderID'].strip()
        category, region = row['Category'].strip(), row['Region'].strip()
        if not identifier or identifier in seen or not category or not region:
            raise ValueError('Missing labels or duplicate order ID')
        seen.add(identifier)
        sales, profit = Decimal(row['Sales']), Decimal(row['Profit'])
        if not sales.is_finite() or not profit.is_finite() or sales < 0:
            raise ValueError('Amounts must be finite; sales must be nonnegative')
        records.append((identifier, category, float(sales), float(profit), region))
    output.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(output) as conn:
        conn.execute('CREATE TABLE sales (OrderID TEXT PRIMARY KEY, Category TEXT NOT NULL, Sales REAL NOT NULL CHECK (Sales >= 0), Profit REAL NOT NULL, Region TEXT NOT NULL)')
        conn.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', records)
    return len(records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('outputs/sample_sales.db'))
    args = parser.parse_args()
    try:
        count = create_database(args.output)
    except (FileExistsError, ValueError, InvalidOperation) as error:
        parser.error(str(error))
    print(f'Created {args.output} with {count} fictional records; not the original sales data.')


if __name__ == '__main__':
    main()
