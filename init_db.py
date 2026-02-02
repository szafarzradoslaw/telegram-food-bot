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
        
        conn.execute("""
                CREATE TABLE IF NOT EXISTS food_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    food_id INTEGER NOT NULL,
                    quantity REAL NOT NULL,
                    log_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (food_id) REFERENCES food_macros(id)
                )
            """)
    
    print("Database created")

if __name__ == "__main__":
    init_db()