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
