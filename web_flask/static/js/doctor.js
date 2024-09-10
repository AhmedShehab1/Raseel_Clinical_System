$(document).ready(function () {
  $('.delete_appointment').click(function () {
    const appointmentId = $(this).attr('data-id');
    const button = $(this);

    if (confirm('Are you sure you want to delete this appointment?')) {
      $.ajax({
        url: `/api/v1/appointments/${appointmentId}`,
        type: 'DELETE',
        contentType: 'application/json',
        success: function () {
          button.closest('.appointment-item').remove();
          alert('Appointment deleted successfully.');
        },
        error: function () {
          alert('Failed to delete the appointment, Please try again.');
        }
      });
    }
  });
  function populateList (listClass, items, searchField) {
    const bulletColors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'black'];

    $(`.${listClass}`).empty();

    items.forEach(item => {
      $(`.${listClass}`).append(`<li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#">
                <span class="d-inline-block bg-${bulletColors[Math.floor(Math.random() * 7)]} rounded-circle p-1"></span>
                ${item}
              </a></li>`);
    });

    $(`.${listClass} li a`).on('click', function () {
      const selectedItem = $(this).text().trim();
      searchField.val(selectedItem);
      $(`.${listClass}`).empty();
    });
  }

  $('.update').click(function () {
    const appointmentId = $(this).attr('data-appointment-id');
    const patientId = $(this).attr('data-patient-id');

    $('.submit-button').click(function () {
      const medicationData = {};
      const diagnosisData = {};
      $('.modal-body').find('input, select').each(function () {
        const val = $(this).val();
        const attribute = $(this).attr('attribute');

        if ((val && attribute) && attribute !== 'name') {
          medicationData[attribute] = val;
        }
        if (attribute === 'name') {
          diagnosisData[attribute] = val;
        }
      });

      const medicationRequest = $.ajax({
        url: `/api/v1/patients/${patientId}/medications`,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(medicationData)
      });

      const diagnosisRequest = $.ajax({
        url: `/api/v1/patients/${patientId}/diagnosises`,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(diagnosisData)
      });

      $.when(diagnosisRequest, medicationRequest).done(function () {
        const generalNote = $('.general-notes-textarea').val();

        if (generalNote) {
          $.ajax({
            url: `/api/v1/appointments/${appointmentId}`,
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify({ notes: generalNote }),
            success: function () {
              alert('All updates were successful');
              $(`#update-modal-${appointmentId}`).modal('hide');
            },
            error: function () {
              alert('Failed to update appointment note.');
            }

          });
        } else {
          alert('All updates were successful');
          $(`#update-modal-${appointmentId}`).modal('hide');
        }
      }).fail(function () {
        alert('Failed to update patient data.');
      });
    });

    $('.drug-search, .diagnosis-search').on('focus', function () {
      const searchField = $(this);

      searchField.off('keydown').on('keydown', function (event) {
        if (event.key === 'Enter') {
          event.preventDefault();

          const searchTerm = searchField.val();
          if (searchTerm) {
            if (searchField.hasClass('drug-search')) {
              $.ajax({
                url: `https://api.fda.gov/drug/ndc.json?search=brand_name:${searchTerm}&limit=10`,
                type: 'GET',
                success: function (data) {
                  const brandNames = data.results.map(drug => drug.brand_name);
                  populateList('medications-list', brandNames, searchField);
                },
                error: function (error) {
                  console.error('Error fetching data:', error);
                }
              });
            } else if (searchField.hasClass('diagnosis-search')) {
              $.ajax({
                url: `https://clinicaltables.nlm.nih.gov/api/conditions/v3/search?terms=${searchTerm}`,
                type: 'GET',
                success: function (data) {
                  const diagnosises = data[3].map(d => d[0]);
                  populateList('diagnosis-list', diagnosises, searchField);
                },
                error: function (error) {
                  console.error('Error fetching data:', error);
                }
              });
            }
          }
        }
      });
    });
  });
});
