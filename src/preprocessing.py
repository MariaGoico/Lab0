import math
import random
import numpy as np
import re

# 1. Removal of missing values
def remove_missing(values):
    """Remove missing values: None, '', nan."""
    cleaned = []
    for v in values:
        if v is None:
            continue
        if isinstance(v, float) and math.isnan(v):
            continue
        if v == "":
            continue
        cleaned.append(v)
    return cleaned


# 2. Filling missing values
def fill_missing(values, fill_value=0):
    """Replace missing values with a given value."""
    filled = []
    for v in values:
        if v is None or v == "" or (isinstance(v, float) and math.isnan(v)):
            filled.append(fill_value)
        else:
            filled.append(v)
    return filled


# 3. Removal of duplicated values
def remove_duplicates(values):
    """Return unique values (order preserved)."""
    seen = set()
    result = []
    for v in values:
        if v not in seen:
            seen.add(v)
            result.append(v)
    return result


# 4. Min-max normalization
def normalize_min_max(values, new_min=0.0, new_max=1.0):
    """Normalize numerical values using min-max scaling."""
    values = np.array(values, dtype=float)
    min_val = values.min()
    max_val = values.max()

    if min_val == max_val:
        return [new_min] * len(values)

    normalized = (values - min_val) / (max_val - min_val)
    return list(normalized * (new_max - new_min) + new_min)


# 5. Standardization (z-score)
def standardize_z_score(values):
    """Standardize numerical values using z-score."""
    values = np.array(values, dtype=float)
    mean = values.mean()
    std = values.std()

    if std == 0:
        return [0.0] * len(values)

    return list((values - mean) / std)


# 6. Clipping values
def clip_values(values, min_val, max_val):
    """Clip values to a specified range."""
    return [max(min(v, max_val), min_val) for v in values]


# 7. Convert values to integers
def convert_to_int(values):
    """Convert a list of strings to integers (ignore invalid)."""
    result = []
    for v in values:
        try:
            result.append(int(v))
        except (ValueError, TypeError):
            continue
    return result


# 8. Logarithmic scale transformation
def log_transform(values):
    """Convert positive numerical values to logarithmic scale."""
    result = []
    for v in values:
        try:
            v = float(v)
            if v > 0:
                result.append(math.log(v))
        except:
            continue
    return result


# 9. Tokenization (alphanumeric + lowercase) -----------------------------------------------------------
def tokenize(text):
    """Tokenize text into lowercase alphanumeric words."""
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


# 10. Select alphanumeric + spaces
def keep_alnum_space(text):
    """Keep only alphanumeric characters and spaces."""
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
    return text


# 11. Stop-word removal
def remove_stop_words(text, stop_words):
    """Remove stop words from lowercased text."""
    words = tokenize(text)  # tokenize already lowercases
    filtered = [w for w in words if w not in stop_words]
    return " ".join(filtered)


# 12. Flatten list of lists
def flatten(list_of_lists):
    """Flatten a list of lists."""
    return [item for sublist in list_of_lists for item in sublist]


# 13. Random shuffle (with seed)
def shuffle(values, seed=None):
    """Shuffle values randomly. Seed ensures reproducibility."""
    random.seed(seed)
    values_copy = values[:]
    random.shuffle(values_copy)
    return values_copy