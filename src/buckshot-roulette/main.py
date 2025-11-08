import sys
from .help import help

args = sys.argv

# Handle Game call and Instruction menu

if __name__ == "main":
    for arg in args:
        match arg:
            case "--verbose":
                print("Show game detail")
            case _:
                raise ValueError(f"Invalid arguments: {help()}")
