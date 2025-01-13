def indent_right(s: str, width: int) -> str:
    return " " * (max(0, width - len(s))) + s
