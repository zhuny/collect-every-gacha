import argparse
import importlib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('problem', help="name of problem to execute", nargs='?')
    parser.add_argument('-l', help="list of problem", action="store_true")

    args = parser.parse_args()

    if args.l:
        print("List of problems are the following")

    elif args.problem is None:
        print("Problem should be given")

    else:
        try:
            problem = importlib.import_module(f"problem.{args.problem}")
            problem.main()
            return
        except ImportError:
            print(f"Problem {args.problem!r} is not found")

    print()
    parser.print_help()


if __name__ == '__main__':
    main()
