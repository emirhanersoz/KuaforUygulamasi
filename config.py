import os

# Örn: 'mysql+mysqlconnector://user:pass@localhost/kuafor'
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'mysql+mysqlconnector://root:password@127.0.0.1/kuafor'
)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '3707',
    'auth_plugin': 'mysql_native_password',
    'database': 'kuafor_db'
}