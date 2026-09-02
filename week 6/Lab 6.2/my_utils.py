def greet(name):
    """Print a greeting message."""
    print(f"Hello, {name}!")


def is_prime(number):
    """Return True if number is prime, otherwise return False."""
    if number < 2:
        return False

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False

    return True
