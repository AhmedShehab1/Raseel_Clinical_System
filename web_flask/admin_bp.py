from flask import Blueprint, render_template, request, session, g, current_app
from flask_login import login_required
from datetime import datetime, timezone
from models import StaffMember

bp = Blueprint('admin_bp', __name__, url_prefix='/admin')



def get_search_results(results):
    session['previous_endpoint'] = request.endpoint
    if g.search_form.validate():
        page = request.args.get("page", 1, type=int)
        search_results = StaffMember.search(g.search_form.q.data, page,
                                             current_app.config.get('SEARCH_RESULTS_PER_PAGE', 20))
        results.extend(search_results)


@bp.route('/dashboard')
@login_required
def admin_dashboard():
    results = []
    get_search_results(results)
    current_time_utc = datetime.now(timezone.utc)
    return render_template(
                           'admin_base.html',
                           title='Admin Dashboard',
                           current_time_utc=current_time_utc,
                           results=results
                                )
