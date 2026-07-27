from manager import DBManager
from psycopg.rows import dict_row
import json

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

    q1_result = execute_query(manager, sql_query_1)
    print(q1_result)

    q2_result = execute_query(manager, sql_query_2)
    print(q2_result)

    q3_result = execute_query(manager, sql_query_3)
    print(q3_result)

    q4_result = execute_query(manager, sql_query_4)
    print(q4_result)

def execute_query(manager:DBManager, sql_query: str):
    result = None
    with manager.conn.transaction():
        with manager.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql_query)
            
            result = cur.fetchmany(5)
    
    return result


