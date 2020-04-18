"""
db.py
"""
from sqlite3 import PARSE_DECLTYPES, Connection, Row, connect

import click
from flask import Flask, current_app, g
from flask.cli import with_appcontext


def get_db() -> Connection:
    """Returns database connection."""
    if "db" not in g:
        g.db = connect(
            current_app.config["DATABASE"], detect_types=PARSE_DECLTYPES,
        )
        g.db.row_factory = Row
    return g.db


def close_db(exc: Exception = None) -> None:  # pylint: disable=unused-argument
    """Closes database connection."""
    connection = g.pop("db", None)
    if connection:
        connection.close()


def init_db() -> None:
    """Initialize database."""
    connection = get_db()

    with current_app.open_resource("schema.sql") as schema:
        connection.executescript(schema.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app: Flask) -> None:
    """Register close_db and init_db_command functions with the app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
