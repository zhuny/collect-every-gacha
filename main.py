import argparse
import importlib
import types
from decimal import Decimal
from fractions import Fraction
from pathlib import Path


def show_list():
    print("List of problems are the following")

    for problem_path in Path('problem').glob("*"):
        print(problem_path.name)
        problem = importlib.import_module(f"problem.{problem_path.name}")
        print("   ", problem.__doc__.strip())


def problem_mod_list():
    for problem_path in Path('problem').glob("*"):
        yield problem_path.name, importlib.import_module(
            f"problem.{problem_path.name}.state"
        ).Problem


def get_number(s):
    if s == 'float':
        return float
    elif s == 'fraction':
        return Fraction
    else:
        return Decimal


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', help="list of problem", action="store_true")
    parser.add_argument(
        '--number', default='fraction', type=get_number,
        choices=[float, Fraction, Decimal]
    )

    subparsers = parser.add_subparsers()

    for name, problem in problem_mod_list():
        problem_construct: types.FunctionType = problem.__init__
        annotation = problem_construct.__annotations__
        var_names = problem_construct.__code__.co_varnames

        # var name checking
        if 'self' not in var_names:
            raise ValueError("'self' must be in variable")
        if 'number' not in var_names:
            raise ValueError("'number' is needed to solve problem")

        problem_parser = subparsers.add_parser(name)
        problem_parser.set_defaults(problem=problem)

        for var_name in var_names:
            if var_name == 'self' or var_name == 'number':
                continue

            if var_name not in annotation:
                raise ValueError(f"Define type of '{var_name}'")

            problem_parser.add_argument(
                f'--{var_name}',
                type=annotation[var_name]
            )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.l:
        show_list()

    elif args.problem is None:
        print("Problem should be given")

    else:
        try:
            kwargs = dict(vars(args))
            kwargs.pop('problem')
            kwargs.pop('l')
            args.problem(**kwargs).solve()
            return
        except ImportError:
            print(f"Problem {args.problem!r} is not found")
            show_list()

    print()
    parser.print_help()


if __name__ == '__main__':
    main()
