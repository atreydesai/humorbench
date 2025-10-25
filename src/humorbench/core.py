"""Core functionality for humorbench."""


class HumorBench:
    """Main class for humor benchmarking functionality."""

    def __init__(self, name: str) -> None:
        """Initialize HumorBench instance.

        Args:
            name: The name of the humor benchmark instance.
        """
        self.name = name
        self.jokes: list[str] = []

    def add_joke(self, joke: str) -> None:
        """Add a joke to the benchmark.

        Args:
            joke: The joke text to add.
        """
        self.jokes.append(joke)

    def get_joke_count(self) -> int:
        """Get the total number of jokes.

        Returns:
            The number of jokes in the benchmark.
        """
        return len(self.jokes)

    def get_random_joke(self) -> str | None:
        """Get a random joke from the collection.

        Returns:
            A random joke or None if no jokes are available.
        """
        if not self.jokes:
            return None
        import random

        return random.choice(self.jokes)

    def clear_jokes(self) -> None:
        """Clear all jokes from the benchmark."""
        self.jokes.clear()


def calculate_humor_score(joke: str) -> float:
    """Calculate a humor score for a given joke.

    Args:
        joke: The joke text to score.

    Returns:
        A humor score between 0.0 and 1.0.
    """
    # Simple scoring based on length and word count
    words = joke.split()
    word_count = len(words)

    if word_count == 0:
        return 0.0

    # Basic scoring algorithm (can be improved)
    base_score = min(word_count / 20.0, 1.0)

    # Bonus for question marks (setup-punchline structure)
    if "?" in joke:
        base_score += 0.1

    # Bonus for exclamation marks (enthusiasm)
    if "!" in joke:
        base_score += 0.05

    return min(base_score, 1.0)
