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

    $('.delete_appointment').click((event) => {
        const appointmentId = $(event.target).attr('data-id');
        deleteAppointment(appointmentId);
    });
});

function tableTypeChanged(tableTypeElement) {
    const tableSelected = String(tableTypeElement.value);
    const tableBodiesList = $('.table_body').toArray();

    localStorage.setItem('tableSelected', tableSelected);

    const selectedBody = getSelectedBody(tableBodiesList, tableSelected);
    const tableElement = selectedBody.parentElement;

    checkMembersCount(tableElement, $(selectedBody)[0].childElementCount);
}
