import os

#PATH TO DATABASE
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILENAME = "document_database"
DATABASE_PATH = os.path.join(BASE_DIR, "database", DATABASE_FILENAME)
