from api.v1.errors import bad_request
from web_flask import db
from api.v1.views import bp
from models import Department, Doctor
from flask import request
import sqlalchemy as sa


class AllDepartments:
    """Class to represent all departments in the database.

    Attributes:
        count: int - the number of departments in the database.
        results: list - a list of dictionaries representing each department

    Methods:
        to_dict() - returns a dictionary representation of the class.
    """

    def __init__(self, departments_list):
        """Initialize the AllDepartments class.

        Args:
            departments_list: list - a list of Department objects.
        """

        self.count = len(departments_list)
        self.results = [department.to_dict() for department in departments_list]

    def to_dict(self):
        """Return a jsn representation of the class."""

        return {
            'count': self.count,
            'results': self.results
        }

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
        if k in ['id', 'created_at', 'updated_at', 'deleted_at']:
            continue
        setattr(item, k, v)
    save()

@bp.get('/departments/<string:department_id>')
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

@bp.get('/departments')
def get_all_departments():
    """Get all departments in the database.

    Returns:
        dict: a json format containing the count of departments and a list of
            dictionaries representing each department.
        int: the status code of the response.
    """

    # dep_query = sa.delete(Department).where(Department.name.in_(["Cardiology", "Surgery", "Dental", "Orthopedics"]))
    # db.session.execute(dep_query)
    # doc_query = sa.delete(Doctor).where(Doctor.name.in_(["Dr. Mazen", "Dr. Ahmed", "Dr. Anas", "Dr. Sherif"]))
    # db.session.execute(doc_query)
    # db.session.commit()

    # surgery_doctors = []
    # dental_doctors = []
    # cardiology_doctors = []
    # orthopedics_doctors = []
    # surgery = Department('Surgery', doctors=surgery_doctors)
    # dental = Department('Dental', doctors=dental_doctors)
    # cardiology = Department('Cardiology', doctors=cardiology_doctors)
    # orthopedics = Department('Orthopedics', doctors=orthopedics_doctors)
    # mazen = Doctor('Dr. Mazen', '12345@Aa', 'mazen@gmail.com', 'MBBS', str(surgery.id))
    # ahmed = Doctor('Dr. Ahmed', '12345@Aa', 'ahmed2@gmail.com', 'MBBS', str(surgery.id))
    # anas = Doctor('Dr. Anas', '12345@Aa', 'anas@gmail.com', 'MBBS', str(surgery.id))
    # sherif = Doctor('Dr. Sherif', '12345@Aa', 'sherif@gmail.com', 'MBBS', str(dental.id))
    # surgery_doctors.append(mazen)
    # surgery_doctors.append(ahmed)
    # surgery_doctors.append(anas)
    # dental_doctors.append(sherif)
    # db.session.add(mazen)
    # db.session.commit()
    # db.session.add(ahmed)
    # db.session.commit()
    # db.session.add(anas)
    # db.session.commit()
    # db.session.add(sherif)
    # db.session.commit()
    # db.session.add(surgery)
    # db.session.commit()
    # db.session.add(cardiology)
    # db.session.commit()
    # db.session.add(dental)
    # db.session.commit()
    # db.session.add(orthopedics)
    # db.session.commit()

    departments_list = db.session.scalars(sa.select(Department)).all()
    departments = AllDepartments(departments_list)
    status_code = 200 if departments.count > 0 else 404

    return departments.to_dict(), status_code
