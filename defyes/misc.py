import pathlib

PROJECT_PATH = pathlib.Path(__file__).parent.resolve()


def get_db_filename(protocol_name):
    return PROJECT_PATH / "db" / f"{protocol_name}_db.json"
