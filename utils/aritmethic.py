import re


def parse_aritmethic(op_string):
    pattern = r"[0-9]+"

    # Gets all the characthers that match with the pattern 545+7 turns into ['546', '7']
    numbers = re.findall(pattern, op_string)
    # Gets all the characters that don't match the pattern 546+7 turns into ['', '+', '']
    operands = re.split(pattern, op_string)

    # remove empty characters from list
    operands.pop()
    operands.reverse()
    operands.pop()
    operands.reverse()

    # turn every number into int '5' to 5
    for c, n in enumerate(numbers):
        numbers[c] = int(n)

    if operands is not None and len(numbers) > len(operands):
        for op in operands:
            if op == '*':
                numbers[0] = numbers[0]*numbers[1]
                numbers.remove(numbers[1])

            elif op == '+':
                numbers[0] = numbers[0]+numbers[1]
                numbers.remove(numbers[1])

            elif op == '/':
                numbers[0] = numbers[0]/numbers[1]
                numbers.remove(numbers[1])

            elif op == '-':
                numbers[0] = numbers[0]-numbers[1]
                numbers.remove(numbers[1])

        return numbers[0]