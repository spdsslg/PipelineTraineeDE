import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection

def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class DBManager():
    """
    DBManager class encapsulates the connection and creation of the schema
    """
    #class attributes of decorated class can't be accessed through the class name!
    db_name = "dormitory" 

    def __init__(self):
        self._create_db()

        self.conn = psycopg2.connect(user='postgres', password='postgres', dbname=self.db_name, host='localhost')

        self._create_tables()

    def _create_db(self):
        """
        Create a database `db_name` if doesn't exist
        """
        postgres_conn = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='postgres')

        postgres_conn.autocommit = True

        with postgres_conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname=%s;", (self.db_name,))
            exists = cur.fetchone()

            if not exists:
                #avoids injection
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.db_name)))
                print(f"Created {self.db_name}")
            else:
                print(f"{self.db_name} already exists")
        
        postgres_conn.close()

    def _create_tables(self):
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

        #automatically commits or rolls back
        with self.conn: 
            with self.conn.cursor() as cur:
                cur.execute(room_create)
                cur.execute(student_create)
                print("Tables 'student' and 'room' were created/already exist")

    # def close_connection(self):
    #     self.conn.close()

if __name__ == '__main__':
    db_manager = DBManager()

    