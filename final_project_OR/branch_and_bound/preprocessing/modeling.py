from mip import Model, MAXIMIZE, CBC, xsum, CONTINUOUS

from final_project_OR.branch_and_bound.utils.read_problem_example_file import OptmProblem
from final_project_OR.branch_and_bound.utils.read_problem_example_file import read_problem_example_file


class OptmModel:
    def __init__(self, file_name: str):
        # setting problem info object
        self.file_name = file_name
        self.problem: OptmProblem = read_problem_example_file(file_name=self.file_name)
        self.vars = {}

    def model_problem(self) -> Model:
        """
        Models a python mip model from any file stored in this project data folder. The problem will be modeled as a
        MAXIMIZE problem, with 'lesser or equal than' restrictions only.
        Returns:
            optm_model (Model): python mip model of predefined optimization problem
        """

        # modeling.py the problem
        optm_model = Model(sense=MAXIMIZE, solver_name=CBC)

        # creating vars dictionary, with linear relaxation
        self.vars = {i + 1: optm_model.add_var(var_type=CONTINUOUS, name=f"x_{i + 1}", lb=0, ub=1)
                     for i in range(self.problem.num_vars)}

        # creating target function
        optm_model.objective = xsum(c * self.vars[index + 1] for index, c in enumerate(self.problem.obj_function))

        # creating restrictions
        for coefficients in self.problem.restrictions.values():
            optm_model += xsum(c * self.vars[index + 1] for index, c in enumerate(coefficients[:-1])) <= \
                          coefficients[-1]

        optm_model.write(f"model_{self.file_name}.lp")  # saves model on archive
        # with open(f"model_{self.file_name}.lp", "r") as f:  # reads and exhibit model
        #     print(f.read())

        return optm_model
