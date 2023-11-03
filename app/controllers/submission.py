from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from app.services.submission import SubmissionService
from app.utils.scraping import JournalScraper


class Submission:
    def __init__(self, request):
        self.request = request
        self.submission_service = SubmissionService(request)

    @view_config(route_name="home", renderer="templates/index.jinja2")
    def submissions(self):
        pageShow = int(self.request.params.get("page-show", 15))
        page = int(self.request.params.get("page", 1))
        search = self.request.params.get("search", None)
        duplicate = self.request.params.get("duplicate", False)
        sync = self.request.params.get("sync", False)

        journal_lists = [
            {
                "url": "https://ijeecs.iaescore.com/index.php/IJEECS",
                "journal_name": "Indonesian Journal of Electrical Engineering and Computer Science",
            },
        ]

        submissions = []

        scraper = JournalScraper(journal_lists)

        if sync:
            scraper_data = scraper.run()

            for submission in scraper_data:
                self.submission_service.create_or_update_submission(submission)

            submissions = self.submission_service.get_all_submission(
                page, pageShow, search, duplicate
            )

        else:
            submissions = self.submission_service.get_all_submission(
                page, pageShow, search, duplicate
            )

        context = {"content": submissions}

        return render_to_response(
            "templates/index.jinja2", context, request=self.request
        )
