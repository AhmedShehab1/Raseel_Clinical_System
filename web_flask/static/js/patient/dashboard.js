$(document).ready(function () {
    const appointmentStatus = document.getElementById('appointment-status');
    checkMembersCount($('.table_body')[0].childElementCount);

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
                    window.location.reload();
                },
                error: function () {
                    window.location.reload();
                }
            });
        }
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
        var statusBodyElement, statusTable;

        tableBodiesList.forEach(element => {
            if (String(element.id) === status) {
                statusTable = element.parentElement;
                statusBodyElement = element;
                element.style = "";
            }
            else {
                element.parentElement.style = "display:none;";
                element.style = "display:none;";
            }
        });
        checkMembersCount(statusTable, $(statusBodyElement)[0].childElementCount);
    });
});
