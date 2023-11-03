from pyramid.config import Configurator
from pymongo import MongoClient


def main(global_config, **settings):
    config = Configurator(settings=settings)
    mongo_uri = settings.get("mongo_uri")
    client = MongoClient(mongo_uri)
    db = client.get_database()
    config.registry.db = db
    config.include("pyramid_jinja2")
    config.include(".routes")
    config.scan()

    return config.make_wsgi_app()
