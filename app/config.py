import os

CACHE_SIZE = int(os.environ.get("JOHNNY_CACHE_FLUSH_SIZE", "1000"))
DB_CONN_STRING = os.environ.get("DB_CONN_STRING", "sqlite:///db.sqlite3")
