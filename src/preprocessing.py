"""
preprocessing.py

A collection of data preprocessing utility functions for cleaning, transforming,
and manipulating data. This module supports operations commonly required in
data preparation workflows, including:

• Data cleaning:
    - Removing missing values
    - Filling missing values
    - Removing duplicate values

• Numeric preprocessing:
    - Min-max normalization
    - Z-score standardization
    - Value clipping
    - Integer conversion
    - Logarithmic transformation

• Text preprocessing:
    - Tokenization (lowercase alphanumeric extraction)
    - Removing punctuation while keeping spaces
    - Removing stop-words

• Structural transformations:
    - Flattening a list of lists
    - Shuffling values with optional reproducibility

The functions are designed to be reusable and independent, making the module
suitable for use in data pipelines, command-line interfaces, or integration
with machine learning preprocessing steps.

Each function includes detailed docstrings describing the purpose, parameters,
return values, and examples.

Author: <your name>
Date: <your date>
"""

import math
import random
import re
import numpy as np


# 1. Removal of missing values
def remove_missing(values):
    """
    Remove missing values from a list.

    Missing values include: None, empty strings (""), and NaN values.

    Parameters
    ----------
    values : list
        List containing values that may include None, "", or NaN.

    Returns
    -------
    list
        A new list without missing values.

    Example
    -------
    >>> remove_missing([1, None, "", float("nan"), 3])
    [1, 3]
    """
    cleaned = []
    for v in values:
        if v is None:
            continue
        if v in ("", "None", "none", "null", "NaN", "nan"):
            continue
        if isinstance(v, float) and math.isnan(v):
            continue
        if v == "":
            continue
        cleaned.append(v)
    return cleaned


# 2. Filling missing values
def fill_missing(values, fill_value=0):
    """
    Replace missing values with a given filling value.

    Missing values include: None, empty strings (""), and NaN values.

    Parameters
    ----------
    values : list
        List of values that may include missing ones.
    fill_value : any, optional
        Value used to replace missing entries (default = 0).

    Returns
    -------
    list
        New list with missing values replaced.

    Example
    -------
    >>> fill_missing([1, None, "", 3], fill_value=-1)
    [1, -1, -1, 3]
    """
    filled = []
    for v in values:
        if (
            v is None
            or v == ""
            or (isinstance(v, float) and math.isnan(v))
            or v in ("", "None", "none", "null", "NaN", "nan")
        ):
            filled.append(fill_value)
        else:
            filled.append(v)
    return filled


# 3. Removal of duplicated values
def remove_duplicates(values):
    """
    Remove duplicate values, preserving original order.

    Parameters
    ----------
    values : list

    Returns
    -------
    list
        New list with duplicates removed.

    Example
    -------
    >>> remove_duplicates([1, 2, 2, 3, 1])
    [1, 2, 3]
    """
    seen = set()
    result = []
    for v in values:
        if v not in seen:
            seen.add(v)
            result.append(v)
    return result


# 4. Min-max normalization
def normalize_min_max(values, new_min=0.0, new_max=1.0):
    """
    Normalize numeric values to a new range using min-max scaling.

    Formula: X_norm = (X - X_min) / (X_max - X_min)

    Parameters
    ----------
    values : list of numbers
    new_min : float, optional
    new_max : float, optional

    Returns
    -------
    list of float
        Values normalized to the new range.

    Example
    -------
    >>> normalize_min_max([10, 20, 30], new_min=0, new_max=1)
    [0.0, 0.5, 1.0]
    """
    values = np.array(values, dtype=float)
    min_val = values.min()
    max_val = values.max()

    if min_val == max_val:
        return [new_min] * len(values)

    normalized = (values - min_val) / (max_val - min_val)
    return [float(x) for x in (normalized * (new_max - new_min) + new_min)]


# 5. Standardization
def standardize_z_score(values):
    """
    Standardize values using the z-score method.

    Formula: Z = (X - mean) / std

    Parameters
    ----------
    values : list of numbers

    Returns
    -------
    list of float
        Standardized values.

    Example
    -------
    >>> standardize_z_score([10, 20, 30])
    [-1.2247..., 0.0, 1.2247...]
    """
    values = np.array(values, dtype=float)
    mean = values.mean()
    std = values.std()

    if std == 0:
        return [0.0] * len(values)

    return list((values - mean) / std)


# 6. Clipping values
def clip_values(values, min_val, max_val):
    """
    Clip values to remain within [min_val, max_val].

    Parameters
    ----------
    values : list of numbers
    min_val : number
    max_val : number

    Returns
    -------
    list
        Values clipped to range.

    Example
    -------
    >>> clip_values([1, 5, 10], min_val=2, max_val=8)
    [2, 5, 8]
    """
    return [max(min(v, max_val), min_val) for v in values]


# 7. Convert to integers
def convert_to_int(values):
    """
    Convert values to integers when possible.

    Non-numeric values are ignored.

    Parameters
    ----------
    values : list

    Returns
    -------
    list of int

    Example
    -------
    >>> convert_to_int(["10", "20", "hello"])
    [10, 20]
    """
    result = []
    for v in values:
        try:
            result.append(int(v))
        except (ValueError, TypeError):
            continue
    return result


# 8. Logarithmic scale transformation
def log_transform(values):
    """
    Apply natural logarithm transformation to positive values.

    Non-positive or non-numeric values are ignored.

    Parameters
    ----------
    values : list of numbers or strings convertible to numbers.

    Returns
    -------
    list of float

    Example
    -------
    >>> log_transform([1, 10, -5, "100"])
    [0.0, 2.302..., 4.605...]
    """
    result = []
    for v in values:
        try:
            v = float(v)
            if v > 0:
                result.append(math.log(v))
        except (ValueError, TypeError):
            continue
    return result


# 9. Tokenization
def tokenize(text):
    """
    Split text into lowercase alphanumeric words.

    Uses regex: keeps only [a-zA-Z0-9]+ sequences.

    Parameters
    ----------
    text : str

    Returns
    -------
    list of str

    Example
    -------
    >>> tokenize("Hello, World! 123")
    ['hello', 'world', '123']
    """
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


# 10. Keep alphanumeric + spaces
def keep_alnum_space(text):
    """
    Remove punctuation and keep only alphanumeric chars and spaces.

    Parameters
    ----------
    text : str

    Returns
    -------
    str

    Example
    -------
    >>> keep_alnum_space("Hello!!! World?")
    'Hello World'
    """
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
    return text


# 11. Stop-word removal
def remove_stop_words(text, stop_words):
    """
    Remove stop-words from text.

    Processing steps:
    - convert to lowercase
    - tokenize into words
    - filter out stop words

    Parameters
    ----------
    text : str
    stop_words : list of str

    Returns
    -------
    str
        Text without stop words.

    Example
    -------
    >>> remove_stop_words("This is a sentence", ["is", "a"])
    'this sentence'
    """
    words = tokenize(text)
    filtered = [w for w in words if w not in stop_words]
    return " ".join(filtered)


# 12. Flatten a list of lists
def flatten(list_of_lists):
    """
    Flatten a list of lists into a single list.

    Parameters
    ----------
    list_of_lists : list of lists

    Returns
    -------
    list

    Example
    -------
    >>> flatten([[1, 2], [3, 4]])
    [1, 2, 3, 4]
    """
    return [item for sublist in list_of_lists for item in sublist]


# 13. Random shuffle
def shuffle(values, seed=None):
    """
    Shuffle list values randomly.

    Parameters
    ----------
    values : list
    seed : int, optional
        Seed ensures reproducibility.

    Returns
    -------
    list

    Example
    -------
    >>> shuffle([1, 2, 3], seed=42)
    [3, 1, 2]
    """
    rng = random.Random(seed)
    values_copy = values[:]
    rng.shuffle(values_copy)
    return values_copy
