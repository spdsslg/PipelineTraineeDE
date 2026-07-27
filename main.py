from manager import DBManager
import loader

if __name__ == '__main__':
    rooms_path = input()
    students_path = input()
    format = input()

    db_manager = DBManager()

    loader.load(db_manager, rooms_path, students_path)
    

    