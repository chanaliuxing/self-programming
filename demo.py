"""
Sample demo module for self-programming engine testing and refactoring.
"""

def calculate_factorial(n: int) -> int:
    """Calculate the factorial of a positive integer."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n in (0, 1):
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def reverse_string(s: str) -> str:
    """Reverse a given string."""
    return s[::-1]
