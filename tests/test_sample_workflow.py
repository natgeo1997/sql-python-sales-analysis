import hashlib
from pathlib import Path
import sqlite3
import subprocess
import sys

import pandas as pd
import pytest
from build_demo_database import create_database

ROOT = Path(__file__).resolve().parents[1]


def test_sample_end_to_end_preserves_database_and_matches_known_totals(tmp_path):
    db = tmp_path/'sample.db'
    assert create_database(db) == 7
    checksum = hashlib.sha256(db.read_bytes()).hexdigest()
    out = tmp_path/'reports'
    subprocess.run([sys.executable, str(ROOT/'analysis.py'), '--database', str(db), '--output-dir', str(out), '--no-show'], check=True)
    actual = pd.read_csv(out/'total_vendas_por_categoria.csv')
    assert actual.set_index('Category')['total_vendas'].to_dict() == {'Technology': 450, 'Furniture': 300, 'Office Supplies': 50}
    assert (out/'grafico_vendas_por_categoria.png').stat().st_size > 0
    with sqlite3.connect(db) as conn:
        query = (ROOT/'queries.sql').read_text().split(';')[1]
        assert conn.execute(query).fetchall() == [('Southeast',72),('South',48),('North',10)]
    assert hashlib.sha256(db.read_bytes()).hexdigest() == checksum


def test_database_builder_never_replaces_existing_file(tmp_path):
    db = tmp_path/'sample.db'
    db.write_bytes(b'keep this existing file')
    with pytest.raises(FileExistsError):
        create_database(db)
    assert db.read_bytes() == b'keep this existing file'
