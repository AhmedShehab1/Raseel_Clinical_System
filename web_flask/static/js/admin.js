$(document).ready(function () {

  $('.delete-member').click(function () {
    const staffMemberId = $(this).attr('data-id');
    const button = $(this);

    if (confirm('Are you sure you want to delete this member?')) {
      $.ajax({
        url: `/api/v1/staff-members/${staffMemberId}`,
        type: 'DELETE',
        contentType: 'application/json',
        success: function () {
          button.closest('.member-item').remove();
          alert('member deleted successfully.');
        },
        error: function () {
          alert('Failed to delete the member, Please try again.');
        }
      });
    }
  });

  function handleSubmitForm(url, type, formData, successMessage) {
    $.ajax({
        url: url,
        type: type,
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function () {
            alert(successMessage);
            $('.modal').modal('hide');
            $('.needs-validation').removeClass('was-validated').trigger('reset');
        },
        error: function (xhr) {
            const response = xhr.responseJSON;
            if (response.errors) {
                for (const [field, errorMsg] of Object.entries(response.errors)) {
                    let fieldElement = $(`[name="${field}"]`);
                    fieldElement.removeClass('is-valid').addClass('is-invalid');

                    let feedbackElement = fieldElement.next('.invalid-feedback')
                    if (feedbackElement.length === 0) {
                        feedbackElement = "<div class='invalid-feedback'></div>"
                        fieldElement.after(feedbackElement);
                    }
                    feedbackElement.text(errorMsg).show();
                }
            } else {
                alert('Failed to process your request, Please try again.');
            }
        }
    });
  }

  function updateModalFields(modal, member) {
    modal.find('input[name="name"]').val(member.name);
    modal.find('input[name="email"]').val(member.email);
    modal.find('input[name="phone"]').val(member.phone);
    modal.find('input[name="role"]').val(member.__class__);
    modal.find('input[name="department"]').val(member.department);
    toggleDoctorFields(member.__class__, member.certificates, member.department);
    }

    function toggleDoctorFields(role, certificates = '', department = '') {
        if (role === 'Doctor') {
            $('.doctor-fields').show();
            $('#new-certificates, #edit-certificates').val(certificates).attr('required', true);
            $('#new-department, #edit-department').val(department).attr('required', true);
        } else {
            $('.doctor-fields').hide();
            $('#new-certificates, #edit-certificates').val('').removeAttr('required');
            $('#new-department, #edit-department').val('').removeAttr('required');
        }
    }

    $('#roleSelect').change(function () {
        toggleDoctorFields($(this).val());
    });


  $('.edit-member').click(function () {
    const staffMemberId = $(this).attr('data-id');
    const modal = $('#editModal');
    $('#editModal').find('.needs-validation').data('url', `/api/v1/staff-members/${staffMemberId}`);

    $.ajax({
      url: `/api/v1/staff-members/${staffMemberId}`,
      type: 'GET',
      contentType: 'application/json',
      success: function (data) {
        updateModalFields(modal, data);
      },
      error: function () {
        alert('Failed to fetch member details, Please try again.');
      }
    });
 });

    $('.needs-validation').off('submit').on('submit', function (event) {
        event.preventDefault();
        const form = $(this);
        const formData = {
            name: form.find('input[name="name"]').val(),
            email: form.find('input[name="email"]').val(),
            phone: form.find('input[name="phone"]').val(),
            password: form.find('input[name="password"]').val(),
            certificates: form.find('textarea[name="certificates"]').val(),
            department: form.find('input[name="department"]').val(),
            role: form.find('select[name="role"]').val() || form.find('input[name="role"]').val(),
        };

      const phoneField = $('#edit-phone');
      if (phoneField.val() && !phoneField[0].checkValidity()) {
        phoneField.addClass('is-invalid');
      } else {
        phoneField.removeClass('is-invalid');
      }

      if (!this.checkValidity()) {
        event.stopPropagation();
        form.addClass('was-validated');
        return;
      }

      const url = form.data('url');
      const type = form.data('method');
      const successMessage = form.data('success-message');
      handleSubmitForm(url, type, formData, successMessage);
    });

    $('.modal').on('hidden.bs.modal', function () {
        $('.needs-validation').removeClass('was-validated').trigger('reset');
    });
});
