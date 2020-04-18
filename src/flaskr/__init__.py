"""
__init__.py
"""
from os import makedirs, path
from typing import Mapping, Optional

from flask import Flask


def create_app(test_config: Optional[Mapping] = None) -> Flask:
    """Create and configure the app."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(  # nosec
        SECRET_KEY="dev",
        DATABASE=path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile("config.py", silent=True)

    try:
        makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello() -> str:  # pylint: disable=unused-variable
        return "Hello, World!"

    from . import db  # pylint:disable=import-outside-toplevel

    db.init_app(app)

    return app
