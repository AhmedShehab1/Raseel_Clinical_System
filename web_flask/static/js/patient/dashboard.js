$(document).ready(function () {
    const appointmentStatus = document.getElementById('appointment-status');
    checkMembersCount($('.table_body')[0].childElementCount);

    $('.book-appointment').click(function () {
        window.location.href = '/patient/book-appointment';
    });

    $('.delete_appointment').click((event) => {
        const appointmentId = $(event.target).attr('data-id');
        deleteAppointment(appointmentId);
    });

    $('.restore-appointment').click(function () {
        const appointmentId = $(this).attr('data-id');

        if (confirm('Are you sure you want to delete this appointment?')) {
            $.ajax({
                url: `/api/v1/appointments/2/${appointmentId}`,
                type: 'PUT',
                contentType: 'application/json',
                success: function () {
                    window.location.reload();
                },
                error: function () {
                    window.location.reload();
                }
            });
        }
    });

    appointmentStatus.addEventListener('change', function () {
        const status = String(appointmentStatus.value) + "-table-body";
        const tableBodiesList = $('.table_body').toArray();
        const selectedBody = getSelectedBody(tableBodiesList, status);
        const tableElement = selectedBody.parentElement;

        checkMembersCount(tableElement, $(selectedBody)[0].childElementCount);
    });
});
