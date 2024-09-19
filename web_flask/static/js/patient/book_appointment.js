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

        if (current_fs === vitals_index) {
            const vitalsData = new Object();
            Object.assign(vitalsData, fieldsValue);
            $.ajax({
                type: 'POST',
                url: `/api/v1/patients/${formData['patient_id']}/vitals`,
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                data: JSON.stringify(vitalsData),
                error: function (err) {
                    swal({
                        title: 'Error',
                        text: err.responseJSON.message + '. This step will be skipped.',
                        icon: 'error',
                        button: 'Ok',
                    });
                }
            });
        } else if (current_fs === allergies_index) {
            const allergiesData = new Object();
            Object.assign(allergiesData, fieldsValue);
            $.ajax({
                type: 'POST',
                url: `/api/v1/patients/${formData['patient_id']}/allergies`,
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                data: JSON.stringify(allergiesData),
                error: function (err) {
                    swal({
                        title: 'Error',
                        text: err.responseJSON.message + '. This step will be skipped.',
                        icon: 'error',
                        button: 'Ok',
                    });
                }
            });
        } else {
            Object.assign(fieldsetData, fieldsValue);
        }
    }
    if (Object.keys(fieldsetData).length !== 0) {
        Object.assign(formData, fieldsetData);
    }
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
