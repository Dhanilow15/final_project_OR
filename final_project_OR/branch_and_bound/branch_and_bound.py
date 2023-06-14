import copy

from mip import Model, OptimizationStatus, Var


class BranchAndBound:
    def __init__(self, initial_model: Model, initial_vars: Var, num_initial_restrictions: int):
        # saving initial problem info, without screen printing
        self.initial_model = initial_model
        self.initial_model.verbose = False
        self.vars = initial_vars
        self.initial_solution = self.initial_model.optimize()
        self.num_initial_restrictions = num_initial_restrictions
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

    def execute_branch_and_bound(self, start_model: Model, n_restrs: int):
        # solving
        if start_model != self.initial_model:
            solution = start_model.optimize()
            # checking feasibility
            if self.filter_feasibility(solution_satus=solution):
                return
            # start_model.write("model_{self.file_name}.lp")  # saves model on archive
            # with open("model_{self.file_name}.lp", "r") as f:  # reads and exhibit model
            #      print(f.read())

        # getting solution vars for this iteration
        solution_vars = [self.vars[i + 1].x for i in range(len(self.vars))]
        # checking if all variables are integers
        decimal_vars = self.filter_integrality(solution_vars=solution_vars)

        # checking solution value
        if self.filter_inferior_solution(solution_value=start_model.objective_value) and not decimal_vars:
            return
        # setting new primal limit
        elif not decimal_vars:
            self.primal_limit = start_model.objective_value
            return

        # searching in depth
        for var in decimal_vars:
            # getting the integer border numbers for this variable value
            border_integers = self.get_border_integers_for_float(solution_vars[var-1])
            # branching and bounding
            for index, integer in enumerate(border_integers):
                # setting relevant info
                relaxated_model = copy.copy(start_model)
                restrs_list = list(relaxated_model.constrs)

                # removing exceeding restrs
                if len(restrs_list) > n_restrs and n_restrs == self.num_initial_restrictions:
                    exceeding_restrs = restrs_list[n_restrs:]
                    for restr in exceeding_restrs:
                        relaxated_model.remove(restr)

                # restriction to be lesser than bottom limit
                if index == 1:
                    relaxated_model.add_constr(self.vars[var] >= integer)
                # greater than upper limit
                else:
                    relaxated_model += self.vars[var] <= integer
                # recursive call
                self.execute_branch_and_bound(start_model=relaxated_model, n_restrs=n_restrs+1)
