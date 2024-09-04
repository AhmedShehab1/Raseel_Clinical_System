from web_flask import create_app, db
import sqlalchemy as sa
import sqlalchemy.orm as so
from models import Vital, Diagnose, Prescription, Allergy  # Import your models
from uuid import uuid4
import random

app = create_app()

app_context = app.app_context()
app_context.push()

# Patient ID
patient_ids = ["0799bbb7-6bfa-445b-b072-76aaf9487d81", "6b73b575-7014-4788-bf6c-3c02cb0a0908", "559452cf-2736-4af6-8f47-3eda479c0bd8", "cf5bf037-b446-4f8d-b105-7adcbffae825"]

# Sample data generators
def generate_vitals(patient_id):
    return [
        Vital(
            patient_id=patient_id,
            height=random.uniform(150.0, 200.0),
            weight=random.uniform(50.0, 100.0),
            temperature=random.uniform(96.0, 104.0),
            blood_pressure=f"{random.randint(90, 140)}/{random.randint(60, 90)}",
            pulse=random.randint(60, 100)
        ) for _ in range(5)
    ]

def generate_diagnoses(patient_id):
    diagnoses = ["Flu", "Cold", "Headache", "Back Pain", "Asthma"]
    return [
        Diagnose(
            patient_id=patient_id,
            name=random.choice(diagnoses[i])
        ) for i in range(5)
    ]

def generate_prescriptions(patient_id):
    medications = ["Tylenol", "Advil", "Antibiotic", "Cough Syrup", "Antihistamine"]
    dosages = ["100mg", "200mg", "500mg", "1g", "2mg"]
    return [
        Prescription(
            patient_id=patient_id,
            medication=random.choice(medications[i]),
            dosage=random.choice(dosages[i])
        ) for i in range(5)
    ]

def generate_allergies(patient_id):
    allergens = ["Peanuts", "Milk", "Shellfish", "Pollen", "Dust"]
    reactions = ["Hives", "Swelling", "Itching", "Rash", "Anaphylaxis"]
    return [
        Allergy(
            patient_id=patient_id,
            allergen=allergens[i],
            reaction=random.choice(reactions[i])
        ) for i in range(5)
    ]

# Adding entries to the database
def add_entries_to_db():
    try:
        # Create and add entries for each model
        db.session.add_all(generate_vitals(random.choice(patient_ids)))
        db.session.add_all(generate_diagnoses(random.choice(patient_ids)))
        db.session.add_all(generate_prescriptions(random.choice(patient_ids)))
        db.session.add_all(generate_allergies(random.choice(patient_ids)))

        # Commit the session
        db.session.commit()
        print("Entries added successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
# Execute the function to add entries
add_entries_to_db()
