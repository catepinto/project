def phone(number):
    """Formats value as a phone number."""
    if not number:
        return f"None"
    else:
        # SOURCE: https://docs.python.org/3.6/reference/lexical_analysis.html#f-strings
        number = f"{number!s}"
        return f"({number[0]}{number[1]}{number[2]}) {number[3]}{number[4]}{number[5]}-{number[6]}{number[7]}{number[8]}{number[9]}"
