def includeme(config):
    config.add_route("home", "/")
    config.add_route("automation", "/automation")
    config.add_static_view("static", "static", cache_max_age=3600)

    config.scan(".controllers")
