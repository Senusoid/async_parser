import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = f'{BASE_DIR}/config/config.json'
DATETIME_FORMAT = "%d/%m/%y %H:%M"

db_credentials = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'database': os.getenv('POSTGRES_DB', 'app_db'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'password'),
    'port': os.getenv('POSTGRES_PORT', '5433')
}
