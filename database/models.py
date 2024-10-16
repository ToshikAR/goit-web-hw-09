from bson import json_util
from mongoengine import ListField, ReferenceField, StringField, Document, CASCADE


class Author(Document):
    fullname = StringField(max_length=120, required=True)
    born_date = StringField(max_length=120)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=50))
    quote = StringField(required=True)
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)

