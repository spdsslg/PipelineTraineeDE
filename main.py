from manager import DBManager
import loader
import processing
import sys
import psycopg
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('rooms_path', help='Rooms file path')
    parser.add_argument('students_path', help='Students file path')
    parser.add_argument('format', help='Out data format')
    
    args = parser.parse_args()
    rooms_path = args.rooms_path
    students_path = args.students_path
    format = args.format

    while not (format == 'json' or format == 'xml'):
        print("Incorrect format, try again!")
        format = input('Out data format: ')

    try:
        db_manager = DBManager()

        loader.load(db_manager, rooms_path, students_path)
        db_manager.create_index()
        
        processing.process(db_manager, format)

        print('Out files are successfully created')
    except Exception as e:
        print(f"A general exception occurred: {e} ")
        sys.exit(1)

    except psycopg.Error as pe:
        print(f"A psycopg error occurred: {pe}")
        sys.exit(1)


    