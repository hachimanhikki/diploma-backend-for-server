def formated(s: str) -> str:
    return s.lower().strip()


def compare_strings(s1: str, s2: str) -> bool:
    if not isinstance(s1, str) or not isinstance(s2, str):
        return False
    return formated(s1) == formated(s2)


def clear_int(value) -> int:
    return int(value) if isinstance(value, (int, float)) else 0
