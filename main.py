import argparse
import importlib
from pathlib import Path


def show_list():
    print("List of problems are the following")

    for problem_path in Path('problem').glob("*"):
        print(problem_path.name)
        problem = importlib.import_module(f"problem.{problem_path.name}")
        print("   ", problem.__doc__.strip())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('problem', help="name of problem to execute", nargs='?')
    parser.add_argument('-l', help="list of problem", action="store_true")

    args = parser.parse_args()

    if args.l:
        show_list()

    elif args.problem is None:
        print("Problem should be given")

    else:
        try:
            problem = importlib.import_module(f"problem.{args.problem}")
            problem.main()
            return
        except ImportError:
            print(f"Problem {args.problem!r} is not found")
            show_list()

    print()
    parser.print_help()


if __name__ == '__main__':
    main()
