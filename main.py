from manager import DBManager
import loader
import processing

if __name__ == '__main__':
    rooms_path = input('Rooms file path: ')
    students_path = input('Students file path: ')
    format = input('Out data format: ')
    while not (format == 'json' or format == 'xml'):
        print("Incorrect format, try again!")
        format = input('Out data format: ')


    db_manager = DBManager()

    loader.load(db_manager, rooms_path, students_path)
    db_manager.create_index()
    
    processing.process(db_manager, format)

    print('Out files are successfully created')


    