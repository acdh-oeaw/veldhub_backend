from veld_registry.src.veld_registry import init_connection
from veld_registry.src.veld_registry import init_connection
from veld_validator.src.veld_validator import validate


if __name__ == "__main__":
    init_connection()
    validate(42)
