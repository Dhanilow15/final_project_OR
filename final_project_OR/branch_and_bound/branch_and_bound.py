from mip import *

from utils.read_problem_example_file import read_problem_example_file


def model_problem():
    # setting problem info object
    optm_problem = read_problem_example_file(file_name='problem_example_1')

    # modeling.py the problem
    optm_model = Model(sense=MAXIMIZE, solver_name=CBC)

    # creating vars dictionary
    x = {i + 1: optm_model.add_var(var_type=CONTINUOUS, name=f"x_{i + 1}")
         for i in range(optm_problem.num_vars)}

    # creating restrictions
    for coefficients in optm_problem.restrictions.values():
        optm_model += xsum(c*x[index+1] for index, c in enumerate(coefficients[:-1])) <= coefficients[-1]

    optm_model.write("model.lp")  # salva modelo em arquivo
    with open("model.lp", "r") as f:  # lê e exibe conteúdo do arquivo
        print(f.read())

if __name__ == "__main__":
    model_problem()


"""
from queue import LifoQueue
import numpy as np
import mip

def read_data(filename):
    with open(filename, 'r') as file:
        num_vars, num_constraints = map(int, file.readline().split())
        c = np.array(list(map(int, file.readline().split())))
        A = []
        b = []
        for _ in range(num_constraints):
            constraint = list(map(int, file.readline().split()))
            A.append(constraint[:-1])
            b.append(constraint[-1])
        return num_vars, num_constraints, c, A, b

def branch_and_bound(num_vars, num_constraints, c, A, b):
    # Inicialize a pilha com o nó raiz
    stack = LifoQueue()
    stack.put(([], 0))  # (variáveis fixadas, limite inferior)

    best_solution = None
    best_value = float('-inf')

    while not stack.empty():
        fixed_vars, lower_bound = stack.get()

        # Crie um novo modelo MIP
        model = mip.Model()

        # Crie as variáveis do modelo
        x = [model.add_var(var_type=mip.BINARY) for _ in range(num_vars)]

        # Adicione as restrições ao modelo
        for i in range(num_constraints):
            model.add_constr(sum(A[i][j] * x[j] for j in range(num_vars)) <= b[i])

        # Fixe as variáveis de acordo com o nó atual
        for var_index, var_value in fixed_vars:
            x[var_index].fix(var_value)

        # Defina a função objetivo
        model.objective = mip.maximize(sum(c[j] * x[j] for j in range(num_vars)))

        # Resolva o modelo
        model.optimize()

        # Verifique se encontrou uma solução inteira melhor
        if model.num_solutions:
            solution = [x[j].x for j in range(num_vars)]
            solution_value = model.objective_value

            if solution_value > best_value and all(np.isclose(x_value, 0) or np.isclose(x_value, 1) for x_value in solution):
                best_solution = solution
                best_value = solution_value

        # Verifique se o limite inferior é menor do que a melhor solução atual
        if lower_bound < best_value:
            # Encontre a variável fracionária mais próxima de 0.5
            fractional_index = None
            fractional_value = float('inf')

            for var_index, var in enumerate(x):
                var_value = var.x
                if not np.isclose(var_value, 0) and not np.isclose(var_value, 1):
                    distance_from_half = abs(var_value - 0.5)
                    if distance_from_half < fractional_value:
                        fractional_index = var_index
                        fractional_value = distance_from_half

            if fractional_index is not None:
                # Ramifique em torno da variável fracionária
                fixed_vars_0 = fixed_vars + [(fractional_index, 0)]
                fixed_vars_1 = fixed_vars + [(fractional_index, 1)]

                # Calcule os limites inferiores para cada ramificação
                lower_bound_0 = lower_bound
                lower_bound_1 = lower_bound

                model.optimize(relax=True)
                lower_bound_0 += model.objective_bound
                lower_bound_1 += model.objective_bound

                # Adicione os nós filhos à pilha
                stack.put((fixed_vars_0, lower_bound_0))
                stack.put((fixed_vars_1, lower_bound_1))

    return best_solution, best_value

# Ler dados do arquivo
num_vars, num_constraints, c, A, b = read_data('data.txt')

# Execute o algoritmo branch-and-bound
best_solution, best_value = branch_and_bound(num_vars, num_constraints, c, A, b)

# Imprima a melhor solução encontrada
print("Melhor solução:", best_solution)
print("Valor da função objetivo:", best_value)

"""