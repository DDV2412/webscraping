from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, ListField


class Submission(Document):
    submission_id = StringField(max_length=10, required=True)
    title = StringField(max_length=255, required=True, text=True)
    journal_name = StringField(text=True)
    authors = StringField(text=True)
    date_submitted = StringField(text=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            "submission_id": self.submission_id,
            "title": self.title,
            "journal_name": self.journal_name,
            "authors": self.authors,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
