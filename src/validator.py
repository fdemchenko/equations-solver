from typing import Any

class Validator:
    @staticmethod
    def validate_float_number(number: Any) -> bool:
        try:
            result = float(number)
            return True
        except ValueError or TypeError:
            return False
