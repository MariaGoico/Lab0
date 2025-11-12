"""
cli.py

Command Line Interface (CLI) for interacting with preprocessing functions.

This module uses the `click` library to organize commands into functional groups:
    • clean   → cleaning data (remove missing, fill missing)
    • numeric → numeric preprocessing (normalize, standardize, etc.)
    • text    → text processing (tokenization, stopword removal, etc.)
    • struct  → structure-related operations (flatten, shuffle, unique)

Each command calls a function from preprocessing.py and prints the output so it
can be used from the terminal.

Run `python cli.py --help` for an overview of available commands.
"""

import ast
import click
from .preprocessing import (
    remove_missing,
    fill_missing,
    remove_duplicates,
    normalize_min_max,
    standardize_z_score,
    clip_values,
    convert_to_int,
    log_transform,
    tokenize,
    keep_alnum_space,
    remove_stop_words,
    flatten,
    shuffle,
)


# ─────────────────────────────
# MAIN GROUP
# ─────────────────────────────
@click.group(help="Main CLI group to preprocess data.")
def cli():
    """
    Entry point of the CLI.

    This function does not execute anything by itself. It acts as a parent
    command that organizes other command groups (clean, numeric, text, struct).
    """


# ─────────────────────────────
# CLEAN GROUP
# ─────────────────────────────
@cli.group(help="Operations for cleaning and filtering raw data.")
def clean():
    """Group of commands related to cleaning data (missing values, duplicates)."""


@clean.command(
    name="remove-missing",
    help="Remove missing values (None, empty string, NaN). Example: python cli.py"
    " clean remove-missing 1 '' 3 None",
)
@click.argument("values", nargs=-1)
def clean_remove_missing(values):
    """
    Remove missing values from input.

    Missing values include: None, empty strings, and NaN values.

    Args:
        values (tuple): Values ed from the command line.

    Example:
        python cli.py clean remove-missing 1 '' None 3
    """
    click.echo(remove_missing(list(values)))


@clean.command(
    name="fill-missing",
    help="Fill missing values with a given value. Example: python cli.py "
    "clean fill-missing 1 '' 3 None --value 0",
)
@click.argument("values", nargs=-1)
@click.option(
    "--value", default=0, help="Value to replace missing entries (default=0)."
)
def clean_fill_missing(values, value):
    """
    Replace missing values with a given fill value.

    Args:
        values (tuple): Input values that may contain missing entries.
        value (any): Replacement value (default is 0).

    Example:
        python cli.py clean fill-missing 1 '' None 3 --value -1
    """
    click.echo(fill_missing(list(values), value))


# ─────────────────────────────
# NUMERIC GROUP
# ─────────────────────────────
@cli.group(help="Operations related to numerical preprocessing.")
def numeric():
    """Group of commands related to numerical preprocessing."""


@numeric.command(
    name="normalize",
    help="Normalize values using min-max scaling. Example: python cli.py numeric"
    " normalize 5 10 15 --min 0 --max 1",
)
@click.argument("values", nargs=-1, type=float)
@click.option("--min", "new_min", default=0.0, help="New minimum (default=0)")
@click.option("--max", "new_max", default=1.0, help="New maximum (default=1)")
def numeric_normalize(values, new_min, new_max):
    """
    Normalize numeric input using min-max scaling.

    Args:
        values (tuple): Numeric values from CLI.
        new_min (float): Minimum of new range.
        new_max (float): Maximum of new range.

    Example:
        python cli.py numeric normalize 10 20 30 --min 0 --max 1
    """
    click.echo(normalize_min_max(list(values), new_min, new_max))


@numeric.command(
    name="standardize",
    help="Standardize values (z-score method). Example: python cli.py numeric standardize 5 10 15",
)
@click.argument("values", nargs=-1, type=float)
def numeric_standardize(values):
    """
    Apply z-score standardization (mean=0, std=1).

    Args:
        values (tuple): Numeric values to standardize.

    Example:
        python cli.py numeric standardize 1 2 3 4 5
    """
    click.echo(standardize_z_score(list(values)))


@numeric.command(
    name="clip",
    help="Clip values into a given range. Example: python cli.py numeric "
    "clip 1 5 10 --min 2 --max 8",
)
@click.argument("values", nargs=-1, type=float)
@click.option("--min", "min_val", default=0.0, help="Lower clipping bound")
@click.option("--max", "max_val", default=1.0, help="Upper clipping bound")
def numeric_clip(values, min_val, max_val):
    """
    Clip numeric values to remain within the specified interval.

    Args:
        values (tuple): Numeric values from CLI.
        min_val (float): Minimum allowed value.
        max_val (float): Maximum allowed value.

    Example:
        python cli.py numeric clip 1 5 10 --min 2 --max 8
    """
    click.echo(clip_values(list(values), min_val, max_val))


@numeric.command(
    name="to-int",
    help="Convert values to integers (non convertible values ignored). "
    "Example: python cli.py numeric to-int 5 10 3.6 A",
)
@click.argument("values", nargs=-1)
def numeric_to_int(values):
    """
    Convert values to integers, ignoring invalid inputs.

    Args:
        values (tuple): List of values that may include non-numerical strings.

    Example:
        python cli.py numeric to-int 5 10 3.6 A
    """
    click.echo(convert_to_int(list(values)))


@numeric.command(
    name="log",
    help="Apply logarithmic transformation (positive values only)."
    " Example: python cli.py numeric log 1 10 100",
)
@click.argument("values", nargs=-1)
def numeric_log(values):
    """
    Apply a natural logarithm transformation.

    Only positive numeric inputs are transformed; invalid entries are ignored.

    Args:
        values (tuple): Numeric values or numeric strings.

    Example:
        python cli.py numeric log 1 10 100
    """
    click.echo(log_transform(list(values)))


# ─────────────────────────────
# TEXT GROUP
# ─────────────────────────────
@cli.group(help="Operations to process and analyze text.")
def text():
    """Group of commands for text preprocessing."""


@text.command(name="tokenize", help="Tokenize text into lowercase alphanumeric words.")
@click.argument("input_text")
def text_tokenize(input_text):
    """
    Tokenize text into lowercase alphanumeric words.

    Args:
        input (str): Raw input text.

    Example:
        python cli.py text tokenize "Hello World 123!"
    """
    click.echo(tokenize(input_text))


@text.command(
    name="remove-punctuation",
    help="Remove punctuation (keeps alphanumeric + spaces).",
)
@click.argument("input_text")
def text_remove_punctuation(input_text):
    """
    Remove punctuation from text, preserving only alphanumeric characters and spaces.

    Args:
        input (str): Raw input text.

    Example:
        python cli.py text remove-punctuation "Hello, world!"
    """
    click.echo(keep_alnum_space(input_text))


@text.command(
    name="remove-stopwords",
    help="Remove stop words. Example: python cli.py text "
    "remove-stopwords 'this is a test' --stop 'is,a'",
)
@click.argument("input_text")
@click.option("--stop", help="Comma-separated stop words list")
def text_remove_stopwords(input_text, stop):
    """
    Remove stop-words from a text string.

    Args:
        input (str): Text to process.
        stop (str): Comma-separated list of stop words.

    Example:
        python cli.py text remove-stopwords "This is a test" --stop "is,a"
    """
    stop_words = stop.split(",") if stop else []
    click.echo(remove_stop_words(input_text, stop_words))


# ─────────────────────────────
# STRUCT GROUP
# ─────────────────────────────
@cli.group(help="Operations to manipulate data structures.")
def struct():
    """Group of commands that modify data structure (shuffle, flatten, etc.)."""


@struct.command(
    name="shuffle",
    help="Randomly shuffle values. Example: python cli.py struct shuffle 1 2 3 4 --seed 42",
)
@click.argument("values", nargs=-1)
@click.option("--seed", default=None, type=int, help="Seed to ensure reproducibility")
def struct_shuffle(values, seed):
    """
    Randomly shuffle a list of values.

    Args:
        values (tuple): Values to shuffle.
        seed (int): Optional seed for reproducibility.

    Example:
        python cli.py struct shuffle 1 2 3 4 --seed 42
    """
    parsed_values = [parse_value(v) for v in values]
    click.echo(shuffle(parsed_values, seed))


@struct.command(
    name="flatten",
    help="Flatten a list of lists. Example: python cli.py struct flatten '[1,2]' '[3,4]'",
)
@click.argument("values", nargs=-1)
def struct_flatten(values):
    """
    Flatten nested lists into a single list.

    Uses `eval()` to interpret each input string as a Python list.

    Args:
        values (tuple): String representation of lists.

    Example:
        python cli.py struct flatten "[1,2]" "[3,4]"
    """
    parsed_values = ast.literal_eval(values)
    result = flatten(parsed_values)
    click.echo(result)


def parse_value(v):
    """
    Convert a CLI input string to an integer if possible.

    Parameters
    ----------
    v : str
        The value to parse, typically coming from command-line arguments.

    Returns
    -------
    int or str
        - If `v` can be converted to an integer, returns the integer.
        - Otherwise, returns `v` unchanged as a string.

    Example
    -------
    >>> parse_value("10")
    10
    >>> parse_value("hello")
    'hello'
    """
    try:
        return int(v)
    except ValueError:
        return v  # leave as string if not numeric


@struct.command(
    name="unique",
    help="Get unique values (remove duplicates). Example: python cli.py struct unique 1 2 2 3",
)
@click.argument("values", nargs=-1)
def struct_unique(values):
    """
    Remove duplicate values, preserving order.

    Args:
        values (tuple): Input values from CLI.

    Example:
        python cli.py struct unique 1 2 2 3
    """
    parsed_values = [parse_value(v) for v in values]
    click.echo(remove_duplicates(parsed_values))


if __name__ == "__main__":
    cli()
