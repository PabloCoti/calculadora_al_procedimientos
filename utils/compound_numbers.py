import re


def compound_parse(string):
    # Get the complex number structure
    pattern = r"\([-]?[0-9]+[+-][0-9]+i\)"

    # Separate complex from operands
    c_numbers = re.findall(pattern, string)
    operands = re.split(pattern, string)

    # The list appears as ['', op, op, ''], this turns it into [op, op]
    operands.pop()
    operands.reverse()
    operands.pop()
    operands.reverse()

    # Check if the structure is correct
    if c_numbers is not None and len(operands) < len(c_numbers):
        for op in operands:
            if op == '*':
                c_numbers[0] = compound_mult(c_numbers[0], c_numbers[1])
                c_numbers.remove(c_numbers[1])

            elif op == '+':
                c_numbers[0] = compound_add(c_numbers[0], c_numbers[1])
                c_numbers.remove(c_numbers[1])

            elif op == '/':
                c_numbers[0] = compound_div(c_numbers[0], c_numbers[1])
                c_numbers.remove(c_numbers[1])

            elif op == '-':
                c_numbers[0] = compound_sub(c_numbers[0], c_numbers[1])
                c_numbers.remove(c_numbers[1])

        return c_numbers[0]

def compound_mult(str1, str2):
    pattern = r"\(([-]?[0-9]+)([+-][0-9]+)i\)"

    str1_n = re.findall(pattern, str1)
    str2_n = re.findall(pattern, str2)

    r_result_1 = int(str1_n[0][0]) * int(str2_n[0][0])
    r_result_2 = (int(str1_n[0][1]) * int(str2_n[0][1]))*-1
    r_result = r_result_1 + r_result_2
    i_result = (int(str1_n[0][0]) * int(str2_n[0][1])) + (int(str1_n[0][1]) * int(str2_n[0][0]))

    if i_result != 0:
        result = f"({r_result}+{i_result}i)" if i_result > 0 else f"({r_result}{i_result}i)"

    else:
        result = r_result
    return result

def compound_add(str1, str2):
    pattern = r"\(([-]?[0-9]+)([+-][0-9]+)i\)"

    str1_n = re.findall(pattern, str1)
    str2_n = re.findall(pattern, str2)

    r_result = int(str1_n[0][0]) + int(str2_n[0][0])
    i_result = int(str1_n[0][1]) + int(str2_n[0][1])

    result = f"({r_result}+{i_result}i)" if i_result > 0 else f"({r_result}{i_result}i)"
    return result

def compound_div(str1, str2):
    pattern = r"\(([-]?[0-9]+)([+-][0-9]+)i\)"

    str1_n = re.findall(pattern, str1)
    str2_n = re.findall(pattern, str2)

    prev_str2 = str2

    complementary = int(str2_n[0][1]) * -1

    str2 = f"({str2_n[0][0]}{complementary}i)"

    numerator = compound_mult(str1, str2)
    denominator = compound_mult(prev_str2, str2)

    numerator_n = re.findall(pattern, numerator)

    r_result = int(numerator_n[0][0])/denominator
    if r_result % 1 != 0:
        r_result = f"{numerator_n[0][0]}/{denominator}"

    i_result = int(numerator_n[0][1])/denominator
    positive = False
    if i_result > 0:
        positive = True

    if i_result % 1 != 0:
        i_result = f"{numerator_n[0][1]}/{denominator}"

    if positive is True:
        result = f"({r_result}+{i_result}i)"
    else:
        result = f"({r_result}{i_result}i)"

    return result

def compound_sub(str1, str2):
    pattern = r"\(([-]?[0-9]+)([+-][0-9]+)i\)"

    str1_n = re.findall(pattern, str1)
    str2_n = re.findall(pattern, str2)

    r_result = int(str1_n[0][0]) + (int(str2_n[0][0])*-1)
    i_result = int(str1_n[0][1]) + (int(str2_n[0][1])*-1)

    result = f"({r_result}+{i_result}i)" if i_result > 0 else f"({r_result}{i_result}i)"
    return result
