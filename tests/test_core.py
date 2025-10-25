"""Tests for humorbench core functionality."""

from humorbench.core import HumorBench, calculate_humor_score


class TestHumorBench:
    """Test cases for HumorBench class."""

    def test_init(self) -> None:
        """Test HumorBench initialization."""
        bench = HumorBench("test")
        assert bench.name == "test"
        assert bench.jokes == []

    def test_add_joke(self) -> None:
        """Test adding jokes."""
        bench = HumorBench("test")
        joke = "Why did the chicken cross the road?"
        bench.add_joke(joke)
        assert joke in bench.jokes
        assert bench.get_joke_count() == 1

    def test_get_joke_count_empty(self) -> None:
        """Test getting joke count when empty."""
        bench = HumorBench("test")
        assert bench.get_joke_count() == 0

    def test_get_joke_count_multiple(self) -> None:
        """Test getting joke count with multiple jokes."""
        bench = HumorBench("test")
        bench.add_joke("Joke 1")
        bench.add_joke("Joke 2")
        bench.add_joke("Joke 3")
        assert bench.get_joke_count() == 3

    def test_get_random_joke_empty(self) -> None:
        """Test getting random joke when no jokes exist."""
        bench = HumorBench("test")
        assert bench.get_random_joke() is None

    def test_get_random_joke_single(self) -> None:
        """Test getting random joke with one joke."""
        bench = HumorBench("test")
        joke = "Why did the chicken cross the road?"
        bench.add_joke(joke)
        assert bench.get_random_joke() == joke

    def test_get_random_joke_multiple(self) -> None:
        """Test getting random joke with multiple jokes."""
        bench = HumorBench("test")
        jokes = ["Joke 1", "Joke 2", "Joke 3"]
        for joke in jokes:
            bench.add_joke(joke)

        random_joke = bench.get_random_joke()
        assert random_joke in jokes

    def test_clear_jokes(self) -> None:
        """Test clearing jokes."""
        bench = HumorBench("test")
        bench.add_joke("Joke 1")
        bench.add_joke("Joke 2")
        assert bench.get_joke_count() == 2

        bench.clear_jokes()
        assert bench.get_joke_count() == 0
        assert bench.jokes == []


class TestCalculateHumorScore:
    """Test cases for calculate_humor_score function."""

    def test_empty_joke(self) -> None:
        """Test scoring empty joke."""
        assert calculate_humor_score("") == 0.0

    def test_short_joke(self) -> None:
        """Test scoring short joke."""
        score = calculate_humor_score("Hi")
        assert 0.0 <= score <= 1.0

    def test_medium_joke(self) -> None:
        """Test scoring medium-length joke."""
        joke = "Why did the chicken cross the road? To get to the other side!"
        score = calculate_humor_score(joke)
        assert 0.0 <= score <= 1.0

    def test_long_joke(self) -> None:
        """Test scoring long joke."""
        joke = "This is a very long joke with many words that should test the scoring algorithm properly and give us a good score because it has enough content to be considered humorous."
        score = calculate_humor_score(joke)
        assert 0.0 <= score <= 1.0

    def test_joke_with_question_mark(self) -> None:
        """Test scoring joke with question mark."""
        joke_with_q = "Why did the chicken cross the road?"
        joke_without_q = "The chicken crossed the road"

        score_with_q = calculate_humor_score(joke_with_q)
        score_without_q = calculate_humor_score(joke_without_q)

        assert score_with_q > score_without_q

    def test_joke_with_exclamation(self) -> None:
        """Test scoring joke with exclamation mark."""
        joke_with_excl = "That's hilarious!"
        joke_without_excl = "That's hilarious"

        score_with_excl = calculate_humor_score(joke_with_excl)
        score_without_excl = calculate_humor_score(joke_without_excl)

        assert score_with_excl > score_without_excl

    def test_joke_with_both_marks(self) -> None:
        """Test scoring joke with both question and exclamation marks."""
        joke = "Why did the chicken cross the road? To get to the other side!"
        score = calculate_humor_score(joke)
        assert score > 0.15  # Should get bonus for both marks
