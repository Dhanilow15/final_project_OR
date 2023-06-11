import copy

from mip import Model, OptimizationStatus, Var


class BranchAndBound:
    def __init__(self, initial_model: Model, initial_vars: Var):
        # saving initial problem info, without screen printing
        self.initial_model = initial_model
        self.initial_model.verbose = False
        self.vars = initial_vars
        self.initial_solution = self.initial_model.optimize()
        self.primal_limit = 0

    @staticmethod
    def get_border_integers_for_float(value: float) -> list[int]:
        """
        Returns a list with border integers for a float number
        Args:
            value (float): float valuee
        Returns:
             (list[int]): list with the first integer number before and after a value.
        """
        return [int(value), int(value) + 1]

    @staticmethod
    def filter_feasibility(solution_satus: OptimizationStatus) -> bool:
        """
        Feasibility filter for branch and bound
        Args:
            solution_satus (OptimizationStatus): optimization status of a model solution
        Returns:
            (bool): True if solution is feasible, otherwise False
        """
        return solution_satus == OptimizationStatus.INFEASIBLE

    @staticmethod
    def filter_integrality(solution_vars: list[float]) -> list:
        """
        Integrality filter for branch and bound
        Args:
            solution_vars (list[float]): list with the var values for a model solution
        Returns:
            (list): Empty list if every variable is a whole number, otherwise returns a list with the deciamal indexes
        """
        return [index + 1 for index, var in enumerate(solution_vars) if not var.is_integer()]

    def filter_inferior_solution(self, solution_value: float) -> bool:
        """
        Inferior value solution filter for branch and bound
        Args:
            solution_value (float): solution value of a model
        Returns:
            (bool): True if solution is lesser than primal limit, otherwise False
        """
        return solution_value < self.primal_limit

    def execute_branch_and_bound(self, start_model: Model):
        if start_model != self.initial_model:
            solution = start_model.optimize()
            # checking feasibility
            if self.filter_feasibility(solution_satus=solution):
                return

        # getting solution vars for this iteration
        solution_vars = [self.vars[i + 1].x for i in range(len(self.vars))]
        # checking if all variables are integers
        decimal_vars = self.filter_integrality(solution_vars=solution_vars)

        # checking solution value
        if self.filter_inferior_solution(solution_value=start_model.objective_value) and not decimal_vars:
            return
        else:
            self.primal_limit = start_model.objective_value

        # searching in depth
        for var in decimal_vars:
            # getting the integer border numbers for this variable value
            border_integers = self.get_border_integers_for_float(solution_vars[var-1])
            # branching and bounding
            for index, integer in enumerate(border_integers):
                relaxated_model = copy.copy(start_model)
                # >= for integer after, and <= for integer before
                relaxated_model += self.vars[var] >= integer if index else self.vars[var] <= integer
                # recursive call
                self.execute_branch_and_bound(start_model=relaxated_model)
