import re
from pyramid.request import Request


class SubmissionRepo:
    def __init__(self, request: Request):
        self.db = request.registry.db["submission"]
        self.collection = self.db["submission"]

    def create_submission(self, submission):
        result = self.collection.insert_one(submission)
        return str(result.inserted_id)

    def find_by_submission_id(self, submission_id):
        submission = self.collection.find_one({"submission_id": submission_id})
        if submission:
            submission["_id"] = str(submission["_id"])
        return submission

    def find_all_submissions(self, page=1, pageShow=15, search=None, duplicate=False):
        offset = (page - 1) * pageShow

        search_criteria = {}
        if search:
            search_criteria["$or"] = [
                {"title": {"$regex": f".*{search}.*", "$options": "i"}},
                {"submission_id": search},
            ]

        query = {}

        if search_criteria:
            query.update(search_criteria)

        pipeline_journal = [
            {"$group": {"_id": "$journal_name", "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}},
        ]

        aggr_journal = list(self.collection.aggregate(pipeline_journal))

        duplicate_title_values = []

        if duplicate:
            duplicate_titles_pipeline = [
                {"$group": {"_id": {"$toLower": "$title"}, "count": {"$sum": 1}}},
                {"$match": {"count": {"$gt": 1}}},
            ]

            duplicate_titles = list(
                self.collection.aggregate(duplicate_titles_pipeline)
            )

            duplicate_title_values = [item["_id"] for item in duplicate_titles]

            regex_patterns = [
                re.compile(f"^{re.escape(title)}$", re.IGNORECASE)
                for title in duplicate_title_values
            ]

            query = {"title": {"$in": regex_patterns}}

        submissions = list(self.collection.find(query).skip(offset).limit(pageShow))
        for submission in submissions:
            submission["_id"] = str(submission["_id"])

        total_submissions = self.collection.count_documents(query)
        total_pages = (total_submissions + pageShow - 1) // pageShow

        return {
            "submissions": submissions,
            "aggrs": {
                "journal": aggr_journal,
            },
            "total": total_submissions,
            "current_page": page,
            "total_pages": total_pages,
        }
