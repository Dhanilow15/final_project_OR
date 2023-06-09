from mip import *

from final_project_OR.branch_and_bound.preprocessing.modeling import OptmModel


class BranchAndBound():
    def __init__(self, initial_model: Model):
        self.initial_model = initial_model
        self.initial_solution = self.initial_model.optimize()
        self.a = 1

    def daada(self):
        pass


if __name__ == '__main__':
    my_model = OptmModel(file_name='problem_example_1')
    my_bb = BranchAndBound(initial_model=my_model.model_problem())

    my_bb.daada()