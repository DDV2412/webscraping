from app.repository.submission import SubmissionRepo
from pyramid.request import Request


class SubmissionService:
    def __init__(self, request: Request):
        self.submission = SubmissionRepo(request)

    def get_all_submission(self, page, pageShow, search, duplicate):
        return self.submission.find_all_submissions(page, pageShow, search, duplicate)

    def create_or_update_submission(self, submission):
        journal_name = submission.get("journal_name")
        submission_id = submission.get("submission_id")
        existing_submission = self.submission.find_by_submission_id(submission_id)

        if existing_submission:
            if existing_submission["journal_name"] == journal_name:
                return
        else:
            try:
                return self.submission.create_submission(submission)
            except Exception as e:
                return

    def delete_all_submissions(self):
        return self.submission.delete_all_submissions()
