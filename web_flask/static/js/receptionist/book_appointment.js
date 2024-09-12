const patientAttributes = ['name', 'password', 'email', 'contact_number', 'gender', 'national_id', 'birth_date'];
const newPatientData = new Object();

function nextClicked(event) {
    const fieldsetData = new Object();

    if (fieldsets[current_fs].classList.contains('search-form')) {
        const patientsList = document.querySelectorAll('.form-check-input');
        const patientID = getPatientID(patientsList);
        if (patientID !== null) {
            fieldsetData['patient_id'] = patientID;
            for (let i = 1; i < 3; i++) {
                fieldsets[i].classList.add('skipped');
                $("#progressbar li").eq(i).addClass("active");
            }
        }
    } else {
        const fields = $(fieldsets[current_fs])[0].querySelectorAll('input, select, textarea');
        const fieldsValue = getFieldsValue(fields, patientAttributes);
        if (!fieldsValue) {
            event.preventDefault();
            event.stopPropagation();
            return;
        }

        if (current_fs === create_account_index || current_fs === personal_info_index) {
            Object.assign(newPatientData, fieldsValue);
            if (current_fs === personal_info_index) {
                $.ajax({
                    type: 'POST',
                    url: '/api/v1/patients',
                    contentType: 'application/json; charset=utf-8',
                    dataType: 'json',
                    data: JSON.stringify(newPatientData),
                    success: function(data) {
                        fieldsetData['patient_id'] = data['id'];
                        Object.assign(formData, fieldsetData);

                    },
                    error: function() {
                        window.location.reload();
                    }
                });
            }
        } else {
            Object.assign(fieldsetData, fieldsValue);
        }
    }
    if (Object.keys(fieldsetData).length !== 0) {
        Object.assign(formData, fieldsetData);
    }
    displayNextStep();
}

function continueClicked(){
    return;
}

function submitForm(data) {
    $.ajax({
        type: 'POST',
        url: '/api/v1/appointments',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify(data),
        success: function() {
            window.location.href = '/receptionist/dashboard'
        },
        error: function() {
            window.location.reload();
        }
    });
}
