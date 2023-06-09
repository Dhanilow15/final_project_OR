from mip import *

from final_project_OR.branch_and_bound.preprocessing.modeling import OptmModel


class BranchAndBound():
    def __init__(self, initial_model: Model, initial_vars: mip.Var):
        # saving initial problem info, without screen printing
        self.initial_model = initial_model
        self.initial_model.verbose = False
        self.initial_vars = initial_vars
        self.initial_solution = self.initial_model.optimize()



if __name__ == '__main__':
    my_model = OptmModel(file_name='problem_example_1')
    my_bb = BranchAndBound(initial_model=my_model.model_problem(), initial_vars=my_model.vars)
    print('-----------------')
    print(my_bb.initial_solution)
    print(my_bb.initial_model.objective_value)
    print(my_bb.initial_vars)