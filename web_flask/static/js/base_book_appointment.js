const formData = new Object();
var fieldsets;
var current_fs, previous_fs, next_fs; //fieldsets indexes
var create_account_index, personal_info_index, appointment_info_index, vitals_index, allergies_index;
var opacity;
var all_doctors_working_hours = new Object();
const all_doctors = new Object();
const appointmentAttributes = ['doctor_id', 'patient_id', 'appointment_time', 'reason'];

$(document).ready(function(){
    fieldsets = $("fieldset");
    current_fs = 0, previous_fs = fieldsets.length - 1, next_fs = 1;
    create_account_index = $('#progressbar li').index($('#create_account'));
    personal_info_index = $('#progressbar li').index($('#personal_info'));
    appointment_info_index = $('#progressbar li').index($('#appointment_info'));
    vitals_index = $('#progressbar li').index($('#vitals'));
    allergies_index = $('#progressbar li').index($('#allergies'));
    localStorage.setItem('allergy_count', 1);

    $("form").bind("keypress", function (event) {
        if (event.keyCode === 13) {
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
        displayNextStep();
    });

    $(".submit").click(function(event){
        const fieldsetData = new Object();
        const fields = $(fieldsets[current_fs])[0].querySelectorAll('input, select, textarea');
        var valid = true;

        const fieldsValue = getFieldsValue(fields, attr=appointmentAttributes);
        if (!fieldsValue) {
            event.preventDefault();
            event.stopPropagation();
            return;
        }
        
        Object.assign(fieldsetData, fieldsValue);
        const date = fieldsetData['appointment_time'].split('T')[0];
        const time = fieldsetData['appointment_time'].split('T')[1];
        const hour = time.split(':')[0];
        const minutes = time.split(':')[1];
        if (parseInt(minutes) < 30) {
            fieldsetData['appointment_time'] = date + 'T' + hour + ':' + '00';
        } else {
            fieldsetData['appointment_time'] = date + 'T' + hour + ':' + '30';
        }

        const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
        const appointmentDate = new Date(fieldsetData['appointment_time']);
        const appointmentDay = weekday[appointmentDate.getDay()];
        const doctorID = fieldsetData['doctor_id'];
        const doctorWorkingHours = all_doctors_working_hours[doctorID];

        if (typeof doctorWorkingHours !== 'undefined') {
            doctorWorkingHours.forEach((workingHour) => {
                if (workingHour['day'] === appointmentDay) {
                    const startHour = parseInt(workingHour['start_hour'].split(':')[0]);
                    const startMinutes = parseInt(workingHour['start_hour'].split(':')[1]) + (startHour * 60);

                    const endHour = parseInt(workingHour['end_hour'].split(':')[0]);
                    const endMinutes = parseInt(workingHour['end_hour'].split(':')[1]) + (endHour * 60);

                    const appointmentMinutes = parseInt(hour) * 60 + parseInt(minutes);
                    if (appointmentMinutes < startMinutes || appointmentMinutes > endMinutes) {
                        const dateTimeField = $('input[name=appointment_time]')[0];
                        createInvalidFeedback(dateTimeField, 'Doctor is not available at this time.');
                        valid = false;
                    }
                }
            });
        }

        if (!valid) {
            event.preventDefault();
            event.stopPropagation();
            return;
        }

        Object.assign(formData, fieldsetData);
        formData['status'] = 'scheduled';

        submitForm(formData);
    });

    $(".previous").click(() => {
        const fields = $(fieldsets[current_fs])[0].querySelectorAll('input, select, textarea');
        resetFieldsValue(fields);
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

    $("#inputHeightCM")[0].addEventListener("input", function() {
        const heightCM = parseFloat($(this).val());
        if (isNaN(heightCM)) {
            return;
        }
        const heightIn = heightCM / 2.54;
        const heightInField = $('#inputHeightIn')[0];

        heightInField.value = heightIn.toFixed(2);
    });

    $("#inputWeightKg")[0].addEventListener("input", function() {
        const weightKg = parseFloat($(this).val());
        if (isNaN(weightKg)) {
            return;
        }
        const weightLBS = parseFloat(weightKg / 2.204623);
        const weightLBSField = $('#inputWeightLBS')[0];

        weightLBSField.value = weightLBS.toFixed(2);
    });

    $("#inputHeightIn")[0].addEventListener("input", function() {
        const heightIn = parseFloat($(this).val());
        if (isNaN(heightIn)) {
            return;
        }
        const heightCM = heightIn * 2.54;
        const heightCMField = $('#inputHeightCM')[0];

        heightCMField.value = heightCM.toFixed(2);
    });

    $("#inputWeightLBS")[0].addEventListener("input", function() {
        const weightLBS = parseFloat($(this).val());
        if (isNaN(weightLBS)) {
            return;
        }
        const weightKg = parseFloat(weightLBS / 2.204623);
        const weightKgField = $('#inputWeightKg')[0];

        weightKgField.value = weightKg.toFixed(2);
    });

    $("#add_allergy").click(function() {
        localStorage.setItem('allergy_count', parseInt(localStorage.getItem('allergy_count')) + 1);

        const newAllergy = document.createElement('div');
        newAllergy.className = 'col-md-12 d-flex align-items-end justify-content-between';
        newAllergy_number = localStorage.getItem('allergy_count');
        newAllergy.id = `allergy_${newAllergy_number}`;

        const allergen_field = createField('Allergen', 'text', newAllergy_number);
        newAllergy.appendChild(allergen_field);

        const reaction_field = createField('Reaction', 'text', newAllergy_number);
        newAllergy.appendChild(reaction_field);

        $('#allergies_group').append(newAllergy);
    });

    $("#remove_allergy").click(function() {
        const allergyNumber = parseInt(localStorage.getItem('allergy_count'));
        if (allergyNumber === 1) {
            swal('You cannot remove the last allergy fields.');
            return;
        }
        const allergyToRemove = document.getElementById(`allergy_${allergyNumber}`);
        allergyToRemove.remove();
        localStorage.setItem('allergy_count', allergyNumber - 1);
    });

    $(".next").click((event) => nextClicked(event));

    $(".continue").click((event) => continueClicked(event));
});

function getPatientID(patientsList) {
    if (typeof patientsList === 'undefined' || patientsList === null) {
        return null;
    }

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
    var inputFormat;


    if (field.id == 'inputHeightCM' || field.id == 'inputHeightIn') {
        inputFormat = document.getElementById('input-Height');
    } else if (field.id == 'inputWeightKg' || field.id == 'inputWeightLBS') {
        inputFormat = document.getElementById('input-Weight');
    } else {
        inputFormat = $(field).parent()[0].querySelector('#input-format');
    }

    if (inputFormat !== null) {
        inputFormat.classList.add('visually-hidden');
    }
    const feedback = field.parentNode.querySelector('.invalid-feedback');
    if (feedback !== null && typeof feedback !== 'undefined') {
        feedback.remove();
    }
}

function createInvalidFeedback(field, message) {
    field.classList.add('is-invalid');
    var inputFormat;
    var appendServerFeedback = true;

    if (field.id == 'inputHeightCM' || field.id == 'inputHeightIn') {
        inputFormat = document.getElementById('input-Height');
        appendServerFeedback = false;
    } else if (field.id == 'inputWeightKg' || field.id == 'inputWeightLBS') {
        inputFormat = document.getElementById('input-Weight');
        appendServerFeedback = false;
    } else {
        inputFormat = $(field).parent()[0].querySelector('#input-format');
    }

    if (inputFormat !== null) {
        inputFormat.classList.remove('visually-hidden');
    }

    if (appendServerFeedback) {
        const feedback = document.createElement('div');
        feedback.classList.add('invalid-feedback');
        feedback.innerHTML = message;
        field.parentNode.appendChild(feedback);
    }
}

function createValidFeedback(field) {
    field.classList.add('is-valid');
}

function getFieldsValue(fields, attr=[]) {
    var fieldsValue = new Object();
    var valid = true;

    fields.forEach((field) => {
        if (field.type === 'button' || field.type === 'submit') {
            return;
        }
        removeFeedback(field);
        if (!field.checkValidity()) {
            createInvalidFeedback(field, field.validationMessage);
            valid = false;
        } else {
            createValidFeedback(field);
            if ((attr.length === 0 ||
                attr.includes(field.name)) &&
                field.id != 'inputHeightIn' &&
                field.id != 'inputWeightLBS'
            ) {
                if (current_fs === allergies_index) {
                    fieldsValue[field.id] = field.value;
                } else {
                    fieldsValue[field.name] = field.value;
                }
            }
        }
    });
    fieldsets[current_fs].classList.add('was-validated');
    if (!valid) {
        return null;
    }
    return fieldsValue;
}

function resetFieldsValue(fields) {
    fields.forEach((field) => {
        if (field.type === 'button' || field.type === 'submit') {
            return;
        }
        delete formData[field.name];
    });
}

function displayNextStep() {
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

    if (current_fs === appointment_info_index) {
        loadDepartments();
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
}

function loadDepartments() {
    const departmentSelect = document.getElementById('inputDepartment');
    const doctorSelect = document.getElementById('inputDoctor');

    var departments;

    $.ajax({
        url: '/api/v1/departments',
        method: 'GET',
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            departments = data.results; // data_departments.results is a list of objects containing all departments
            departments.forEach((department) => {
                let option = document.createElement('option');
                option.setAttribute('value', String(department.id));
                option.setAttribute('label', department.name);
                departmentSelect.appendChild(option);
                all_doctors[String(department.id)] = department.doctors; // department.doctors is a list of objects containing all doctors in the department
            });
        },
        error: function (err) {
            swal({
                title: 'Error',
                text: err.responseJSON.message,
                icon: 'error',
                button: 'Ok',
            });
        }
    });

    departmentSelect.addEventListener("change", (event) => {
        removeFeedback(departmentSelect);
        resetDoctorOptions(doctorSelect);

        const department_id = event.target.value;
        const doctors = all_doctors[department_id];

        if (typeof doctors === "undefined" || doctors.length === 0) {
            if (department_id !== "") {
                createInvalidFeedback(departmentSelect, 'Unfortunately, this department is currently closed.');
            }
            return;
        }

        doctors.forEach((doctor) => {
            let option = document.createElement('option');
            option.setAttribute('value', doctor.id);
            option.setAttribute('label', doctor.name);
            doctorSelect.appendChild(option);
            all_doctors_working_hours[doctor.id] = doctor.working_hours;
        });
    });
}

function resetDoctorOptions(doctorSelectElement) {
    let optionIndex, lenght = doctorSelectElement.options.length - 1;

    for (optionIndex = lenght; optionIndex >= 0; optionIndex--) {
        doctorSelectElement.remove(optionIndex);
    }
    let option = document.createElement('option');
    option.setAttribute('value', '');
    option.setAttribute('label', "Choose a doctor");
    doctorSelectElement.appendChild(option);
    doctorSelectElement.value = '';
}

function createField(label, inputType, index) {
    const field = document.createElement('div');
    const fieldId = label.toLowerCase() + '_' + index;
    field.className = 'col-md-5';
    const fieldLabel = document.createElement('label');
    fieldLabel.className = 'form-label';
    fieldLabel.setAttribute('for', fieldId);
    fieldLabel.innerHTML = label + ' ' + index;
    field.appendChild(fieldLabel);

    const fieldInput = document.createElement('input');
    fieldInput.className = 'form-control';
    fieldInput.setAttribute('type', inputType);
    fieldInput.setAttribute('name', label.toLowerCase());
    fieldInput.setAttribute('id', fieldId);
    field.appendChild(fieldInput);

    return field;
}

/**
 * arrangeAllergies - Arrange allergies data in an objects of allergy objects
 * 
 * @param {Object} data - Allergies data to be arranged
 * 
 * @returns {Object} - Object of allergy objects
 * 
 * @example arrangeAllergies(data) -> {
                                        1: {allergen: 'allergen_1', reaction: 'reaction_1'},
                                        2: {allergen: 'allergen_2', reaction: 'reaction_2'}
                                    }
 */
function arrangeAllergies(data) {
    const allergiesData = new Object();

    for (const fieldId of Object.keys(data)) {
        const allergyData = new Object();
        const fieldName = fieldId.split('_')[0];    // e.g fieldId=allergen_1 => fieldName = 'allergen'
        const fieldIndex = fieldId.split('_')[1];   // e.g fieldId=allergen_1 => fieldIndex = '1'

        if (typeof allergiesData[fieldIndex] === 'undefined') {
            allergiesData[fieldIndex] = new Object();   // this allergy does not exist => make a new object
        }

        allergyData[fieldName] = data[fieldId];
        Object.assign(allergiesData[fieldIndex], allergyData);
    }
    return allergiesData;
}
