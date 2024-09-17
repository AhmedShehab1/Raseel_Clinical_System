import models as m
from flask import request, current_app, session, g


def table_search():
    session["previous_endpoint"] = request.endpoint
    if g.search_form.validate():
        page = request.args.get("page", 1, type=int)
        search_results = m.Patient.search(
            g.search_form.q.data,
            page,
            current_app.config.get("SEARCH_RESULTS_PER_PAGE", 10),
        )
        if type(search_results) != list:
            search_results = search_results.all()
        return search_results
    return None
