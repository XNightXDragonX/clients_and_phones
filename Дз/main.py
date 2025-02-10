import psycopg2


def connect_db():
        return psycopg2.connect(database="task5", user="postgres", password="Fedia_38_2025")


def create_db():
    conn= connect_db()
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE IF EXISTS phones;
            DROP TABLE IF EXISTS clients;   
            """)
        cur.execute("""
            CREATE TABLE clients (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE phones (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
                phone_number VARCHAR(20) UNIQUE    
            );
        """)
        conn.commit()
    conn.close()


def add_client(first_name, last_name, email):
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clients (first_name, last_name, email)
            VALUES (%s, %s, %s) RETURNING id;
        """, (first_name, last_name, email))
        client_id = cur.fetchone()[0]
        conn.commit()
    conn.close()
    return client_id
          

def add_phone(client_id, phone_number):
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phones (client_id, phone_number)
            VALUES (%s, %s);
        """, (client_id, phone_number))
        conn.commit()
    conn.close()


def update_client(client_id, first_name=None, last_name=None, email=None):
    conn = connect_db()
    with conn.cursor() as cur:
        if first_name:
            cur.execute("UPDATE clients SET first_name=%s WHERE id=%s;", (first_name, client_id))
        if last_name:
            cur.execute("UPDATE clients SET last_name=%s WHERE id=%s;", (last_name, client_id))
        if email:
            cur.execute("UPDATE clients SET email=%s WHERE id=%s;", (email, client_id))
        conn.commit()
    conn.close()


def delete_phone(client_id, phone_number):
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM phones WHERE client_id=%s AND phone_number=%s;", (client_id, phone_number))
        conn.commit()
    conn.close()


def delete_client(client_id):
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM clients WHERE id=%s;", (client_id,))
        conn.commit()
    conn.close()


def find_client(first_name=None, last_name=None, email=None, phone=None):
    conn = connect_db()
    with conn.cursor() as cur:
        query = """
                SELECT c.id, c.first_name, c.last_name, c.email, p.phone_number
                FROM clients AS c
                LEFT JOIN phones AS p ON c.id = p.client_id
                WHERE (%s IS NULL OR c.first_name = %s)
                    AND (%s IS NULL OR c.last_name = %s)
                    AND (%s IS NULL OR c.email = %s)
                    AND (%s IS NULL OR p.phone_number = %s);
        """
        cur.execute(query, (first_name, first_name, last_name, last_name, email, email, phone, phone))
        results = cur.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    create_db()


    client1 = add_client("Иван", "Иванов", "ivan@gmail.com")
    client2 = add_client("Анна", "Иоановна", "anna@gmail.com")


    add_phone(client1, "11111111111")
    add_phone(client1, "22222222222")
    add_phone(client2, "33333333333")


    update_client(client1, first_name="Дмитрий", email="dmitriy@yandex.ru")


    print("Поиск по имени:", find_client(first_name="Дмитрий"))
    print("Поиск по почте:", find_client(email="dmitriy@yandex.ru"))
    print("Поиск по телефону:", find_client(phone="11111111111"))


    delete_phone(client1, "22222222222")


    delete_client(client2)


    print("Поиск после удаления:", find_client())