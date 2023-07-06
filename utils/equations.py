from fractions import Fraction as FR
from .matrix import *
import re


def equation_parse(string, method):
    eq_list = string.split('\n')

    n_pattern = r'-?\d+'
    l_pattern = r'[a-zA-Z]'

    coefficients = []
    constants = []
    letters = []

    for eq in eq_list:
        numbers = re.findall(n_pattern, eq)
        letters = re.findall(l_pattern, eq)

        number_list = []
        for n in range(len(numbers)):
            if n != len(numbers) - 1:
                number_list.append(int(numbers[n]))
            else:
                constants.append(int(numbers[n]))

        coefficients.append(number_list)

    if method == 'Sustitución':
        return st_solve_equation(coefficients, constants, letters)

    elif method == 'Igualación':
        return ig_solve_equation(coefficients, constants, letters)

    elif method == 'Reducción':
        return rd_solve_equation(coefficients, constants, letters)

    elif method == 'Eliminación Gaussiana':
        return eg_solve_equation(coefficients, constants, letters)

    elif method == 'Gauss Jordan':
        return gj_solve_equation(coefficients, constants, letters)

    elif method == 'Sarrus':
        return sarrus_solve_equation(coefficients, constants, letters)


def st_solve_equation(coefficients, constants, letters):
    n = len(coefficients)
    procedure = ""

    # Solve for variables one by one
    for i in range(n - 1):
        # Solve equation i for the variable letters[i]
        equation = coefficients[i]
        constant = constants[i]
        x = letters[i]

        for j in range(i + 1, n):
            factor = coefficients[j][i] / equation[i]
            constants[j] -= factor * constant
            for k in range(i, n):
                coefficients[j][k] -= factor * equation[k]

        # Build equation string for procedure
        equation_str = " + ".join([f"{coefficients[i][j]}{letters[j]}" for j in range(n)])
        equation_str += f" = {constants[i]}"

        procedure += f"Solving equation for {x}:\n"
        procedure += equation_str + "\n\n"

    # Back substitution to find the values of remaining variables
    solution = [0] * n
    for i in range(n - 1, -1, -1):
        constant = constants[i]
        equation = coefficients[i]
        x = letters[i]

        for j in range(i + 1, n):
            constant -= equation[j] * solution[j]

        solution[i] = constant / equation[i]

        # Build equation string for procedure
        equation_str = " + ".join([f"{coefficients[i][j]}{letters[j]}" for j in range(n)])
        equation_str += f" = {constants[i]}"

        procedure += f"Substituting into equation for {x}:\n"
        procedure += equation_str + "\n\n"

    result = ''
    for l, s in enumerate(solution):
        result += f"{letters[l]}={FR(s).limit_denominator()} "

    procedure += result

    return procedure


def ig_solve_equation(coefficients, constants, letters):
    pass


def rd_solve_equation(coefficients, constants, letters):
    n = len(coefficients)

    # Applying the elimination method
    procedure = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            ratio = coefficients[j][i] / coefficients[i][i]
            procedure.append(f"R{j + 1} = R{j + 1} - {ratio:.2f} * R{i + 1}")
            for k in range(i, n):
                coefficients[j][k] -= ratio * coefficients[i][k]
            constants[j] -= ratio * constants[i]

    # Back substitution to find the solution
    solution = [0] * n
    solution[n - 1] = constants[n - 1] / coefficients[n - 1][n - 1]
    procedure.append(f"{letters[n - 1]} = {constants[n - 1] / coefficients[n - 1][n - 1]:.2f}")

    for i in range(n - 2, -1, -1):
        sum_term = 0
        for j in range(i + 1, n):
            sum_term += coefficients[i][j] * solution[j]
        solution[i] = (constants[i] - sum_term) / coefficients[i][i]
        procedure.append(f"{letters[i]} = ({constants[i]} - {sum_term:.2f}) / {coefficients[i][i]:.2f}")

    # Constructing the result string
    result = ''
    for i, letter in enumerate(letters):
        result += f"{letter} = {FR(solution[i]).limit_denominator()}, "

    final_result = ''
    for step in procedure:
        final_result += f"{step}\n"

    result = result[:-2]

    final_result += result

    return final_result


def eg_solve_equation(coefficients, constants, letters):
    n = len(coefficients)
    procedure = []

    # Applying Gaussian elimination
    for i in range(n):
        pivot = coefficients[i][i]
        procedure.append(f"Step {i + 1}: Divide Row {i + 1} by {pivot}")

        for j in range(i + 1, n):
            ratio = coefficients[j][i] / pivot
            procedure.append(f"Step {i + 1}: Subtract {ratio} times Row {i + 1} from Row {j + 1}")

            for k in range(n):
                coefficients[j][k] -= ratio * coefficients[i][k]

            constants[j] -= ratio * constants[i]

    # Back substitution to find the solution
    solution = [0] * n
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            constants[i] -= coefficients[i][j] * solution[j]

        solution[i] = constants[i] / coefficients[i][i]

    print(procedure)

    final_result = ''
    for step in procedure:
        final_result += f"{str(step)}\n"

    result = ''
    for l, s in enumerate(solution):
        result += f"{letters[l]}={FR(s).limit_denominator()}"

    final_result += result

    return final_result


def gj_solve_equation(coefficients, constants, letters):
    n = len(coefficients)
    procedure = []

    # Applying Gaussian elimination
    for i in range(n):
        pivot = coefficients[i][i]
        procedure.append(f"Step {i + 1}: Divide Row {i + 1} by {pivot}")

        for j in range(i + 1, n):
            ratio = coefficients[j][i] / pivot
            procedure.append(f"Step {i + 1}: Subtract {ratio} times Row {i + 1} from Row {j + 1}")

            for k in range(n):
                coefficients[j][k] -= ratio * coefficients[i][k]

            constants[j] -= ratio * constants[i]

    # Back substitution to find the solution
    solution = [0] * n
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            constants[i] -= coefficients[i][j] * solution[j]

        solution[i] = constants[i] / coefficients[i][i]

    result = ''
    for n, r in enumerate(solution):
        result += f"{letters[n]}={FR(r).limit_denominator()}, "

    final_result = ''
    for step in procedure:
        final_result += f"{step}\n"

    final_result += result

    return final_result


def sarrus_solve_equation(coefficients, constants, letters):
    procedure = ''

    # Calculate the identity's matrix determinant
    identity_det = matrix_determinant(coefficients)
    procedure += f"Se calcula la determinante de la matriz identidad\n{identity_det}"

    identity_det = identity_det.split('=')
    identity_det = int(identity_det[1])


    # if the determinant is not 0 that means that the system is solvable
    if identity_det != 0 and len(coefficients[0]) == 3:
        results = []

        for i in range(3):
            new_coefficients = coefficients.copy()

            for x in range(len(constants)):
                new_coefficients[x][i] = constants[x]

            procedure += f"\nSustituir los valores de las constantes en la matriz identidad: \n"
            for row in new_coefficients:
                for n in row:
                    procedure += f"{n} "
                procedure += '\n'

            procedure += f"\nCalcular la determinante de la nueva matriz\n"

            det = matrix_determinant(new_coefficients)
            procedure += det

            det = int(det.split('=')[1])

            procedure += f"\n\nDividir determinante dentro de determinante de identidad: \n"
            results.append(FR(det/identity_det).limit_denominator())
            procedure += str(FR(det/identity_det).limit_denominator())

        result = ''
        for n, l in enumerate(letters):
            result += f"{l}={results[n]}"

        procedure += f"\n{result}"

        return procedure

    else:
        return 'Error'