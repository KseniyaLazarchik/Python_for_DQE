import sqlite3

def fetch_data_from_db(db_name):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM News;")

        records = cursor.fetchall()

        for record in records:
            print(record)

    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    finally:

        if connection:
            connection.close()


fetch_data_from_db('records.db')
