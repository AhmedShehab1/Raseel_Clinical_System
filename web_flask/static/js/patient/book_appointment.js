function nextClicked(event) {
    const fieldsetData = new Object();

    if (fieldsets[current_fs].classList.contains('search-form')) {
        const patientsList = document.querySelectorAll('.form-check-input');
        const patientID = getPatientID(patientsList);
        if (patientID !== null) {
            fieldsetData['patient_id'] = patientID;
        } else {
            alert('Please select a patient or continue with your account');
            event.preventDefault();
            event.stopPropagation();
            return;
        }
    } else {
        const fields = $(fieldsets[current_fs])[0].querySelectorAll('input, select, textarea');
        const fieldsValue = getFieldsValue(fields);
        if (!fieldsValue) {
            event.preventDefault();
            event.stopPropagation();
            return;
        }
        Object.assign(fieldsetData, fieldsValue);
    }
    Object.assign(formData, fieldsetData);
    displayNextStep();
}

function continueClicked(event) {
    formData['patient_id'] = event.target.id;
    displayNextStep();
}

function submitForm(data) {
    $.ajax({
        type: 'POST',
        url: '/api/v1/appointments',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify(data),
        success: function() {
            window.location.href = '/patient/dashboard';
        },
        error: function() {
            window.location.reload();
        }
    });
}
