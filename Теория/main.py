import psycopg2


conn = psycopg2.connect(database="netology_db", user="postgres", password="Fedia_38_2025")
with conn.cursor() as cur:
    cur.execute("""
        DROP TABLE IF EXISTS homework;
        DROP TABLE IF EXISTS course;
        """)
    

    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
            id SERIAL PRIMARY KEY,
            name VARCHAR(40) UNIQUE
        );
        """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS homework(
            id SERIAL PRIMARY KEY,
            number INTEGER NOT NULL,
            description TEXT NOT NULL,
            course_id INTEGER NOT NULL REFERENCES course(id)    
        );
        """)
    conn.commit()


    cur.execute("""
        INSERT INTO course(name) VALUES('Python');   
        """)
    conn.commit()

    cur.execute("""
        INSERT INTO course(name) VALUES('Java') RETURNING id, name;        
        """)
    print(cur.fetchone())

    cur.execute("""
        INSERT INTO homework(number, description, course_id) VALUES(1, 'простое дз', 1);     
        """)
    conn.commit()


    cur.execute("""
        SELECT * FROM course;     
        """)
    print('fetchall', cur.fetchall())

    cur.execute("""
        SELECT * FROM course;
        """)
    print(cur.fetchone())

    cur.execute("""
        SELECT * FROM course;
        """)
    print(cur.fetchmany(3))

    cur.execute("""
        SELECT name FROM course;
        """)
    print(cur.fetchall())

    cur.execute("""
        SELECT id FROM course
        WHERE name='Python';
        """)
    print(cur.fetchone())

    cur.execute("""
        SELECT id FROM course
        WHERE name=%s;
        """, ("Python",))
    print(cur.fetchone())


    def get_course_id(cursor, name: str) -> int:
        cursor.execute("""
            SELECT id FROM course WHERE name=%s;
            """, (name,))
        return cur.fetchone()[0]


    python_id = get_course_id(cur, 'Python')
    print('python_id', python_id)


    cur.execute("""
        INSERT INTO homework(number, description, course_id) VALUES(%s, %s, %s);
        """, (2, "задание для проверки", python_id))
    conn.commit()

    cur.execute("""
        SELECT * FROM homework;
        """)
    print(cur.fetchall())


    cur.execute("""
        UPDATE course SET name=%s WHERE id=%s;
        """, ('Pyhon Advanced', python_id))

    cur.execute("""
        SELECT * FROM course;
        """)
    print(cur.fetchall())


    cur.execute("""
        DELETE FROM homework WHERE id=%s;
        """, (1,))

    cur.execute("""
        SELECT * FROM homework;
        """)
    print(cur.fetchall())
    
    
conn.close()