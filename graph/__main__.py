import argparse

arg_parser = argparse.ArgumentParser(
    prog="uv run -m graph", description="A simple argument parser"
)

arg_parser.add_argument(
    "graph",
    choices=["acc", "err-rel", "err-abs", "surv", "scatter"],
    help="The type of graph to plot",
)

args = arg_parser.parse_args()

print(args._get_args())
