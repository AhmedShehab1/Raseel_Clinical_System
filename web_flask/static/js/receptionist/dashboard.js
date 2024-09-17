$(document).ready(function () {
    const tableType = document.getElementById('table-type');

    if(typeof localStorage.getItem('tableSelected') === 'undefined' || localStorage.getItem('tableSelected') === null) {
        localStorage.setItem('tableSelected', 'today-appointments');
    } else {
        tableType.value = localStorage.getItem('tableSelected');
        tableTypeChanged(tableType);
    }

    tableType.addEventListener('change', () => {tableTypeChanged(tableType);});

    $('.book-appointment').click(function () {
        window.location.href = '/receptionist/book-appointment';
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
});

function tableTypeChanged(tableTypeElement) {
    const tableSelected = String(tableTypeElement.value);
    const tableBodiesList = $('.table_body').toArray();
    var tableElement, tableBodyElement;

    localStorage.setItem('tableSelected', tableSelected);

    tableBodiesList.forEach(tableBody => {
        if (String(tableBody.id) === tableSelected) {
            tableElement = tableBody.parentElement;
            tableBodyElement = tableBody;
            tableBody.style = "";
        }
        else {
            tableBody.parentElement.style = "display:none;";
            tableBody.style = "display:none;";
        }
    });

    checkMembersCount(tableElement, $(tableBodyElement)[0].childElementCount);
}
