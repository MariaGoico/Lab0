import pytest
from click.testing import CliRunner
from src.cli import cli


# --------------------------------------------------------
# FIXTURE FOR CliRunner (shared between all CLI tests)
# --------------------------------------------------------
@pytest.fixture
def runner():
    """Fixture that returns a reusable CliRunner instance."""
    return CliRunner()


# --------------------------------------------------------
# INTEGRATION TESTS FOR CLI COMMANDS
# --------------------------------------------------------

# CLEAN GROUP
def test_cli_remove_missing(runner):
    """Test CLI command: clean remove-missing"""
    result = runner.invoke(cli, ["clean", "remove-missing", "1", "", "None", "3"])
    assert result.exit_code == 0
    assert "['1', '3']" in result.output


def test_cli_fill_missing_with_option(runner):
    """Test CLI command: clean fill-missing with --value option"""
    result = runner.invoke(
        cli, ["clean", "fill-missing", "1", "", "None", "--value", "-1"]
    )
    assert result.exit_code == 0
    assert "['1', -1, -1]" in result.output


# NUMERIC GROUP
def test_cli_normalize(runner):
    """Test CLI command: numeric normalize"""
    result = runner.invoke(
        cli, ["numeric", "normalize", "10", "20", "30", "--min", "0", "--max", "1"]
    )
    assert result.exit_code == 0
    assert "[0.0, 0.5, 1.0]" in result.output

def test_cli_standardize(runner):
    """Test CLI command: numeric standardize"""
    result = runner.invoke(
        cli, ["numeric", "standardize", "1", "2", "3", "4", "5"]
    )
    assert result.exit_code == 0
    assert "np.float64(-1.414" in result.output  # First standardized value
    assert "np.float64(-0.707" in result.output   # Second standardized value
    assert "np.float64(0.0" in result.output      # Third standardized value (mean)
    assert "np.float64(0.707" in result.output    # Fourth standardized value
    assert "np.float64(1.414" in result.output    # Fifth standardized value

def test_cli_clip(runner):
    """Test CLI command: numeric clip"""
    result = runner.invoke(
        cli, ["numeric", "clip", "1", "5", "10", "--min", "2", "--max", "8"]
    )
    assert result.exit_code == 0
    assert "[2.0, 5.0, 8.0]" in result.output

def test_cli_to_int(runner):
    """Test CLI command: numeric to-int"""
    result = runner.invoke(cli, ["numeric", "to-int", "10", "hello", "3.5"])
    assert result.exit_code == 0
    assert "[10]" in result.output

def test_cli_log(runner):
    """Test CLI command: numeric log"""
    result = runner.invoke(
        cli, ["numeric", "log", "1", "10", "100"]
    )
    assert result.exit_code == 0
    assert "0.0" in result.output  # ln(1) = 0
    assert "2.302" in result.output  # ln(10) ≈ 2.302585
    assert "4.605" in result.output  # ln(100) ≈ 4.605170


# TEXT GROUP
def test_cli_tokenize(runner):
    """Test CLI command: text tokenize"""
    result = runner.invoke(cli, ["text", "tokenize", "Hello world 123!"])
    assert result.exit_code == 0
    assert "['hello', 'world', '123']" in result.output

def test_cli_remove_punctuation(runner):
    """Test CLI command: text remove-punctuation"""
    result = runner.invoke(
        cli, ["text", "remove-punctuation", "Hello, world!"]
    )
    assert result.exit_code == 0
    assert "Hello world" in result.output

def test_cli_remove_stopwords(runner):
    """Test CLI command: text remove-stopwords"""
    result = runner.invoke(
        cli, ["text", "remove-stopwords", "This is a test", "--stop", "is,a"]
    )
    assert result.exit_code == 0
    assert "this test" in result.output


# STRUCT GROUP
def test_cli_struct_shuffle_nums(runner):
    """Test CLI command: struct shuffle"""
    result = runner.invoke(cli, ["struct", "shuffle", "1", "2", "3", "--seed", "42"])
    assert result.exit_code == 0
    assert "[2, 1, 3]" in result.output

def test_cli_flatten(runner):
    """Test CLI command: struct flatten"""
    result = runner.invoke(
        cli, ["struct", "flatten", "[1,2]", "[3,4]"]
    )
    assert result.exit_code == 0
    assert "[1, 2, 3, 4]" in result.output

@pytest.mark.parametrize(
    "input_values, expected_output",
    [
        (["1", "2", "2", "3"], "[1, 2, 3]"),
        (["a", "b", "a", "c"], "['a', 'b', 'c']"),
        (["1", "1", "1"], "[1]"),
        (["5", "4", "3", "2", "1"], "[5, 4, 3, 2, 1]"),  # No duplicates
        (["hello", "world", "hello"], "['hello', 'world']"),
        (["1", "a", "1", "a"], "[1, 'a']"),  # Mixed int and string
    ],
)
def test_cli_struct_unique(runner, input_values, expected_output):
    """Test CLI command: struct unique"""
    result = runner.invoke(cli, ["struct", "unique"] + input_values)
    assert result.exit_code == 0
    assert expected_output in result.output
