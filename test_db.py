from database import get_connection

def test_rows():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM food_macros").fetchall()
        for row in rows:
            print(dict(row))

def test_columns():
    with get_connection() as conn:
        cursor = conn.execute("PRAGMA table_info(food_macros);")
        for col in cursor.fetchall():
            print(dict(col))

if __name__ == "__main__":
    test_rows()
    #test_columns()
    # ood_id = add_food("orange", 47, 0.9, 0.1, 11.8)