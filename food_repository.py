import sqlite3
from typing import Optional
from dataclasses import dataclass
from errors import FoodNotFoundError

@dataclass(frozen=True)
class Food:
    id: int
    name: str
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float
    gram_per_portion: Optional[float] = None

def add_food(
    conn: sqlite3.Connection,
    name: str,
    calories_per_100g: float,
    protein_per_100g: float,
    fat_per_100g: float,
    carbs_per_100g: float,
    gram_per_portion: Optional[float] = None,
) -> int:
    """
    Insert a new food and return its database id.
    Assumes name is already normalized and uniqueness checked.
    """
    cursor = conn.execute(
        """
        INSERT INTO foods (
            name,
            calories_per_100g,
            protein_per_100g,
            fat_per_100g,
            carbs_per_100g,
            gram_per_portion
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            name.strip().lower(),
            calories_per_100g,
            protein_per_100g,
            fat_per_100g,
            carbs_per_100g,
            gram_per_portion,
        ),
    )
    return cursor.lastrowid



def get_food_by_name(conn: sqlite3.Connection, name: str) -> Food:
    """
    Retrieve a food by name or raise FoodNotFoundError.
    """
    cursor = conn.execute(
        """
        SELECT
            id,
            name,
            calories_per_100g,
            protein_per_100g,
            fat_per_100g,
            carbs_per_100g,
            gram_per_portion
        FROM foods
        WHERE name = ?
        """,
        (name.strip().lower(),),
    )

    row = cursor.fetchone()
    if row is None:
        raise FoodNotFoundError(f"Food '{name}' not found.")

    return Food(
        id=row[0],
        name=row[1],
        calories_per_100g=row[2],
        protein_per_100g=row[3],
        fat_per_100g=row[4],
        carbs_per_100g=row[5],
        gram_per_portion=row[6],
    )
    
def food_exists(conn: sqlite3.Connection, name: str) -> bool:
    """
    Check whether a food with the given normalized name exists.
    """
    cursor = conn.execute(
        """
        SELECT 1
        FROM foods
        WHERE name = ?
        LIMIT 1
        """,
        (name.strip().lower(),),
    )
    return cursor.fetchone() is not None