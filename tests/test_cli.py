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


def test_cli_to_int(runner):
    """Test CLI command: numeric to-int"""
    result = runner.invoke(cli, ["numeric", "to-int", "10", "hello", "3.5"])
    assert result.exit_code == 0
    assert "[10]" in result.output


# TEXT GROUP
def test_cli_tokenize(runner):
    """Test CLI command: text tokenize"""
    result = runner.invoke(cli, ["text", "tokenize", "Hello world 123!"])
    assert result.exit_code == 0
    assert "['hello', 'world', '123']" in result.output


def test_cli_remove_stopwords(runner):
    """Test CLI command: text remove-stopwords"""
    result = runner.invoke(
        cli, ["text", "remove-stopwords", "This is a test", "--stop", "is,a"]
    )
    assert result.exit_code == 0
    assert "this test" in result.output


# STRUCT GROUP
def test_cli_struct_shuffle(runner):
    """Test CLI command: struct shuffle"""
    result = runner.invoke(cli, ["struct", "shuffle", "1", "2", "3", "--seed", "42"])
    assert result.exit_code == 0
    assert "[2, 1, 3]" in result.output


def test_cli_struct_unique(runner):
    """Test CLI command: struct unique"""
    result = runner.invoke(cli, ["struct", "unique", "1", "2", "2", "3"])
    assert result.exit_code == 0
    assert "[1, 2, 3]" in result.output
