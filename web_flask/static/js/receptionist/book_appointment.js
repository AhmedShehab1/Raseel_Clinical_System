$(document).ready(function(){
    const formData = {};
    const newPatientData = {};
    const patientAttributes = ['name', 'password', 'email', 'contact_number', 'gender', 'national_id', 'birth_date'];
    var fieldsets = $('fieldset');
    var current_fs = 0, previous_fs = fieldsets.length - 1, next_fs = 1; //fieldsets
    var opacity;
    var all_doctors_working_hours = {};


    $("form").bind("keypress", function (event) {
        if (event.keyCode === 13) {
            console.log(event.keyCode);
            $(".search").attr('value');
            $(".submit").attr('value');
            event.preventDefault();
        }
    });

    $(".form-check-input").click(function(){
        const deselectButton = $(".deselect")[0];
        deselectButton.disabled = false;
        deselectButton.classList.remove('btn-outline-secondary');
        deselectButton.classList.add('btn-secondary');
    });

    $(".deselect").click(function(){
        const patientsList = document.querySelectorAll('.form-check-input');
        if (typeof patientsList !== 'undefined' && patientsList !== null) {
            patientsList.forEach((patient) => {
                if (patient.checked) {
                    patient.checked = false;
                }
            });
        }
        const deselectButton = $(this)[0];
        deselectButton.disabled = true;
        deselectButton.classList.remove('btn-secondary');
        deselectButton.classList.add('btn-outline-secondary');
    });

    $(".skip").click(function(){
        // Make all fields' value equal to "" in the current fieldset, which is fieldsets[current_fs] at current_fs = 3
        const fields = $(fieldsets[current_fs])[0].querySelectorAll('input, select, textarea');
        fields.forEach((field) => {
            if (field.type === 'button' || field.type === 'submit') {
                return;
            }
            field.value = "";
        });
        $(this).parent().find('input[name="next"]').click();
    });

    $(".submit").click(function(event){
        const fieldsetData = {};
        const fields = $(fieldsets[current_fs])[0].querySelectorAll('input, select, textarea');
        var valid = true;

        fields.forEach((field) => {
            if (field.type === 'button' || field.type === 'submit') {
                return;
            }
            fieldsetData[field.name] = field.value;
            removeFeedback(field);
            if (!field.checkValidity()) {
                createInvalidFeedback(field, field.validationMessage);
                valid = false;
            } else {
                createValidFeedback(field);
            }

        });
        fieldsets[current_fs].classList.add('was-validated');

        const date = fieldsetData['datetime'].split('T')[0];
        const time = fieldsetData['datetime'].split('T')[1];
        const hour = time.split(':')[0];
        const miniutes = time.split(':')[1][0] + time.split(':')[1][1];
        const am_pm = time.split(':')[1][2] + time.split(':')[1][3];
        if (parseInt(miniutes) < 30) {
            fieldsetData['datetime'] = date + 'T' + hour + ':' + '00' + am_pm;
        } else {
            fieldsetData['datetime'] = date + 'T' + hour + ':' + '30' + am_pm;
        }

        const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
        const appointmentDate = new Date(fieldsetData['datetime']);
        const appointmentDay = weekday[appointmentDate.getDay()];
        const doctorID = fieldsetData['doctor'];
        const doctorWorkingHours = all_doctors_working_hours[doctorID];

        if (typeof doctorWorkingHours !== 'undefined') {
            doctorWorkingHours.forEach((workingHour) => {
                if (workingHour['day'] === appointmentDay) {
                    const startHour = parseInt(workingHour['start_hour'].split(':')[0]);
                    const startMinutes = parseInt(workingHour['start_hour'].split(':')[1]) + (startHour * 60);
                    
                    const endHour = parseInt(workingHour['end_hour'].split(':')[0]);
                    const endMinutes = parseInt(workingHour['end_hour'].split(':')[1]) + (endHour * 60);

                    const appointmentMinutes = parseInt(hour) * 60 + parseInt(miniutes);
                    if (appointmentMinutes < startMinutes || appointmentMinutes > endMinutes) {
                        alert('The appointment time is not within the working hours of the doctor. Please choose another time or select another doctor.');
                        valid = false;
                    }
                }
            });
        }

        $.ajax({
            type: 'GET',
            url: '/api/v1/appointments/' + fieldsetData['doctor'],
            contentType: 'application/json; charset=utf-8',
            success: function(data) {
                for (const appointment of data) {
                    if (appointment['appointment_time'] === fieldsetData['datetime']) {
                        alert('The appointment time is not available. Please choose another time or select another doctor.');
                        valid = false;
                        break;
                    }
                }
            },
            error: function(error) {
                alert('An error occurred while checking the availability of the appointment time.');
            }
        });
        if (!valid) {
            event.preventDefault();
            event.stopPropagation();
            return;
        }

        Object.assign(formData, fieldsetData);

        $.ajax({
            type: 'POST',
            url: '/api/v1/appointments',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            data: JSON.stringify(formData),
            success: function() {
                alert('Appointment has been successfully booked.');
                window.location.href = '/receptionist/dashboard';
            },
            error: function() {
                alert('An error occurred while booking the appointment.');
            }
        });

    });

    $(".next").click(function(event){
        const fieldsetData = {};
        if (fieldsets[current_fs].classList.contains('search-form')) {
            const patientsList = document.querySelectorAll('.form-check-input');
            if (typeof patientsList !== 'undefined' && patientsList !== null) {
                const patientID = getPatientID(patientsList);
                if (typeof patientID !== 'undefined' && patientID !== null) {
                    fieldsetData['patient_id'] = patientID;
                    for (let i = 1; i < 3; i++) {
                        fieldsets[i].classList.add('skipped');
                        $("#progressbar li").eq(i).addClass("active");
                    }
                }
            }
        } else {
            const fields = $(fieldsets[current_fs])[0].querySelectorAll('input, select, textarea');
            var valid = true;
            var fieldsValue = {};
            fields.forEach((field) => {
                if (field.type === 'button' || field.type === 'submit') {
                    return;
                }
                if (!(current_fs === 1 || current_fs === 2) || patientAttributes.includes(field.name)) {
                    fieldsValue[field.name] = field.value;
                }
                removeFeedback(field);
                if (!field.checkValidity()) {
                    createInvalidFeedback(field, field.validationMessage);
                    valid = false;
                } else {
                    createValidFeedback(field);
                }

            });

            fieldsets[current_fs].classList.add('was-validated');
            if (!valid) {
                event.preventDefault();
                event.stopPropagation();
                return;
            }

            if (current_fs === 1 || current_fs === 2) {
                Object.assign(newPatientData, fieldsValue);
                if (current_fs === 2) {
                    $.ajax({
                        type: 'POST',
                        url: '/api/v1/patients',
                        contentType: 'application/json; charset=utf-8',
                        dataType: 'json',
                        data: JSON.stringify(newPatientData),
                        success: function(data) {
                            fieldsetData['patient_id'] = data['id'];
                        },
                        error: function(error) {
                            alert('An error occurred while creating a new account.');
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

        previous_fs = current_fs;
        current_fs += 1;

        while (fieldsets[current_fs].classList.contains('skipped') && current_fs < fieldsets.length - 1) {
            current_fs += 1;
        }
        next_fs = current_fs + 1;

        //Add Class Active
        $("#progressbar li").eq(current_fs).addClass("active");
        
        //show the next fieldset
        $(fieldsets[current_fs]).show();
        if (current_fs === 4) {
            all_doctors_working_hours = loadDepartments();
        }
        //hide the current fieldset with style
        $(fieldsets[previous_fs]).animate({opacity: 0}, {
            step: function(now) {
                // for making fielset appear animation
                opacity = 1 - now;
    
                $(fieldsets[previous_fs]).css({
                    'display': 'none',
                    'position': 'relative'
                });
                $(fieldsets[current_fs]).css({'opacity': opacity});
            }, 
            duration: 600
        });
    });
    
    $(".previous").click(function(){
        next_fs = current_fs;
        current_fs -= 1;

        while (fieldsets[current_fs].classList.contains('skipped') && current_fs > 0) {
            fieldsets[current_fs].classList.remove('skipped');
            $("#progressbar li").eq(current_fs).removeClass("active");
            current_fs -= 1;
        }
        previous_fs = current_fs - 1;
        
        //Remove class active
        $("#progressbar li").eq(next_fs).removeClass("active");
        
        //show the previous fieldset
        $(fieldsets[current_fs]).show();
    
        //hide the current fieldset with style
        $(fieldsets[next_fs]).animate({opacity: 0}, {
            step: function(now) {
                // for making fielset appear animation
                opacity = 1 - now;
    
                $(fieldsets[next_fs]).css({
                    'display': 'none',
                    'position': 'relative'
                });
                $(fieldsets[current_fs]).css({'opacity': opacity});
            }, 
            duration: 600
        });
    });
});

function getPatientID(patientsList) {
    for (let i = 0; i < patientsList.length; i++) {
        if (patientsList[i].checked) {
            return patientsList[i].value;
        }
    }
    return null;
}

function removeFeedback(field) {
    field.classList.remove('is-invalid');
    field.classList.remove('is-valid');
    const inputFormat = $(field).parent()[0].querySelector('#input-format');
    if (inputFormat !== null) {
        inputFormat.classList.add('visually-hidden');
    }
    const feedback = field.parentNode.querySelector('.invalid-feedback');
    if (feedback !== null) {
        feedback.remove();
    }
}

function createInvalidFeedback(field, message) {
    field.classList.add('is-invalid');
    const inputFormat = $(field).parent()[0].querySelector('#input-format');
    if (inputFormat !== null) {
        inputFormat.classList.remove('visually-hidden');
    }
    const feedback = document.createElement('div');
    feedback.classList.add('invalid-feedback');
    feedback.innerHTML = message;
    field.parentNode.appendChild(feedback);
}

function createValidFeedback(field) {
    field.classList.add('is-valid');
}
