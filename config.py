import os

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '3707',
    'auth_plugin': 'mysql_native_password',
    'database': 'kuafor_db'
}

DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"