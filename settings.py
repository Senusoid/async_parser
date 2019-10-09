import os


CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = f'{CONFIG_PATH}/config.json'

DATETIME_FORMAT = "%d/%m/%y %H:%M"
db_credentials = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'app_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'port': os.getenv('DB_PASSWORD', '5433')
}
