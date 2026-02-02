from database import get_connection

def test_rows(table_name):
    with get_connection() as conn:
        rows = conn.execute(f"SELECT * FROM {table_name}").fetchall()
        for row in rows:
            print(dict(row))

def test_columns(table_name):
    with get_connection() as conn:
        cursor = conn.execute(f"PRAGMA table_info({table_name});")
        for col in cursor.fetchall():
            print(dict(col))

if __name__ == "__main__":
    test_rows("food_log")
    #test_rows("food_log")
    #test_columns("food_macros")