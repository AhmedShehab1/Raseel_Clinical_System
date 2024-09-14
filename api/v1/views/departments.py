from web_flask import db
from api.v1.views import bp
from models import Department
from sqlalchemy.orm import joinedload
from flask import flash


class listAllObjects:
    """Class to represent all departments in the database.

    Attributes:
        count: int - the number of departments in the database.
        results: list - a list of dictionaries representing each department

    Methods:
        to_dict() - returns a dictionary representation of the class.
    """

    def __init__(self, departments_list):
        """Initialize the listAllObjects class.

        Args:
            departments_list: list - a list of Department objects.
        """

        self.count = len(departments_list)
        self.results = [department.to_dict() for department in departments_list]

    def to_dict(self):
        """Return a jsn representation of the class."""

        return {"count": self.count, "results": self.results}


def fetch_department(department_id):
    """Fetch a department from the database

    Args:
        department_id: str - the id of the department to fetch.

    Returns:
        Department: the department fetched from the database.
    """

    return db.get_or_404(Department, department_id)


def save():
    """Save changes to the database."""

    db.session.commit()


def update_item(item, data):
    """Update an item with the data provided in the request.

    Args:
        item: BaseModel - the item to update.
        data: dict - the data to update the item with.
    """

    for k, v in data.items():
        if k in ["id", "created_at", "updated_at", "deleted_at"]:
            continue
        setattr(item, k, v)
    save()


@bp.get("/departments/<string:department_id>")
def get_department(department_id):
    """Get a department by id.

    Args:
        department_id: str - the id of the department to fetch.

    Returns:
        dict: a json format containing the department.
        int: the status code of the response.
    """

    department = fetch_department(department_id)
    return department.to_dict(), 200


@bp.get("/departments")
def get_all_departments():
    """Get all departments in the database.

    Returns:
        dict: a json format containing the count of departments and a list of
            dictionaries representing each department.
        int: the status code of the response.
    """

    departments_list = (
        db.session.query(Department).options(joinedload(Department.doctors)).all()
    )
    departments = listAllObjects(departments_list)
    if departments.count > 0:
        status_code = 200
    else:
        status_code = 404
        flash("Failed to load departments, please try again later", "primary")

    return departments.to_dict(), status_code
