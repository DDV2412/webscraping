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
        self.submission_service.delete_all_submissions()
        submissions = []

        journal_lists = [
            {
                "url": "https://iaesprime.com/index.php/csit",
                "journal_name": "Computer Science and Information Technologies",
                "payload": {"username": "cmedia", "password": "254#@#@778&%"},
            },
            {
                "url": "https://ijece.iaescore.com/index.php/IJECE",
                "journal_name": "International Journal of Electrical and Computer Engineering (IJECE)",
                "payload": {"username": "ijecemedia", "password": "254#@#@778&%"},
            },
            {
                "url": "https://ijeecs.iaescore.com/index.php/IJEECS",
                "journal_name": "Indonesian Journal of Electrical Engineering and Computer Science",
                "payload": {"username": "ijecemedia", "password": "254#@#@778&%$"},
            },
            {
                "url": "https://ijaas.iaescore.com/index.php/IJAAS",
                "journal_name": "International Journal of Advances in Applied Sciences",
                "payload": {"username": "imedia", "password": "254#@#@778&%"},
            },
            {
                "url": "https://ijict.iaescore.com/index.php/IJICT",
                "journal_name": "International Journal of Informatics and Communication Technology (IJ-ICT)",
                "payload": {"username": "imedia", "password": "254#@#@778&%"},
            },
            {
                "url": "https://ijres.iaescore.com/index.php/IJRES",
                "journal_name": "International Journal of Reconfigurable and Embedded Systems (IJRES)",
                "payload": {"username": "imedia", "password": "254#@#@778&%"},
            },
            {
                "url": "https://ijra.iaescore.com/index.php/IJRA",
                "journal_name": "IAES International Journal of Robotics and Automation (IJRA)",
                "payload": {"username": "imedia", "password": "254#@#@778&%"},
            },
            {
                "url": "https://www.beei.org/index.php/EEI",
                "journal_name": "Bulletin of Electrical Engineering and Informatics",
                "payload": {"username": "ijecemedia", "password": "254#@#@778&%$"},
            },
            {
                "url": "https://ijai.iaescore.com/index.php/IJAI",
                "journal_name": "IAES International Journal of Artificial Intelligence (IJ-AI)",
                "payload": {"username": "ddv", "password": "254#@#@778&%"},
            },
            {
                "url": "https://ijpeds.iaescore.com/index.php/IJPEDS",
                "journal_name": "International Journal of Power Electronics and Drive Systems (IJPEDS)",
                "payload": {"username": "ddv", "password": "254#@#@778&%"},
            },
            {
                "url": "https://ijape.iaescore.com/index.php/IJAPE",
                "journal_name": "International Journal of Applied Power Engineering (IJAPE)",
                "payload": {"username": "ijecemedia", "password": "254#@#@778&%$"},
            },
            {
                "url": "https://ijere.iaescore.com/index.php/IJERE",
                "journal_name": "International Journal of Evaluation and Research in Education (IJERE)",
                "payload": {"username": "imedia", "password": "254#@#@778&%"},
            },
            {
                "url": "https://edulearn.intelektual.org/index.php/EduLearn",
                "journal_name": "Journal of Education and Learning (EduLearn)",
                "payload": {"username": "emedia", "password": "254#@#@778&%$"},
            },
            {
                "url": "http://telkomnika.uad.ac.id/index.php/TELKOMNIKA",
                "journal_name": "TELKOMNIKA (Telecommunication Computing Electronics and Control)",
                "payload": {"username": "ijecemedia", "password": "254#@#@778&%$"},
            },
        ]

        for journal in journal_lists:
            scraper = JournalScraper(journal)
            scraper_data = scraper.run()

            for submission in scraper_data:
                self.submission_service.create_or_update_submission(submission)
            print(f"Success {journal['journal_name']}")
        return Response(json_body={"status": "success"}, status_code=200)
