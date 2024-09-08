$(document).ready(function(){
    var fieldsets = $('fieldset');
    console.log(fieldsets);
    var current_fs = 0, previous_fs = -1, next_fs = 1; //fieldsets
    var opacity;

    $(".skip").click(function(){
        // Make all the values in the fieldset empty => ""
    });

    $(".submit").click(function(){
        //Check required fields
        var requiredFields = $(fieldsets[current_fs]).find('.required');
        if (!isRequiredFieldsValid(current_fs)) {
            return;
        }

        const name = $('#inputFullName').val();
        const email = $('#inputemail').val();
    });

    $(".next").click(function(){
        //Check required fields
        var requiredFields = $(fieldsets[current_fs]).find('.required');
        if (!isRequiredFieldsValid(requiredFields)) {
            return;
        }

        previous_fs = current_fs;
        if (fieldsets[next_fs].classList.contains('skipped')) {
            current_fs = next_fs + 1;
            while (fieldsets[current_fs].classList.contains('skipped') && current_fs < fieldsets.length - 1) {
                current_fs += 1;
            }
        } else {
            current_fs = next_fs;
        }
        next_fs = current_fs + 1;
        //Add Class Active
        $("#progressbar li").eq($("fieldset").index($(fieldsets[current_fs]))).addClass("active");
        
        //show the next fieldset
        $(fieldsets[current_fs]).show();
        if (current_fs === 4) {
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
    });
    
    $(".previous").click(function(){
        next_fs = current_fs;
        if (fieldsets[previous_fs].classList.contains('skipped')) {
            current_fs = previous_fs - 1;
            while (fieldsets[current_fs].classList.contains('skipped') && current_fs > 0) {
                current_fs -= 1;
            }
        } else {
            current_fs = previous_fs;
        }
        previous_fs = current_fs - 1;
        console.log(current_fs);
        console.log($(fieldsets[current_fs]));
        
        //Remove class active
        $("#progressbar li").eq($("fieldset").index($(fieldsets[next_fs]))).removeClass("active");
        
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

function isRequiredFieldsValid(requiredFields) {
    var valid = true;

    for (let i = 0; i < requiredFields.length; i++) {
        const field = $(requiredFields[i]);
        if (validateNullValue(field) === false || validateCustomFields(field) === false) {
            field.css('border-color', 'red');
            field.addClass('is-invalid');
            valid = false;
        } else {
            field.css('border-color', 'gray');
            removeInvalidFeedback(field);
            field.removeClass('is-invalid');
        }
    }
    if (!valid) {
        return false;
    }
}

function validateCustomFields(field) {
    var fieldType = field.attr('type');

    if (fieldType === 'email') {
        return validateEmail(field.val());
    } else if (fieldType === 'datetime-local') {
        return validateDateTime(field);
    } else if (fieldType === 'password') {
        return field.attr('id') === 'inputPassword' ? validatePassword(field.val()) : validateConfirmPassword(field.val());
    } else if (fieldType === 'date') {
        return field.attr('id') === 'inputBirthDate' ? validateBirthDate(field.val()) : validateDate(field.val());
    } else if (fieldType === 'tel' || fieldType === 'number') {
        return field.attr('id') === 'inputPhone' ? validateContactNumber(field.val()) : validateNationalId(field.val());
    } else {
        return true;
    }
}

function validateNullValue(field) {
    if (field.val() === '') {
        createInvalidFeedback(field, 'Please fill out this field.');
        return false;
    }

    return true;
}

function validateEmail(email) {
    var regex = /^\S+@\S+\.\S+$/;

    if (regex.test(email) === false) {
        createInvalidFeedback($('#inputEmail'), 'Please enter a valid email address.');
        return false;
    }

    return true;
}

function validateDateTime(dateTime) {
    if (new Date(dateTime.val()) < new Date()) {
        createInvalidFeedback($('#inputDateTime'), 'Date must be in the future.');
        return false;
    }

    return true;
}

function validatePassword(password) {
    var regex = /^(?:(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^\da-zA-Z]).{8,})$/;

    if (regex.test(password) === false) {
        createInvalidFeedback($('#inputPassword'),
        'Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character, and be at least 8 characters long.');
        return false;
    }

    return true;
}

function validateConfirmPassword(confirmPassword) {
    var password = $('#inputPassword').val();

    if (confirmPassword !== password) {
        createInvalidFeedback($('#inputConfirmPassword'), 'Passwords do not match.');
        return false;
    }

    return true;
}

function validateBirthDate(birthDate) {
    if (new Date(birthDate) > new Date()) {
        createInvalidFeedback($('#inputBirthDate'), 'Date must be in the past.');
        return false;
    }

    return true;
}

function validateDate(date) {
    if (new Date(date) < new Date()) {
        createInvalidFeedback($('#inputDate'), 'Date must be in the future.');
        return false;
    }

    return true;
}

function validateContactNumber(contactNumber) {
    var regex = /^05[0-9]{8}$/;

    if (regex.test(contactNumber) === false) {
        createInvalidFeedback($('#inputPhone'), 'Please enter a valid contact number 05########.');
        return false;
    }

    return true;
}

function validateNationalId(nationalID) {
    var regex = /^22[0-9]{8}$/;

    if (regex.test(nationalID) === false) {
        createInvalidFeedback($('#inputNationalID'), 'Please enter a valid national ID 22########.');
        return false;
    }

    return true;
}

function createInvalidFeedback(field, message) {
    var subMessage = field.parent().find('.invalid-feedback');
    subMessage.text(message);
}
function removeInvalidFeedback(field) {
    var subMessage = field.parent().find('.invalid-feedback');
    subMessage.text('');
}
