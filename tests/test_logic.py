import pytest
from src.preprocessing import (
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

# --------------------------------------------------------
# FIXTURE (shared between multiple unit tests)
# --------------------------------------------------------
@pytest.fixture
def sample_values():
    """Fixture that provides a sample list containing missing values."""
    return [None, "", float("nan"), 1, 2, 2, 3]


# --------------------------------------------------------
# UNIT TESTS FOR PREPROCESSING LOGIC
# --------------------------------------------------------

def test_remove_missing(sample_values):
    """Test removal of missing values (None, empty string, NaN)."""
    assert remove_missing(sample_values) == [1, 2, 2, 3]


@pytest.mark.parametrize("input_values, fill_value, expected", [
    ([None, "", float("nan")], 0, [0, 0, 0]),
    ([1, None, 3], -1, [1, -1, 3]),
])
def test_fill_missing(input_values, fill_value, expected):
    """Test replacing missing values using parametrize (with optional argument)."""
    assert fill_missing(input_values, fill_value) == expected


def test_remove_duplicates():
    """Test duplicate removal while preserving list order."""
    assert remove_duplicates([1, 2, 2, 3, 1]) == [1, 2, 3]


@pytest.mark.parametrize("values, new_min, new_max, expected", [
    ([10, 20, 30], 0, 1, [0.0, 0.5, 1.0]),
    ([5, 15], -1, 1, [-1.0, 1.0]),
])
def test_normalize_min_max(values, new_min, new_max, expected):
    """Test min-max normalization (with optional parameters)."""
    assert normalize_min_max(values, new_min, new_max) == expected


def test_standardize_z_score():
    """Test z-score standardization."""
    result = standardize_z_score([10, 20, 30])
    # approx due to floating point rounding
    assert pytest.approx(result, rel=1e-3) == [-1.224744, 0.0, 1.224744]


@pytest.mark.parametrize("values, expected", [
    ([1, 5, 10], [1, 5, 8]),  # Using min=0, max=8
    ([-5, 0, 5], [0, 0, 5]),
])
def test_clip_values(values, expected):
    """Test value clipping (parametrize without optional arguments)."""
    assert clip_values(values, 0, 8) == expected


def test_convert_to_int():
    """Test integer conversion (ignoring invalid values)."""
    assert convert_to_int(["10", "2.9", "hello", 5]) == [10, 5]


def test_log_transform():
    """Test logarithmic transformation (non-positive values ignored)."""
    result = log_transform([1, 10, -5, "100"])
    assert len(result) == 3  # only 3 values > 0
    assert result[0] == 0.0


def test_tokenize():
    """Test tokenizing text into lowercase alphanumeric tokens."""
    assert tokenize("Hello, World! 123") == ["hello", "world", "123"]


def test_keep_alnum_space():
    """Test removal of punctuation while preserving spaces."""
    assert keep_alnum_space("Hi!!! world??") == "Hi world"


def test_remove_stop_words():
    """Test stop words removal."""
    assert remove_stop_words("This is a test", ["is", "a"]) == "this test"


def test_flatten():
    """Test flattening nested lists."""
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


def test_shuffle():
    """Test shuffling with reproducibility using seed."""
    assert shuffle([1, 2, 3], seed=42) == [2, 1, 3]
