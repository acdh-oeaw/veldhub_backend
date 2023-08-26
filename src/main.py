
print("module: main")

from veld_registry.src.veld_registry import run

run()

from veld_validator.src.veld_validator import validate

validate(42)
