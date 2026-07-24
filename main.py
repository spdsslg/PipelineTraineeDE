import psycopg2
from psycopg2 import sql

db_name = "dormitory"

def create_db():
    """
    Create a database `db_name` if doesn't exist
    """
    postgres_conn = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='postgres')

    postgres_conn.autocommit = True

    with postgres_conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname=%s;", (db_name,))
        exists = cur.fetchone()

        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))) #avoids injection
            print(f"Created {db_name}")
        else:
            print(f"{db_name} already exists")
    
    postgres_conn.close()


if __name__ == '__main__':
    create_db()