$(document).ready(function () {
    const appointments = document.getElementById('appointments');
    const appointmentStatus = document.getElementById('appointment-status');
    checkAppointmentsCount($('.table_body')[0].childElementCount);

    $('.book-appointment').click(function () {
        window.location.href = '/patient/book-appointment';
    });

    $('.delete_appointment').click(function () {
        const appointmentId = $(this).attr('data-id');

        if (confirm('Are you sure you want to delete this appointment?')) {
            $.ajax({
                url: `/api/v1/appointments/${appointmentId}`,
                type: 'DELETE',
                contentType: 'application/json',
                success: function () {
                    alert('Appointment deleted successfully.');
                    window.location.reload();
                },
                error: function () {
                    alert('Failed to delete the appointment, Please try again.');
                    window.location.reload();
                }
            });
        }
    });

    $('restore-appointment').click(function () {
        const appointmentId = $(this).attr('data-id');

        if (confirm('Are you sure you want to delete this appointment?')) {
            $.ajax({
                url: `/api/v1/appointments/${appointmentId}`,
                type: 'PUT',
                contentType: 'application/json',
                success: function () {
                    alert('Appointment restored successfully.');
                    window.location.reload();
                },
                error: function () {
                    alert('Failed to delete the appointment, Please try again.');
                    window.location.reload();
                }
            });
        }
    });

    appointmentStatus.addEventListener('change', function () {
        const status = String(appointmentStatus.value) + "-table-body";
        const tableBodiesList = $('.table_body').toArray();

        tableBodiesList.forEach(element => {
            if (String(element.id) === status) {
                element.style = "";
                checkAppointmentsCount($(element)[0].childElementCount);
            }
            else {
                element.style = "display:none;";
            }
        });
    });

    function checkAppointmentsCount(no_of_appointment) {
        const appointmentsTable = $('.table')[0];
        const noAppointmentsDiv = document.getElementById('no-appointments-found');
        const noAppointmentsLabel = document.getElementById('no-appointments-found-label');

        if (no_of_appointment === 0) {
            if (!noAppointmentsDiv && !noAppointmentsLabel) {
                const noAppointmentsLabel = document.createElement('p');
                const noAppointmentsDiv = document.createElement('div');
                const noAppointmentsImage = document.createElement('img');

                appointmentsTable.style = "display:none;";

                noAppointmentsLabel.className = 'text-center';
                noAppointmentsLabel.style = "font-size:20px; font-weight:bold;";
                noAppointmentsLabel.innerHTML = 'You have no appointments currently.';
                noAppointmentsLabel.id = 'no-appointments-found-label';
                appointments.appendChild(noAppointmentsLabel);

                noAppointmentsImage.src = '../static/images/search_no_results.png';
                noAppointmentsImage.width = '400';
                noAppointmentsDiv.appendChild(noAppointmentsImage);

                noAppointmentsDiv.id = 'no-appointments-found';
                noAppointmentsDiv.className = 'd-flex justify-content-center';
                appointments.appendChild(noAppointmentsDiv);
            }
        } else {
            appointmentsTable.style = "";
            if (noAppointmentsLabel) {appointments.removeChild(noAppointmentsLabel);}
            if (noAppointmentsDiv) {appointments.removeChild(noAppointmentsDiv);}
        }
    }
});
