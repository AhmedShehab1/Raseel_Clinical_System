# Raseel Medical Care Center

**Raseel Clinical System** is a web-based platform designed to enhance the quality of care for clinic staff and patients. By integrating modern technologies, the system streamlines processes like appointment scheduling, patient management, and staff organization, providing a reliable and efficient solution for medical care environments.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#system-architecture)
- [Database Design](#database-design)
- [Challenges](#challenges)
- [Learning Outcomes](#learning-outcomes)
- [Future Improvements](#future-improvements)
- [Contributors](#contributors)
- [License](#license)
- [Contact](#contact)

## Introduction

**Raseel Clinical System** is designed to solve one major problem: improving the efficiency and reliability of clinic operations. With features tailored to meet the needs of patients and medical staff, this system aims to streamline routine tasks like appointment scheduling, patient management, and staff coordination. Our goal is to ensure that the quality of care is significantly improved through better organization and ease of use.

As biomedical engineers, we were inspired by the vision of leveraging technology to enhance clinical efficiency. The challenge of designing a system that not only improves workflows but also builds trust among users motivated us to create a platform where medical professionals can focus more on patient care, and less on administrative tasks.

## Features

- **Robust Authentication System**: Secure login for staff and patients.
- **Appointment Scheduling**: Doctors and receptionists can schedule and manage appointments seamlessly.
- **Patient Management**:  Doctors can view and manage patient data.
- **Staff Member Management**: Admins can add and manage staff members, assigning roles and responsibilities.
- **Integrated Third-Party APIs**: Fetch diagnoses and medications to streamline doctors' workflows.
- **Full-Text Search**: Using Elasticsearch, staff can efficiently search for patients, appointments, and more.

## Technologies Used

**Backend:**
- Flask (Python framework)
- Nginx & Gunicorn (Web server and WSGI server)
- HAProxy (Load balancer)
- MySQL Master-Master Cluster
- RESTful APIs

**Frontend:**
- JavaScript, HTML, CSS
- Bootstrap, jQuery

**Other Tools and Libraries:**
- Elasticsearch (Full-text search engine)
- Flask Extensions (e.g., Flask-Babel, Flask-Moment, Flask-Login)
- Docker (For containerized deployment)

## Installation

To set up the project locally, follow these steps:

### Prerequisites
- Python 3.8+
- MySQL
- Docker

### Steps:
1. **Clone the repository**:
   ```bash
   git clone https://github.com/AhmedShehab1/Raseel_Clinical_System.git
   cd Raseel_Clinical_System
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the MySQL database**:
   ```sql
   CREATE DATABASE Raseel_db CHARACTER SET utf8 COLLATE utf8_bin;
   CREATE USER 'raseel'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON Raseel_db.* TO 'raseel'@'localhost';
   FLUSH PRIVILEGES;
   ```

5. **Run database migrations**:
   ```bash
   flask db upgrade
   ```

6. **Populate the database** using `data_only_generator.sql`.
   ```bash
   mysqldump -u raseel -p  Raseel_db < data_only_generator.sql
   ```

7. **Run Elasticsearch** using Docker:
   ```bash
   docker run --name elasticsearch -d --rm -p 9200:9200 --memory="2GB" -e discovery.type=single-node -e xpack.security.enabled=false -t docker.elastic.co/elasticsearch/elasticsearch:8.11.1
   ```

8. **Reindex Documents for ElasticSearch Functionality**
    ```bash
    # Enter Flask shell to execute reindexing commands
    flask shell
    ```
    Inside the shell, execute the following commands:
    ```python
    >>> Patient.reindex()
    >>> StaffMember.reindex()
    ```
This will ensure your ElasticSearch indices are populated correctly and ready for searching.

 9. **Environment Setup**

You need to create two environment configuration files: `.flaskenv` and `.env` in the root directory of your project.

#### **.flaskenv**
```ini
FLASK_APP=web_flask.clinical_system
FLASK_DEBUG=1
FLASK_ENV=development

# Mail server settings (for features like resetting user passwords)
MAIL_SERVER=us2.smtp.mailhostbox.com
MAIL_PORT=587
MAIL_USE_TLS=1
```
#### **.env**
```ini
# ElasticSearch URL (comment this line if you're not using ElasticSearch)
ELASTICSEARCH_URL='http://localhost:9200'

# Email functionality support
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
MAIL_DEFAULT_SENDER=your-email@example.com

# Flask secret key
SECRET_KEY='try_to_guess_me'

# MySQL Database connection URL
DATABASE_URL=mysql+mysqldb://raseel:password@localhost:3306/Raseel_db
```

10. **Run the Flask application**:
   ```bash
   flask run
   ```

## Usage

### Roles:
- **Patient**: Access the system via the public domain (e.g., raseel.com).
- **Staff (Doctors, Admin, Receptionist)**: Access the system through a dedicated subdomain (e.g., staff.raseel.com).

## System Architecture

This project adheres to an MVC/MVT (Model-View-Template) architecture utilizing Flask, with RESTful APIs facilitating communication between the frontend and backend components. The database schema, detailed in the Entity-Relationship Diagram (ERD) below, is crucial for understanding the relationships and interactions between the system's various entities like patients, doctors, and appointments.

## Database Design

![MySQL ERD](images/sql_ERD.png)

Figure 1: ERD of the MySQL Database used in the project.

The database is designed to optimize the management and querying of medical data. Here are a few highlights and rationales for the design choices:

**Normalization**: The database schema is normalized to reduce redundancy and improve data integrity. For example, the separation of patients, doctors, and appointments into distinct tables prevents data duplication and facilitates easier updates.

**Foreign Key Relationships**: Relationships are established using foreign keys which ensure referential integrity across the database. For instance, doctor_id in the appointments table links an appointment to a specific doctor.

**Indexing**: Key columns such as email in the doctors table and patient_id in the appointments table are indexed to speed up query performance, crucial for features like searching and reporting.

**Constraints**: Data integrity is enforced through various constraints. For instance, the email fields in patients and doctors tables are set to be unique to prevent duplicate records.

***Integration with Frontend***

Jinja2 templates are used for dynamic content rendering on the frontend, enhancing the responsiveness of the user interface to different user actions. The database design supports the application's functionality by ensuring efficient data storage and retrieval, which is essential for features such as appointment scheduling and management.

***Search Functionality***

Elasticsearch is integrated into the backend to provide advanced search capabilities. This allows for fast and efficient querying of large datasets, which is particularly beneficial for features like searching patient records or past appointments based on various criteria.

## Screenshots and Media
Below are some visual representations of the Raseel Clinical System interfaces for different roles and key features:

### Admin Dashboard
The Admin dashboard provides a comprehensive view of the clinic's operations, including staff management, patient records, and more.

![Admin Interface](images/dashboard_admin.png)
![Admin Interface (edit member)](images\admin_dashboard_edit_member.png)
![Admin Interface edit member on success](images/admin_interface_update_member_on_success.png)

### Doctor Interface
The Doctor's dashboard allows quick access to patient information, appointment scheduling, and clinical records. Here’s an example of the doctor interface while viewing a patient's record:

![Doctor Interface](images/doctor_interface.png)
![Doctor Interface (Patient Modal)](images/doctor_dashboard_patient_modal.png)
![Doctor Interface (Patient Modal)](images/doctor_dashboard_patient_modal_1.png)


### Appointment Scheduling
The scheduling feature for doctors and receptionists helps manage appointments and avoid conflicts.

### Search Functionality
Raseel's integrated search engine enables efficient searches for patients, doctors, and staff members using Elasticsearch.

- Searching Patient By Phone Number
![Doctor Interface (Search Patient by phone)](images\doctor_dashboard_patient_search_by_phone.png)
- Searching Staff Members by Name
![Admin Interface](images\admin_dashboard_search_by_name.png)

### Patient Portal
Patients can view their appointments, update contact details, and communicate with clinical staff through the patient portal.

## Challenges

1. **Setting Up Load Balancing**: Implementing a load balancer using HAProxy to distribute traffic between two Nginx servers, ensuring availability and scalability. Configuring a MySQL Master-Master cluster for handling database load efficiently.
   - **Solution**: We researched the setup of UNIX sockets for faster communication and configured SSL termination at the load balancer to reduce server overhead.

2. **Integrating Elasticsearch**: Adding Elasticsearch to the project to improve search functionalities was challenging due to initial performance bottlenecks.
   - **Solution**: By tuning the Elasticsearch cluster configuration and optimizing queries, we were able to provide doctors and admins with faster and more reliable search results.

## Learning Outcomes

**Mazen Atef Atlam**:
- Mastered Flask's backend capabilities and developed advanced frontend components using CSS, HTML, and JavaScript.


**Ahmed Abdelghafar Shehab**:
- Learned to integrate **Elasticsearch** for enhanced search capabilities.
- Improved Python multithreading skills and integrated Flask-Babel for localization (including Arabic).
- Gained experience in using **GitHub Actions** for CI pipelines, ensuring the reliability of code with automated testing.

## Future Improvements

- **Expanding Roles**: Adding support for new roles such as Pharmacist and Laboratory Technician.
- **Lab Requests**: Allowing doctors to request lab results and assign medications directly to pharmacists for a more integrated workflow.

## Contributors

- **Mazen Atef Atlam** – Full-Stack Developer: Worked on the **patient portal** and **appointment scheduling**.
- **Ahmed Abdelghafar Shehab** – Full-Stack Developer: Focused on **admin systems**, **authentication**, and **search functionality**.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Contact

- **Ahmed Abdelghafar Shehab**: [LinkedIn](https://www.linkedin.com/in/ahmed-shehab-engineering)
- **Mazen Atef Atlam**: [LinkedIn](https://www.linkedin.com/in/mazen-atlam-801788267)
