from database import get_connection
from food_repository import get_food_by_name
from errors import UnitConversionError

def convert_units_to_grams(amount: float, unit: str, food_name: str) -> float:
    unit_key = unit.lower()
    with get_connection() as conn:
        food = get_food_by_name(conn, food_name.lower())
    
    UNIT_MULTIPLIER = {
        "g": 1,
        "kg": 1000,
        "ml": 1,   # for milk/water
        "l": 1000,
        "portion": food.gram_per_portion,
        "x": food.gram_per_portion  # same as portion
    }
    if unit_key not in UNIT_MULTIPLIER:
        raise UnitConversionError(f"Unit '{unit}' not recognized.")

    if unit_key in ["portion", "x"] and food.gram_per_portion is None:
        raise UnitConversionError(f"Food '{food_name}' does not have a defined portion.")
    return amount * UNIT_MULTIPLIER[unit_key]
    

def calculate_macros(food_name: str, amount: float, unit: str):
    with get_connection() as conn:
        food = get_food_by_name(conn, food_name)
    grams = convert_units_to_grams(amount, unit, food_name)
    macros = {
        "calories": food.calories_per_100g * grams / 100,
        "protein": food.protein_per_100g * grams / 100,
        "fat": food.fat_per_100g * grams / 100,
        "carbs": food.carbs_per_100g * grams / 100,
    }
    return macros