from dataclasses import dataclass


@dataclass
class OptmProblem:
    num_vars: int
    num_restrictions: int
    obj_function: list
    restrictions: dict


def read_problem_example_file(file_name: str) -> OptmProblem:
    """
    Reads a text file from data folder and gets some of its optimzation problem info.
    Args:
        file_name (str): name of the file to be read
    Returns:
        (OptmProblem): OptimizationProblem object filled with .txt file data
    """
    # reading file
    with open(f'../data/{file_name}.txt', 'r') as file:
        lines = file.readlines()

    # useful info
    num_vars = 0
    num_restrictions = 0
    restrictions = {}
    obj_function = []

    # getting useful info
    for index, line in enumerate(lines):
        # first line, sets number of vars and restrictions
        if not index:
            num_vars, num_restrictions = [int(value) for value in line.split() if value.isdigit()]
        # second line, sets objective function coefficients
        elif index == 1:
            obj_function = [int(value) for value in line.split() if value.isdigit()]
        else:
            # third line on, adds restrictions
            restrictions[index - 1] = [int(value) for value in line.split() if value.isdigit()]

    return OptmProblem(num_vars=num_vars,
                       num_restrictions=num_restrictions,
                       obj_function=obj_function,
                       restrictions=restrictions)


if __name__ == "__main__":
    read_problem_example_file(file_name='problem_example_1')
