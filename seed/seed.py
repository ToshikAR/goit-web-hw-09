import sys
import os
import json
import logging

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from database.models import Author, Quote
from database.decorators import error_decorator
from database.db import connect

FIALE_A = r"seed/authors.json"
FIALE_Q = r"seed/qoutes.json"


@error_decorator
def seed_author():
    if not os.path.isfile(FIALE_A):
        logging.error(f" {FIALE_A} no such file or directory")
        return
    with open(FIALE_A, encoding="utf-8") as file:
        data = json.load(file)
        for el in data:
            fullname = el.get("fullname")
            if not Author.objects(fullname=fullname).first():
                author = Author(
                    fullname=fullname,
                    born_date=el.get("born_date"),
                    born_location=el.get("born_location"),
                    description=el.get("description"),
                )
                author.save()


@error_decorator
def seed_quote():
    with open(FIALE_Q, encoding="utf-8") as file:
        data = json.load(file)
        for el in data:
            quote = el.get("quote")
            author = el.get("author")
            author_obj = Author.objects(fullname=author).first()
            if not author_obj:
                raise Exception(f"Object Author {author} not found")
            if not Quote.objects(quote=quote).first():
                quote = Quote(
                    author=author_obj,
                    tags=el.get("tags"),
                    quote=quote,
                )
                quote.save()


if __name__ == "__main__":
    seed_author()
    seed_quote()
