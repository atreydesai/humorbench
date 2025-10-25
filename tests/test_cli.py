"""Tests for humorbench CLI functionality."""

from unittest.mock import patch

from humorbench.cli import main


class TestCLI:
    """Test cases for CLI functionality."""

    def test_cli_without_args(self) -> None:
        """Test CLI runs without arguments."""
        with patch("sys.argv", ["humorbench"]):
            # Should not raise any exceptions
            main()

    def test_cli_with_joke(self) -> None:
        """Test CLI with --joke argument."""
        with patch("sys.argv", ["humorbench", "--joke", "Test joke"]):
            with patch("builtins.print") as mock_print:
                main()
                mock_print.assert_called_with("Added joke: Test joke")

    def test_cli_with_score(self) -> None:
        """Test CLI with --score argument."""
        with patch(
            "sys.argv", ["humorbench", "--score", "Why did the chicken cross the road?"]
        ):
            with patch("builtins.print") as mock_print:
                main()
                # Should print a humor score
                mock_print.assert_called()
                call_args = mock_print.call_args[0][0]
                assert "Humor score:" in call_args

    def test_cli_with_random_no_jokes(self) -> None:
        """Test CLI with --random when no jokes exist."""
        with patch("sys.argv", ["humorbench", "--random"]):
            with patch("builtins.print") as mock_print:
                main()
                mock_print.assert_called_with("No jokes available")

    def test_cli_with_count(self) -> None:
        """Test CLI with --count argument."""
        with patch("sys.argv", ["humorbench", "--count"]):
            with patch("builtins.print") as mock_print:
                main()
                mock_print.assert_called_with("Joke count: 0")
