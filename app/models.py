from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, ListField


class Author(Document):
    name = StringField()
    affiliation = StringField()

    def to_dict(self):
        return {
            "name": self.name,
            "affiliation": self.affiliation,
        }


class Submission(Document):
    submission_id = StringField(max_length=10, required=True)
    title = StringField(max_length=255, required=True, text=True)
    abstract = StringField(text=True)
    journal_name = StringField(text=True)
    authors = ListField(Author)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            "submission_id": self.submission_id,
            "title": self.title,
            "abstract": self.abstract,
            "journal_name": self.journal_name,
            "authors": self.authors,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
