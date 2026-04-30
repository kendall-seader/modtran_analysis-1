from datetime import datetime
import argparse
from pathlib import Path

from libera_utils.io.smart_open import smart_open
import numpy as np

REFERENCE_DATA_PATH = "reference_data.txt"


def create_message(input_file_path: str | None = None, output_file_path: str | None = None):
    """
    Creates a message based on input file contents and reference data file contents, optionally returning the message to
    an output file instead of printed to the terminal.

    Parameters
    ----------
    input_file_path: str, optional
    output_file_path: str, optional
    """
    name = "foo"
    formatted_name = format_name(name)
    message = f'Hello, {formatted_name}! Current time: {datetime.now()}'

    with smart_open(REFERENCE_DATA_PATH, mode='r') as ref:
        message = f'{message}\n{ref.read()}'

    if input_file_path is not None:
        with smart_open(Path(input_file_path), mode='r') as input_file:
            input_data = np.genfromtxt(input_file, delimiter=',')
            manipulated_data = np.flip(input_data)
            message = f'{message}\nFlipped result from {input_file_path}:\n{manipulated_data}'

    if output_file_path is not None:
        with smart_open(Path(output_file_path), mode="w") as f:
            f.write(f'{message}\nThis message is in a file. Saved at time: {datetime.now()}\n')
    else:
        print(message)


def format_name(name: str) -> str:
    """
    Capitalizes letters of a name depending on length.

    Parameters
    __________
    name: str
        Name to be formatted

    Returns
    -------
    edited_name: str
    """
    edited_name = str()
    if len(name) < 3:
        edited_name = name
    if len(name) == 3:
        edited_name = f'{name[0]}{name[1].upper()}{name[2]}'
    if len(name) > 4:
        edited_name = name.upper()
    return edited_name


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input_file_path', '-i', default=None)
    arg_parser.add_argument('--output_file_path', '-o', default=None)
    args = arg_parser.parse_args()
    create_message(args.input_file_path, args.output_file_path)