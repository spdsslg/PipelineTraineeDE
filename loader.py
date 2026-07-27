from manager import DBManager
import json

def load(manager: DBManager, rooms_path: str, students_path: str):
    with open(rooms_path, 'r') as rooms_file:
        json_rooms = json.load(rooms_file)

        insert_rooms(manager, json_rooms)
        
    with open(students_path, 'r') as students_file:
        json_students = json.load(students_file)

        insert_students(manager, json_students)

def insert_rooms(manager: DBManager, json_rooms: list):
    keys = ('id', 'name')

    #keys tuple in a generator expr prevents incorrect ordering
    rooms_tuples = (tuple(entry[key] for key in keys) for entry in json_rooms)
    #print(list(rooms_tuples))

    sql_insert = """
    INSERT INTO room (id, name) 
    VALUES (%s,%s)
    ON CONFLICT (id) DO NOTHING
    """
    
    with manager.conn.transaction():
        with manager.conn.cursor() as cur:
            cur.executemany(sql_insert, rooms_tuples)
    
    print("Inserted room values")

def insert_students(manager:DBManager, json_students: list):
    keys = ('id', 'room', 'name', 'birthday', 'sex')

    students_tuples = (tuple(entry[key] for key in keys) for entry in json_students)

    sql_insert = """
    INSERT INTO student (id, room_id, name, birthday, sex)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    """

    with manager.conn.transaction():
        with manager.conn.cursor() as cur:
            cur.executemany(sql_insert, students_tuples)

    print("Inserted student values")






