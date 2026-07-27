from manager import DBManager
from psycopg.rows import dict_row
import json
from lxml import etree
from decimal import Decimal

def process(manager: DBManager, format: str):
    sql_query_1 = """
    SELECT r.id, COUNT(s.id) AS students_count
    FROM room r
    LEFT JOIN student s
      ON r.id = s.room_id
    GROUP BY r.id
    ORDER BY COUNT(s.id)
    """

    sql_query_2 = """
    SELECT r.id, AVG(EXTRACT(YEAR FROM age(CURRENT_DATE, s.birthday))) as avg_age
    FROM room r
    LEFT JOIN student s
    ON r.id = s.room_id
    GROUP BY r.id
    ORDER BY AVG(EXTRACT(YEAR FROM age(CURRENT_DATE, s.birthday)))
    LIMIT 5
    """

    sql_query_3 = """
    WITH room_age_diff AS (
        SELECT r.id,
            MAX(EXTRACT(YEAR from age(CURRENT_DATE, s.birthday))) - MIN(EXTRACT(YEAR from age(CURRENT_DATE, s.birthday))) as age_diff
        FROM room r
        LEFT JOIN student s
        ON r.id = s.room_id
        GROUP BY r.id
    )

    SELECT id, age_diff
    FROM room_age_diff
    WHERE age_diff IS NOT NULL
    ORDER BY age_diff DESC 
    LIMIT 5
    """

    sql_query_4 = """
    SELECT id
    FROM room r
    WHERE EXISTS (
        SELECT 1
        FROM student s
        WHERE r.id = s.room_id AND s.sex = 'M'
    ) AND EXISTS (
        SELECT 1
        FROM student s
        WHERE r.id = s.room_id AND s.sex = 'F'
    )
    ORDER BY id
    """

    results = []

    q1_result = execute_query(manager, sql_query_1)
    results.append(q1_result)
    
    q2_result = execute_query(manager, sql_query_2)
    results.append(q2_result)

    q3_result = execute_query(manager, sql_query_3)
    results.append(q3_result)

    q4_result = execute_query(manager, sql_query_4)
    results.append(q4_result)

    num_of_queries = 4
    if(format == 'json'):
        for i in range(num_of_queries):
            save_to_json(results[i], i+1)
    elif(format == 'xml'):
        for i in range(num_of_queries):
            save_to_xml(results[i], i+1)
    else:
        print("Unknown format!")

def execute_query(manager:DBManager, sql_query: str):
    result = None
    with manager.conn.transaction():
        with manager.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql_query)
            
            result = cur.fetchall()
    
    return result

def save_to_json(data: str, query_num: int):
    out_filename = 'out_query'+str(query_num)+'.json'
    
    with open(out_filename, 'w') as fout:
        json.dump(data, fout, indent=4, default=decimal_serializer)

def save_to_xml(data: str, query_num: int):
    """
    Takes data from list of dictionaries and transformes each dictionary to `Element` object.
    `Element`s are written to the `.xml` file one by one.
    Uses lazy evaluation and avoids storing full xml-like object in memory.
    Lazy evaluation is achieved with `lxml` library and `etree.xmlfile`.
    Every Element is garbage collected after being written to the file
    """
    out_filename = 'out_query'+str(query_num)+'.xml'

    with etree.xmlfile(out_filename, encoding='utf-8') as xf:
        xf.write_declaration()

        with xf.element('root'):
            for item in data:
                elem = etree.Element('room')

                for key,val in item.items():
                    child = etree.SubElement(elem, key)
                    child.text = str(val) if not None else ""
                
                xf.write(elem, pretty_print=True)

def decimal_serializer(obj):
    if(isinstance(obj, Decimal)):
        return str(obj)
    
    print(f"Unable to serialise object of type {type(obj)}")