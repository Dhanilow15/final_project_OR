from mip import *

from final_project_OR.branch_and_bound.preprocessing.modeling import OptmModel


class BranchAndBound():
    def __init__(self, initial_model: Model, initial_vars: mip.Var):
        # saving initial problem info, without screen printing
        self.initial_model = initial_model
        self.initial_model.verbose = False
        self.vars = initial_vars
        self.initial_solution = self.initial_model.optimize()
        self.primal_limit = 0

    def filter_feasibility(self, solution_satus: OptimizationStatus) -> bool:
        """
        Feasibility filter for branch and bound
        Args:
            solution_satus (OptimizationStatus): optimization status of a model solution
        Returns:
            (bool): True if solution is feasible, otherwise False
        """
        return not solution_satus.INFEASIBLE

    def filter_integrality(self, solution_vars: list[float]) -> bool:
        """
        Integrality filter for branch and bound
        Args:
            solution_vars (list[float]): list with the var values for a model solution
        Returns:
            (bool): True is every variable is a whole number, otherwise False
        """
        return all(var.is_integer() for var in solution_vars)

    def filter_inferior_solution(self, solution_value: float) -> bool:
        """
        Inferior value solution filter for branch and bound
        Args:
            solution_value (float): solution value of a model
        Returns:
            (bool): True if solution is greater than primal limit, otherwise False
        """
        return solution_value > self.primal_limit

    def execute_branch_and_bound(self):
        pass

if __name__ == '__main__':
    my_model = OptmModel(file_name='problem_example_1')
    my_bb = BranchAndBound(initial_model=my_model.model_problem(), initial_vars=my_model.vars)
    print('-----------------')
    print(my_bb.initial_solution)
    print(my_bb.initial_model.objective_value)
    for v in range(len(my_bb.vars)):
        print(my_bb.vars[v+1].x)