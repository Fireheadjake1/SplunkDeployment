"""Main entrypoint"""

# Standard libraries
from argparse import ArgumentParser

# Project libraries
from python_template.constants import VERSION


def main():
    """Main function"""
    parser = ArgumentParser()
    parser.add_argument("--version", action="version", version=f"v{VERSION}")
    parser.parse_args()


if __name__ == "__main__":
    main()
