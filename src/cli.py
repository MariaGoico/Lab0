import click
from preprocessing import (
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
    shuffle
)

# MAIN GROUP
@click.group(help="Main CLI group to preprocess data.")
def cli():
    pass

# CLEAN GROUP
@cli.group(help="Operations for cleaning and filtering raw data.")
def clean():
    pass


@clean.command(name="remove-missing", help="Remove missing values (None, empty string, NaN). Example: python cli.py clean remove-missing 1 '' 3 None")
@click.argument("values", nargs=-1)
def clean_remove_missing(values):
    click.echo(remove_missing(list(values)))


@clean.command(name="fill-missing", help="Fill missing values with a given value. Example: python cli.py clean fill-missing 1 '' 3 None --value 0")
@click.argument("values", nargs=-1)
@click.option("--value", default=0, help="Value to replace missing entries (default=0).")
def clean_fill_missing(values, value):
    click.echo(fill_missing(list(values), value))


# NUMERIC GROUP
@cli.group(help="Operations related to numerical preprocessing.")
def numeric():
    pass


@numeric.command(name="normalize", help="Normalize values using min-max scaling. Example: python cli.py numeric normalize 5 10 15 --min 0 --max 1")
@click.argument("values", nargs=-1, type=float)
@click.option("--min", "new_min", default=0.0, help="New minimum (default=0)")
@click.option("--max", "new_max", default=1.0, help="New maximum (default=1)")
def numeric_normalize(values, new_min, new_max):
    click.echo(normalize_min_max(list(values), new_min, new_max))


@numeric.command(name="standardize", help="Standardize values (z-score method). Example: python cli.py numeric standardize 5 10 15")
@click.argument("values", nargs=-1, type=float)
def numeric_standardize(values):
    click.echo(standardize_z_score(list(values)))


@numeric.command(name="clip", help="Clip values into a given range. Example: python cli.py numeric clip 1 5 10 --min 2 --max 8")
@click.argument("values", nargs=-1, type=float)
@click.option("--min", "min_val", default=0.0, help="Lower clipping bound")
@click.option("--max", "max_val", default=1.0, help="Upper clipping bound")
def numeric_clip(values, min_val, max_val):
    click.echo(clip_values(list(values), min_val, max_val))


@numeric.command(name="to-int", help="Convert values to integers (non convertible values ignored). Example: python cli.py numeric to-int 5 10 3.6 A")
@click.argument("values", nargs=-1)
def numeric_to_int(values):
    click.echo(convert_to_int(list(values)))


@numeric.command(name="log", help="Apply logarithmic transformation (positive values only). Example: python cli.py numeric log 1 10 100")
@click.argument("values", nargs=-1)
def numeric_log(values):
    click.echo(log_transform(list(values)))



# TEXT GROUP
@cli.group(help="Operations to process and analyze text.")
def text():
    pass


@text.command(name="tokenize", help="Tokenize text into lowercase alphanumeric words.")
@click.argument("input")
def text_tokenize(input):
    click.echo(tokenize(input))


@text.command(name="remove-punctuation", help="Remove punctuation (keeps alphanumeric + spaces).")
@click.argument("input")
def text_remove_punctuation(input):
    click.echo(keep_alnum_space(input))


@text.command(name="remove-stopwords", help="Remove stop words. Example: python cli.py text remove-stopwords 'this is a test' --stop 'is,a'")
@click.argument("input")
@click.option("--stop", help="Comma-separated stop words list")
def text_remove_stopwords(input, stop):
    stop_words = stop.split(",") if stop else []
    click.echo(remove_stop_words(input, stop_words))



# STRUCT GROUP
@cli.group(help="Operations to manipulate data structures.")
def struct():
    pass


@struct.command(name="shuffle", help="Randomly shuffle values. Example: python cli.py struct shuffle 1 2 3 4 --seed 42")
@click.argument("values", nargs=-1)
@click.option("--seed", default=None, type=int, help="Seed to ensure reproducibility")
def struct_shuffle(values, seed):
    click.echo(shuffle(list(values), seed))


@struct.command(name="flatten", help="Flatten a list of lists. Example: python cli.py struct flatten '[1,2]' '[3,4]'")
@click.argument("values", nargs=-1)
def struct_flatten(values):
    parsed = [eval(v) for v in values]  # Eval used for simplifying input parsing
    click.echo(flatten(parsed))


@struct.command(name="unique", help="Get unique values (remove duplicates). Example: python cli.py struct unique 1 2 2 3")
@click.argument("values", nargs=-1)
def struct_unique(values):
    click.echo(remove_duplicates(list(values)))


if __name__ == "__main__":
    cli()