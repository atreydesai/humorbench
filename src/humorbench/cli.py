"""Command-line interface for humorbench."""

import argparse

from humorbench.core import HumorBench, calculate_humor_score


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="HumorBench - A humor benchmarking tool"
    )
    parser.add_argument(
        "--name", default="default", help="Name for the benchmark instance"
    )
    parser.add_argument("--joke", help="Add a joke to the benchmark")
    parser.add_argument("--score", help="Calculate humor score for a joke")
    parser.add_argument("--random", action="store_true", help="Get a random joke")
    parser.add_argument("--count", action="store_true", help="Show joke count")

    args = parser.parse_args()

    bench = HumorBench(args.name)

    if args.joke:
        bench.add_joke(args.joke)
        print(f"Added joke: {args.joke}")

    if args.score:
        score = calculate_humor_score(args.score)
        print(f"Humor score: {score:.2f}")

    if args.random:
        joke = bench.get_random_joke()
        if joke:
            print(f"Random joke: {joke}")
        else:
            print("No jokes available")

    if args.count:
        print(f"Joke count: {bench.get_joke_count()}")


if __name__ == "__main__":
    main()
