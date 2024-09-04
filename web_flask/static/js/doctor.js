$(document).ready(function () {
    $(".delete_appointment").click(function() {
        let appointment_id = $(this).attr('data-id');
        let button = $(this);

        if (confirm('Are you sure you want to delete this appointment?')) {
            $.ajax({
                url: `/api/v1/appointments/${appointment_id}`,
                type: 'DELETE',
                contentType: 'application/json',
                success: function() {
                    button.closest('.appointment-item').remove();
                    alert('Appointment deleted successfully.');
                },
                error: function() {
                    alert('Failed to delete the appointment, Please try again.');
                }
            })
        }
    });
});
