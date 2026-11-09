"""Module mini calculator: cac ham tinh toan co ban."""

def add(a: float, b: float) -> float:
    """Cong hai so a va b."""
    return a + b

def sub(a: float, b: float) -> float:
    """Tru hai so a va b."""
    return a - b

def mul(a: float, b: float) -> float:
    """Nhan hai so a va b."""
    return a * b

def div(a: float, b: float) -> float:
    """Chia hai so a va b."""
    if b == 0:
        raise ValueError("Khong chia duoc")
    return a / b
