import re
from dataclasses import dataclass
from errors import FoodParsingError

PATTERN_AMOUNT_UNIT_BEGINNING = re.compile(
    r"^(?P<amount>\d+(?:\.\d+)?)\s*(?P<unit>[a-zA-Z]+)\s+(?P<food>[a-zA-Z ]+)$"
)

PATTERN_AMOUNT_UNIT_ENDING = re.compile(
    r"^(?P<food>[a-zA-Z ]+)\s+(?P<amount>\d+(?:\.\d+)?)\s*(?P<unit>[a-zA-Z]+)$"
)

PATTERN_NUMBER_ONLY_BEGINNING = re.compile(
    r"^(?P<amount>\d+(?:\.\d+)?)\s+(?P<food>[a-zA-Z ]+)$"
)

PATTERN_NUMBER_ONLY_ENDING = re.compile(
    r"^(?P<food>[a-zA-Z ]+)\s+(?P<amount>\d+(?:\.\d+)?)$"
)

PATTERN_FOOD_ONLY = re.compile(
    r"^[a-zA-Z ]+$"
)


@dataclass(frozen=True)
class ParsedFood:
    name: str
    amount: float
    unit: str


def parse_food_input(user_input: str):
    text = user_input.strip().lower().replace(",", ".")

    for pattern in (
        PATTERN_AMOUNT_UNIT_BEGINNING,
        PATTERN_AMOUNT_UNIT_ENDING,
    ):
        match = pattern.match(text)
        if match:
            return ParsedFood(
                name=match.group("food").strip(),
                amount=float(match.group("amount")),
                unit=match.group("unit"),
            )

    for pattern in (
        PATTERN_NUMBER_ONLY_BEGINNING,
        PATTERN_NUMBER_ONLY_ENDING,
    ):
        match = pattern.match(text)
        if match:
            return ParsedFood(
                name=match.group("food").strip(),
                amount=float(match.group("amount")),
                unit="portion",
            )

    # fallback: food name only
    if PATTERN_FOOD_ONLY.fullmatch(text):
        return ParsedFood(
            name=text,
            amount=1,
            unit="portion",
        )
    
    raise FoodParsingError(f"Unrecognized food input: '{user_input}'")