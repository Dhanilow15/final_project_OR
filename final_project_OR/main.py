from final_project_OR.branch_and_bound.branch_and_bound import BranchAndBound
from final_project_OR.branch_and_bound.preprocessing.modeling import OptmModel


def solve_problem(file_name: str):
    """
    Solves problems in data folder with branch and bound and prints a message with Optimal solution value.
    Args:
        file_name (str): problem file name
    """
    solve_model = OptmModel(file_name=file_name)
    solve_bb = BranchAndBound(initial_model=solve_model.model_problem(),
                              initial_vars=solve_model.vars,
                              num_initial_restrictions=solve_model.problem.num_restrictions)
    solve_bb.execute_branch_and_bound(start_model=solve_bb.initial_model, n_restrs=solve_model.problem.num_restrictions)

    print(f'Optimal integer solution for {file_name} is {solve_bb.primal_limit}')


if __name__ == '__main__':
    for i in range(1, 5):
        solve_problem(file_name=f'problem_example_{i}')
