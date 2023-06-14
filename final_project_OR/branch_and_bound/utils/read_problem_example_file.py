from dataclasses import dataclass
from collections import OrderedDict

import os


@dataclass
class OptmProblem:
    num_vars: int
    num_restrictions: int
    obj_function: list
    restrictions: dict


def get_path_to_data_folder():
    """
    This method returns the path to the data folder
    Returns:
        script_dir (str): path string
    """
    # get the path to the directory of the current script
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    # navigate up the directory hierarchy until the root of the project is reached
    while not os.path.exists(os.path.join(script_dir, "main.py")):
        script_dir = os.path.dirname(script_dir)

    # entering data folder
    script_dir += "/data"

    return script_dir


def read_problem_example_file(file_name: str) -> OptmProblem:
    """
    Reads a text file from data folder and gets some of its optimzation problem info.
    Args:
        file_name (str): name of the file to be read
    Returns:
        (OptmProblem): OptimizationProblem object filled with .txt file data
    """
    # reading file
    with open(f'{get_path_to_data_folder()}/{file_name}.txt', 'r') as file:
        lines = file.readlines()

    # useful info
    num_vars = 0
    num_restrictions = 0
    restrictions = OrderedDict()
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


# if __name__ == "__main__":
#     # Get the path to the directory containing the current script
#     read_problem_example_file(file_name='problem_example_1')
#     current_dir = os.path.dirname(os.path.abspath(__file__))
