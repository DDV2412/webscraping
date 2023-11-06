from datetime import datetime
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

        submissions = self.submission_service.get_all_submission(
            page, pageShow, search, duplicate
        )

        context = {"content": submissions}

        return render_to_response(
            "templates/index.jinja2", context, request=self.request
        )

    @view_config(route_name="automation", renderer="json")
    def scheduled(self):
        submissions = []

        journal_lists = [
            {
                "url": "https://ijece.iaescore.com/index.php/IJECE",
                "journal_name": "International Journal of Electrical and Computer Engineering (IJECE)",
            },
            {
                "url": "https://ijeecs.iaescore.com/index.php/IJEECS",
                "journal_name": "Indonesian Journal of Electrical Engineering and Computer Science",
            },
            {
                "url": "https://iaesprime.com/index.php/csit",
                "journal_name": "Computer Science and Information Technologies",
            },
        ]

        scraper = JournalScraper(journal_lists)

        scraper_data = scraper.run()

        for submission in scraper_data:
            data = self.submission_service.create_or_update_submission(submission)

            submissions.append(data)

        return Response(
            json_body={"status": "success", "data": submissions}, status_code=200
        )
