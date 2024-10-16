import sys
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from database.models import Author, Quote
from database.decorators import error_decorator
from database.db import cache_redis as cache
from database.db import connect


@cache
@error_decorator
def find_by_author(author: str) -> list[str | None]:
    author = Author.objects(fullname__iregex=author).first()
    if author:
        quotes = Quote.objects(author=author)
        return [[quote.author.fullname, quote.quote] for quote in quotes]
    return []


@cache
@error_decorator
def find_by_authors_sh(author: str) -> list[str | None]:
    authors = Author.objects(fullname__iregex=author)
    result = []
    if authors:
        for author in authors:
            quotes = Quote.objects(author=author)
            result.extend([[quote.author.fullname, quote.quote] for quote in quotes])
        return result


@cache
@error_decorator
def find_by_tag(tag: str) -> list[str | None]:
    quotes = Quote.objects(tags=tag)
    return [[quote.author.fullname, quote.quote] for quote in quotes]


@cache
@error_decorator
def find_by_tag_sh(tag: str) -> list[str | None]:
    quotes = Quote.objects(tags__iregex=tag)
    return [[quote.author.fullname, quote.quote] for quote in quotes]


@cache
@error_decorator
def find_by_tags(tags: list) -> list[str | None]:
    tag_list = tags.split(",")
    quotes = Quote.objects(tags__in=tag_list)
    return [quote.to_json() for quote in quotes]


@cache
@error_decorator
def print_quotes(quotes: list) -> None:
    if quotes:
        for quote in quotes:
            print(f"{quote[0]}: - {quote[1]}")
    else:
        print(None)


@error_decorator
def print_quotes_json(quotes: list) -> None:
    for quote in quotes:
        data = json.loads(quote) if isinstance(quote, str) else quote
        print(f"{data['author']}: - {data['quote']}")


if __name__ == "__main__":
    while True:
        command = input("Enter command (name, name_sh, tag, tag_sh, tags or exit): ")

        # знайти та повернути список всіх цитат автора name: Steve Martin
        if command.lower().startswith("name:"):
            author = command.split(":", 1)[1].strip()
            quotes = find_by_author(author)
            print_quotes(quotes)

        # можливість скороченого запису значень для пошуку як name:st
        elif command.lower().startswith("name_sh:"):
            author = command.split(":", 1)[1].strip()
            quotes = find_by_authors_sh(author)
            print_quotes(quotes)

        # tag:life - знайти та повернути список цитат для тега life
        elif command.lower().startswith("tag:"):
            tag = command.split(":", 1)[1].strip()
            quotes = find_by_tag(tag)
            print_quotes(quotes)

        # можливість скороченого запису значень для пошуку як tag:li
        elif command.lower().startswith("tag_sh:"):
            tag = command.split(":", 1)[1].strip()
            quotes = find_by_tag_sh(tag)
            print_quotes(quotes)

        # tags:life,live — знайти та повернути список цитат
        elif command.startswith("tags:"):
            tags = command.split(":", 1)[1].strip()
            quotes = find_by_tags(tags)
            print_quotes_json(quotes)

        # exit — завершити виконання скрипту
        elif command.lower().startswith("exit"):
            print("Exit")
            break

        else:
            print("Invalid command.")
