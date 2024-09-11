import models as m
from flask import request, current_app, session, g

def search_patients():
    session['previous_endpoint'] = request.endpoint
    if g.search_form.validate():
        page = request.args.get("page", 1, type=int)
        print(g.search_form.q.data, page, current_app.config.get('SEARCH_RESULTS_PER_PAGE', 10))
        search_results = m.Patient.search(g.search_form.q.data, page,
                                                current_app.config.get('SEARCH_RESULTS_PER_PAGE', 10))
        return search_results
    return None
