import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection

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
            #avoids injection
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Created {db_name}")
        else:
            print(f"{db_name} already exists")
    
    postgres_conn.close()

def create_tables(conn: connection):
    student_create = """ 
    CREATE TABLE IF NOT EXISTS student (
        id int NOT NULL,
        room int NOT NULL,
        name varchar(50) NOT NULL,
        birthday DATE NOT NULL,
        sex VARCHAR(1) NOT NULL,
        PRIMARY KEY (id),
        CONSTRAINT fk_room_student 
            FOREIGN KEY (room)
            REFERENCES room(id)
    );
    """

    room_create = """
    CREATE TABLE IF NOT EXISTS room (
        id int NOT NULL,
        name varchar(25) NOT NULL,
        PRIMARY KEY (id)
    );
    """

    student_add_constraints = """
    ALTER TABLE student
    ADD CONSTRAINT fk_room_student FOREIGN KEY (room)
    REFERENCES room(id);
    """

    #automatically commits or rolls back
    with conn: 
        with conn.cursor() as cur:
            cur.execute(room_create)
            cur.execute(student_create)
            print("Tables 'student' and 'room' were created/already exist")


if __name__ == '__main__':
    create_db()

    conn = psycopg2.connect(user='postgres', password='postgres', dbname=db_name, host='localhost')

    create_tables(conn)

    conn.close()