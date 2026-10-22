def is_positive_negative_zero(num):
    """Check whether a number is positive, negative, or zero."""
    if num > 0:
        return "positive"
    elif num < 0:
        return "negative"
    else:
        return "zero"

def is_even_odd(num):
    """Check whether a number is even or odd."""
    if num % 2 == 0:
        return "even"
    else:
        return "odd"

num = int(input("Enter a number: "))

sign = is_positive_negative_zero(num)
number_type = is_even_odd(num)

print(f"The number is {sign} and {number_type}")