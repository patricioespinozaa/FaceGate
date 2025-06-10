import os

PORT = 8911
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'DB_UCampus')
DB_CREDENTIALS = {
    "host": "localhost",
    "user": "grupo3",
    "password": "piagrupo3",
    "database": "ucampus_db"
}
