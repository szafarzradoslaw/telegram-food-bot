from database import get_connection

def init_db():
    """
    Initialize the database with required tables.
    Safe to run multiple times; existing tables won't be overwritten.
    """
    with get_connection() as conn:
        # Foods table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS food_macros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                calories_per_100g REAL NOT NULL,
                protein_per_100g REAL NOT NULL,
                fat_per_100g REAL NOT NULL,
                carbs_per_100g REAL NOT NULL,
                gram_per_portion REAL
                
            )
        """)
        print("Database initialized and foods table created successfully.")

if __name__ == "__main__":
    init_db()