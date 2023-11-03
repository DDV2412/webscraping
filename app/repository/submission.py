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
        search_criteria["$or"] = [
            {"title": {"$regex": f"^{search}$", "$options": "i"}} if search else None,
            {"submission_id": search} if search else None,
        ]

        if not any(search_criteria["$or"]):
            del search_criteria["$or"]

        query = {}

        if search_criteria:
            query.update(search_criteria)

        pipeline_journal = [
            {"$group": {"_id": "$journal_name", "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}},
        ]

        aggr_journal = list(self.collection.aggregate(pipeline_journal))

        submissions = list(self.collection.find(query).skip(offset).limit(pageShow))
        for submission in submissions:
            submission["_id"] = str(submission["_id"])

        total_submissions = self.collection.count_documents(query)

        total_pages = (total_submissions + pageShow - 1) // pageShow

        if duplicate:
            duplicate_titles = self.collection.aggregate(
                [
                    {"$match": query},
                    {"$group": {"_id": {"$toLower": "$title"}, "count": {"$sum": 1}}},
                    {"$match": {"count": {"$gt": 1}}},
                ]
            )
            duplicate_titles = [doc["_id"] for doc in duplicate_titles]

            query["title"] = {"$in": [title for title in duplicate_titles]}
            submissions = list(self.collection.find(query).skip(offset).limit(pageShow))
            for submission in submissions:
                submission["_id"] = str(submission["_id"])

            total_submissions = len(submissions)
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
