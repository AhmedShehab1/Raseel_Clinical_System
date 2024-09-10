from web_flask import create_app, db
import sqlalchemy as sa
import sqlalchemy.orm as so
from models import Vital, Diagnose, Prescription, Allergy, Department, Doctor, GenderType, Patient  # Import your models
from uuid import uuid4
import random
from datetime import datetime, timedelta
from faker import Faker
import random
app = create_app()

app_context = app.app_context()
app_context.push()


fake = Faker(['ar_SA'])

def generate_birth_date():
    today = datetime.today()
    age = random.randint(18, 60)
    return today - timedelta(days=age * 365)


def generate_contact_number():
    return f"05{random.randint(10000000, 99999999)}"



def generate_national_id():
    return f"22{random.randint(10000000, 99999999)}"

def generate_gender(name):
    return GenderType.Male if name in ['السيد', 'المهندس', 'الأستاذ', 'سالم', 'سليمان', 'الدكتور'] or fake.random_element(["محمد", "علي", "عبدالله"]) in name else GenderType.Female



def update_doctors_created_at():
    # Fetch all doctors
    all_doctors = db.session.scalars(sa.select(Doctor))

    # Iterate over each doctor
    for doctor in all_doctors:
        # Generate a random date that is at least 4 years before 2024 (i.e., before 2020)
        start_date = datetime.date(2014, 1, 1)  # Random date range start (you can adjust)
        end_date = datetime.date(2020, 12, 31)  # Latest date, 4 years before 2024

        # Generate a random date between the start and end date
        random_days = random.randint(0, (end_date - start_date).days)
        random_date = start_date + datetime.timedelta(days=random_days)

        # Update the doctor's created_at field with the random date
        doctor.created_at = random_date

    # Commit the changes to the database
    db.session.commit()

def generate_patients(num_patients=50):
    for _ in range(num_patients):
        # Generate a realistic Arabic name
        name = fake.name()

        # Determine gender based on name
        gender = generate_gender(name)

        # Generate random email using the name
        email = f"{name.replace(' ', '.').lower()}@example.com"

        # Generate contact number and national ID
        contact_number = generate_contact_number()
        national_id = generate_national_id()

        # Random birth date
        birth_date = generate_birth_date()

        # Use the name or a simple variant as the password
        password = name.split()[0].lower()

        # Create a new patient instance
        patient = Patient(
            name=name,
            email=email,
            contact_number=contact_number,
            birth_date=birth_date,
            password=password,
            national_id=national_id,
            gender=gender
        )

        # Add patient to the session
        db.session.add(patient)

    # Commit the session to the database
    db.session.commit()

# Generate and add 50 patients to the database
# generate_patients()

def add_doc(doc_name, cert, dep_name, eng_name):
    dep = db.session.scalar(sa.select(Department).where(Department.name == dep_name))
    doc = Doctor(name=doc_name, certificates=cert, department=dep, password=eng_name,
                 email=f'{eng_name}@raseel.sa')
    db.session.add(doc)
    db.session.commit()


# add_doc('د. صبري محارق', """ماجستير أشعة تشخيصية
# أخصائي الأشعة التشخيصية""", 'X Ray Place', 'sabri_mahareq')

# add_doc('د. فهمي باخلقي', """استشاري طب الأطفال وحديثي الولادة
# دكتوراه (البورد العربي)
# استشاري الأطفال""", 'Pediatric Clinic', 'fahmi_bakhlqi')

# add_doc('د. هيفاء الخالد', """ماجستير طب الأطفال
# أخصائية أطفال""", 'Pediatric Clinic', 'haifa_alkhaled')

# add_doc('د. محمود الحسيني', """ماجستير طب الأطفال
# طبيب أطفال""", 'Pediatric Clinic', 'mahmoud_alhusseini')

# add_doc('د. عبدالكريم الحريري', """شهادة الدراسات العليا التخصصية الطب الباطني
# شهادة البورد العربي في الأمراض الباطنية الجزء الأول
# أخصائي الأمراض الباطنية""", 'Internal Medicine Clinic', 'abdelkarim_alhariri')

# add_doc('د. امل حليمة', """شهادة الدراسات العليا التخصصية الطب الباطني
# شهادة البورد العربي في الأمراض الباطنية الجزء الأول
# طبيبة الأمراض الباطنية""", 'Internal Medicine Clinic', 'amal_halima')

# add_doc('د. مها محمد الشاذلي', """ماجستير الأمراض الصدرية والدرن
# نائب الأمراض الصدرية""", 'Chest Clinic', 'maha_alshezli')

# add_doc('د. أحمد رشيد', """الدراسات العليا في الجراحة العامة
# محاضر سابق في جامعة حلب
# أخصائي الجراحة العامة""", 'General Surgery Clinic', 'ahmed_rashid')

# add_doc('د. محمود شيخ خليل', """ماجستير طب وجراحة العيون
# أخصائي العيون""", 'Eye Clinic', 'mahmoud_sheikh_khalil')

# add_doc('د. حسن خطاب', """الدراسات العليا من جامعة دمشق
# البورد العربي (الجزء الأول) في الأنف والأذن والحنجرة
# أخصائي الأنف والأذن والحنجرة""", 'Ear, Nose and Throat Clinic', 'hasan_khitab')

# add_doc('د. زكور ابراهيم', """الاختصاص السوري في الجراحة العظمية
# شهادات متقدمة في الجراحة العظمية من فرنسا
# دبلوم في جراحة اليد من فرنسا
# أخصائي العظام""", 'Orthopedic Clinic', 'zakour_ibrahim')

# add_doc('د. احمد مسعود الشناوي', """ماجستير جراحة العظام
# أخصائي عظام""", 'Orthopedic Clinic', 'ahmed_masoud')

# add_doc('د. خالد الأسعد', """بكالوريوس طب وجراحة الفم والأسنان
# طبيب أسنان عام""", 'Dental Clinic', 'khaled_alasad')

# add_doc('د. شيرين علي', """بكالوريوس طب وجراحة الفم والأسنان
# طبيبة أسنان عامة""", 'Dental Clinic', 'shereen_ali')

# add_doc('د. عبدالله خالد', """بكالوريوس طب وجراحة الفم والأسنان
# طبيب أسنان عام""", 'Dental Clinic', 'abdullah_khaled')

# add_doc('د. عبدالله سلمان', """بكالوريوس طب وجراحة الفم والأسنان
# طبيب أسنان عام""", 'Dental Clinic', 'abdullah_salman')

# add_doc('د. لؤي يوسف الحميدي', """بكالوريوس طب وجراحة الفم والأسنان
# طبيب أسنان عام""", 'Dental Clinic', 'louay_alhamidi')

# add_doc('د. مصطفى فتحي', """بكالوريوس طب وجراحة الفم والأسنان
# طبيب أسنان عام""", 'Dental Clinic', 'mostafa_fathi')

# add_doc('د. احمد حلمي برغال', """أخصائي نائب تقويم الأسنان
# ماجستير في تقويم وتجميل الأسنان والفكين""", 'Orthodontic Clinic', 'ahmed_helmi_borgal')

# add_doc('د. أحمد بن حدجة', """بكالوريوس طب وجراحة
# طبيب عام""", 'الطب العام و الطوارئ', 'ahmed_bin_hadja')

# add_doc('د. هاله الشيخ', """بكالوريوس طب وجراحة""", 'الطب العام و الطوارئ', 'hala_alsheikh')

# add_doc('د. فتحية عبد الرحمن', """بكالوريوس طب وجراحة
# طبيبة عامة""", 'الطب العام و الطوارئ', 'fathiya_abdelrahman')

# add_doc('د. بسام سالم علي ناصر', """بكالوريوس طب وجراحة
# طبيب عام""", 'الطب العام و الطوارئ', 'bassem_nasser')

# add_doc('د. حازم عبدالهادي', """بكالوريوس العلاج الطبيعي
# أخصائي العلاج الطبيعي""", 'قسم العلاج الطبيعي (رجال)', 'hazem_abdulhadi')

# add_doc('د. احسان محمد', """بكالوريوس العلاج الطبيعي
# أخصائية العلاج الطبيعي""", 'قسم العلاج الطبيعي (نساء)', 'ihsan_mohamed')

# add_doc('د. سحر جابر', """شهادة الدبلوم العالي في أمراض النساء والولادة
# طبيبة النساء والولادة""", 'Obstetrics and Gynecology Clinic', 'sahar_jaber')

# add_doc('د. نهلة منصور', """ماجستير أمراض النساء والولادة
# أخصائية أمراض النساء والولادة""", 'Obstetrics and Gynecology Clinic', 'nahla_mansour')

# add_doc('د. عائشة جلال', """أخصائية أمراض النساء والولادة""", 'Obstetrics and Gynecology Clinic', 'aisha_jalal')

# add_doc('د. آمال الباز', """ماجستير أمراض النساء والولادة""", 'Obstetrics and Gynecology Clinic', 'amal_albaz')

# add_doc('د. وفاء محمد', """أخصائية أمراض النساء والولادة""", 'Obstetrics and Gynecology Clinic', 'wafaa_mohammed')

# add_doc('د. إيمان الغمري', """ماجستير طب وجراحة العيون
# أخصائية طب وجراحة العيون""", 'Ophthalmology Clinic', 'eman_elghamry')

# add_doc('د. إيمان علام', """ماجستير الأمراض الجلدية
# أخصائية الأمراض الجلدية""", 'Dermatology Clinic', 'eman_allam')

# add_doc('د. فاتن الطيب', """دكتوراه الأمراض الجلدية
# أخصائية الأمراض الجلدية""", 'Dermatology Clinic', 'faten_eltayeb')

# add_doc('د. شادية حمدي', """ماجستير الأمراض الجلدية
# أخصائية الأمراض الجلدية""", 'Dermatology Clinic', 'shadia_hamdi')

# add_doc('د. طارق الأشموني', """ماجستير في الجراحة التجميلية
# أخصائي الجراحة التجميلية""", 'Plastic Surgery Clinic', 'tarek_aleshmony')

# add_doc('د. سلوى عبد الغني', """ماجستير طب الأعصاب
# أخصائية طب الأعصاب""", 'Neurology Clinic', 'salwa_abdelghany')

# add_doc('د. هشام زين الدين', """ماجستير طب الأعصاب
# أخصائي طب الأعصاب""", 'Neurology Clinic', 'hesham_zeineddin')

# add_doc('د. مصطفى أبو يوسف', """دكتوراه في الأمراض الباطنية والغدد الصماء
# أخصائي الغدد الصماء""", 'Endocrinology Clinic', 'mostafa_abuyoussef')

# add_doc('د. هيثم شحاته', """ماجستير الأمراض الباطنية والغدد الصماء
# أخصائي الغدد الصماء""", 'Endocrinology Clinic', 'haitham_shehata')

# add_doc('د. محمد السيد', """دكتوراه في أمراض السرطان
# أخصائي الأورام""", 'Oncology Clinic', 'mohammed_elsayed')

# add_doc('د. علي حسن', """ماجستير في أمراض السرطان
# أخصائي الأورام""", 'Oncology Clinic', 'ali_hassan')

# add_doc('د. كريم أحمد', """أخصائي علاج الأورام""", 'Oncology Clinic', 'karim_ahmed')

# add_doc('د. أيمن عبد الفتاح', """ماجستير الأمراض الروماتيزمية
# أخصائي الأمراض الروماتيزمية""", 'Rheumatology Clinic', 'ayman_abdelfattah')



def update_doctors_created_at():
    # Fetch all doctors
    all_doctors = db.session.scalars(sa.select(Doctor))

    # Iterate over each doctor
    for doctor in all_doctors:
        # Generate a random date that is at least 4 years before 2024 (i.e., before 2020)
        start_date = datetime.date(1980, 1, 1)  # Random date range start (you can adjust)
        end_date = datetime.date(2019, 12, 31)  # Latest date, 4 years before 2024

        # Generate a random date between the start and end date
        random_days = random.randint(0, (end_date - start_date).days)
        random_date = start_date + datetime.timedelta(days=random_days)

        # Update the doctor's created_at field with the random date
        doctor.created_at = random_date

    # Commit the changes to the database
    db.session.commit()


# Patient ID
patient_list = [
    "03c3253f-d23b-4f32-9554-025cc1a2ee52",
    "0450742d-c9d0-4eb4-8b49-10d62cba2ba4",
    "075713db-615b-483a-a9f3-bf012fe1a6b3",
    "09780803-ba35-458c-8f8e-f8b414eb04e3",
    "0ea2ded1-167a-43cd-aa33-0e066450cedd",
    "10022ef3-cd79-417a-9c1b-a4792ee7bebb",
    "1b9a6893-079d-4fee-8d76-caa56895c043",
    "1dfae994-0c7d-4b8e-a991-b1419fa152ba",
    "234a23f0-4265-4d0a-b064-33a0bb2888a5",
    "3d0f6e14-634d-4c9a-93a8-886547fa0dc0",
    "4a84a758-ed97-437c-a961-31872ea56d8d",
    "507222e8-8ae4-4fce-826f-55a3c49d462e",
    "52622eaf-3892-4433-9d5d-8a88f347043c",
    "545026d1-a5ad-4d96-8367-a4eb736c72c7",
    "55ce6a60-fd7c-4402-9400-859b9c8b6a29",
    "62bac28b-3ae4-4b17-bf40-e92dcdc209ee",
    "649a9445-e40d-43b0-90d9-ed9266d04003",
    "64b55263-698b-4866-b289-2fbddc806ef4",
    "68e71b8d-2761-42b7-b1e4-41adf1796584",
    "6c26b775-ed2d-401b-9afc-bc19bd9a18d4",
    "6c29b6fe-817a-475a-8e01-d40eebbd1e2c",
    "748ad2b0-7c91-4085-98cf-3ff6b36ea710",
    "828fdf3e-49af-4dc5-8b38-450ef40b50c9",
    "84fb4176-f366-44e0-940a-f9aa0a8719e7",
    "8f19a085-ce05-4cdc-bb5a-affdd83a0706",
    "911e60e4-1042-4fa7-93dc-1f139b45df8b",
    "91835752-0dfb-48d5-ac83-b8a54e6280e0",
    "924cc221-cbc8-4215-90bc-0ffcd4d9a75a",
    "95964919-d358-4c38-aabc-1792932eb493",
    "98320208-8db1-4851-88f8-1d01302ef9e1",
    "9967b0dc-41d8-407e-983f-005dd4ddb22f",
    "9a54382e-79d7-48e5-8610-ceacea160703",
    "9ac37965-9bc7-4ac2-8b31-38d5b119297b",
    "9ad22ae1-1664-4b61-8726-753b5e4161fb",
    "9c77a957-5635-41a2-9665-5d73b01a6e3c",
    "a667c63e-c0ee-4cee-bf53-135609115f24",
    "a9310461-0409-43ad-ae86-f38e555e0023",
    "b1c689e3-4d88-4522-a61b-faf778b6242a",
    "b59a6432-308e-4bce-ac8c-b7ea4ab2f3b2",
    "beea2b7e-91fb-489d-919e-6d034717c16b",
    "c04b5223-1826-4ae3-a56e-fdcad3ae8a52",
    "c1e8758f-371f-4639-b25f-3230afb0d6f1",
    "c6a063f1-7eb8-4d15-b7ec-d87c7d12c36f",
    "c9b5a1bd-08ee-4ef4-934c-40d1f12c96c7",
    "d096d4de-7544-45e2-a4e5-ef8680e2b36e",
    "d2795b71-303b-4b0a-be5d-f284d5daceda",
    "dc456059-6fda-499d-b77e-3f5fcf4332f6",
    "e0308187-5b25-4303-a2da-a2911deecd9e",
    "e54da15f-904f-4cc5-8b94-2bb67cdd8999",
    "fa0cd183-1803-46c6-bef9-af98cc9f7884"
]


# Sample data generators
def generate_vitals(patient_id):
    return [
        Vital(
            patient_id=patient_id,
            height=random.uniform(150.0, 200.0),
            weight=random.uniform(50.0, 100.0),
            temperature=random.uniform(96.0, 104.0),
            blood_pressure=f"{random.randint(90, 140)}/{random.randint(60, 90)}",
            pulse=random.randint(60, 100),
            measured_at=datetime.now() - timedelta(days=random.randint(1, 365))
        ) for _ in range(5)
    ]

def generate_diagnoses(patient_id):
    diagnoses = [
    "Flu", "Cold", "Headache", "Back Pain", "Asthma", "Diabetes",
    "Hypertension", "Migraine", "Pneumonia", "Bronchitis", "Arthritis",
    "Heart Disease", "Depression", "Anxiety", "Gastroenteritis",
    "Chronic Fatigue Syndrome", "Sinus Infection", "Irritable Bowel Syndrome",
    "COVID-19", "Stroke", "Skin Infection", "Kidney Stones", "Appendicitis",
    "Liver Disease", "Gastritis", "Ulcer", "Allergic Rhinitis",
    "Conjunctivitis", "Urinary Tract Infection", "Tonsillitis"
    ]
    return [
        Diagnose(
            patient_id=patient_id,
            name=diagnoses[i]
        ) for i in range(5)
    ]

def generate_prescriptions(patient_id):
    medications = [
    "Tylenol", "Advil", "Antibiotic", "Cough Syrup", "Antihistamine", "Aspirin",
    "Ibuprofen", "Paracetamol", "Amoxicillin", "Penicillin", "Metformin",
    "Lisinopril", "Atorvastatin", "Hydrochlorothiazide", "Prednisone",
    "Omeprazole", "Albuterol", "Insulin", "Hydrocodone", "Warfarin"
    ]
    dosages = [
    "100mg", "200mg", "500mg", "1g", "2mg", "50mg", "25mg", "75mg", "10mg",
    "5mg", "250mg", "1.5g", "4mg", "12.5mg", "0.5mg", "125mg", "600mg",
    "300mg", "15mg", "800mg"
    ]
    return [
        Prescription(
            patient_id=patient_id,
            medication=medications[i],
            dosage=dosages[i]
        ) for i in range(5)
    ]

def generate_allergies(patient_id):
    allergens = [
    "Peanuts", "Milk", "Shellfish", "Pollen", "Dust", "Eggs", "Soy", "Wheat", "Tree Nuts",
    "Fish", "Latex", "Bee Stings", "Mold", "Pet Dander", "Insect Bites", "Perfume",
    "Medication Allergy", "Nickel", "Sunlight", "Gluten"
    ]
    reactions = [
    "Hives", "Swelling", "Itching", "Rash", "Anaphylaxis", "Wheezing",
    "Breathing Difficulty", "Nausea", "Vomiting", "Diarrhea", "Runny Nose",
    "Watery Eyes", "Coughing", "Sneezing", "Redness", "Dizziness", "Chest Tightness",
    "Fainting", "Abdominal Pain", "Blistering"
    ]
    return [
        Allergy(
            patient_id=patient_id,
            allergen=allergens[i],
            reaction=reactions[i]
        ) for i in range(5)
    ]

# Adding entries to the database
def add_entries_to_db():
    try:
        for patient in patient_list:
            db.session.add_all(generate_vitals(patient))
            db.session.add_all(generate_diagnoses(patient))
            db.session.add_all(generate_prescriptions(patient))
            db.session.add_all(generate_allergies(patient))

        # Commit the session
        db.session.commit()
        print("Entries added successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
# Execute the function to add entries
add_entries_to_db()
