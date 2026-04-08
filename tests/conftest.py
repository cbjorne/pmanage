import sqlite3
import pytest
from argparse import Namespace
from unittest.mock import patch
from pmanage.db import init_db


@pytest.fixture(autouse=True)
def tmp_db(tmp_path):
    """Redirect DB_PATH to a temp file for every test."""
    db_file = tmp_path / "test.db"
    with patch("pmanage.db.DB_PATH", db_file):
        # Also patch get_conn in every command module so they pick up the temp DB
        def _get_conn():
            conn = sqlite3.connect(db_file)
            conn.row_factory = sqlite3.Row
            return conn

        with (
            patch("pmanage.db.get_conn", _get_conn),
            patch("pmanage.commands.start.get_conn", _get_conn),
            patch("pmanage.commands.stop.get_conn", _get_conn),
            patch("pmanage.commands.status.get_conn", _get_conn),
            patch("pmanage.commands.log.get_conn", _get_conn),
            patch("pmanage.commands.projects.get_conn", _get_conn),
        ):
            init_db()
            yield _get_conn


def make_args(**kwargs):
    """Helper to build a Namespace mimicking parsed CLI args."""
    return Namespace(**kwargs)
