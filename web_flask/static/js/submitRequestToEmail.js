$(document).ready(function () {

    const form = $('form');
    const submitBtn = $('#submit-btn');

    function sendData (data) {
        $.ajax({
            url: `/api/v1/sendEmail`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function () {
                swal('Message Sent', 'Your Message has been sent successfully!', 'success');
                submitBtn.prop('disabled', false)
                form.trigger('reset');
            },
            error: function () {
                swal('Error', 'Failed to send your message', 'error')
                submitBtn.prop('disabled', false)
                form.trigger('reset');
            }
        });
    }

    form.off('submit').on('submit', function (event) {
        event.preventDefault();
        submitBtn.prop('disabled', true);
        const formData = {
            name: $('#name').val(),
            email: $('#email').val(),
            phone: $('#phone').val(),
            msg: $('#message').val(),
        };
        sendData(formData);
    });
});