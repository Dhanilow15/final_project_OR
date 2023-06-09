from mip import *

from final_project_OR.branch_and_bound.utils.read_problem_example_file import OptmProblem

class Model:
    def __init__(self, optm_problem: OptmProblem):
        # setting problem info object
        self.problem = optm_problem
    
    def model_problem(self, file_name: str) -> Model:
        """
        Models a python mip model from any file stored in this project data folder. The problem will be modeled as a
        MAXIMIZE problem, with 'lesser or equal than' restrictions only.
        Args:
            file_name (str): model file name
        Returns:
            optm_model (Model): python mip model of predefined optimization problem
        """
    
        # modeling.py the problem
        optm_model = Model(sense=MAXIMIZE, solver_name=CBC)
    
        # creating vars dictionary
        x = {i + 1: optm_model.add_var(var_type=CONTINUOUS, name=f"x_{i + 1}")
             for i in range(self.problem.num_vars)}
    
        # creating restrictions
        for coefficients in self.problem.restrictions.values():
            optm_model += xsum(c*x[index+1] for index, c in enumerate(coefficients[:-1])) <= coefficients[-1]
    
        optm_model.write(f"model_{file_name}.lp")  # saves model on archive
        # with open(f"model_{file_name}.lp", "r") as f:  # reads and exhibit model
        #     print(f.read())

        return optm_model
