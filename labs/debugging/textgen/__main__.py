from .markov import Markov
import click


@click.command()
@click.argument("filenames", nargs=-1)
@click.option("--start", default=None)
@click.option("--max-words", default=30)
def main(filenames, start, max_words):
    if not filenames:
        raise click.UsageError("No files provided")
    markov = Markov()
    for filename in filenames:
        markov.train_on_file(filename)
    print(markov.generate(start, max_words))


if __name__ == "__main__":
    main()
