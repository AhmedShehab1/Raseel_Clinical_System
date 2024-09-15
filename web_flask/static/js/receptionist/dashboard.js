$(document).ready(function () {

    $('.book-appointment').click(function () {
        window.location.href = '/receptionist/book-appointment';
    });

    if ($('.member-item').length === 0) {
        const tableBody = $('.table_body')[0];
        // const tableType = document.getElementById('inputSearchType'); // when changing the search type to appointments

        $.ajax({
            url: '/api/v1/patients',
            method: 'GET',
            type: 'GET',
            contentType: 'application/json',
            success: function (data) {
                const patients = data.results; // data.results is a list of objects containing all patients
                let count = 1;
                for (let patient of patients) {
                    if (count > 10) {break;}
                    let tr = document.createElement('tr');
                    tr.className = 'member-item';

                    let td1 = document.createElement('td');
                    td1.innerHTML = String(count);
                    tr.appendChild(td1);

                    let td2 = document.createElement('td');
                    td2.innerHTML = String(patient.name);
                    tr.appendChild(td2);

                    let td3 = document.createElement('td');
                    td3.innerHTML = String(patient.email);
                    tr.appendChild(td3);

                    let td4 = document.createElement('td');
                    td4.innerHTML = String(patient.contact_number);
                    tr.appendChild(td4);

                    let td5 = document.createElement('td');
                    let btn = document.createElement('a');
                    btn.className = 'btn btn-warning edit-member';
                    btn.setAttribute('data-bs-toggle', 'modal');
                    btn.setAttribute('data-bs-target', '#editModal'+String(patient.id));
                    btn.setAttribute('data-id', String(patient.id));
                    btn.innerHTML = 'Appointments';
                    td5.appendChild(btn);
                    tr.appendChild(td5);

                    tableBody.appendChild(tr);
                    count += 1;
                }
            },
            error: function(error) {
                const response = error.responseJSON;
                if (response) {alert(response.message);}
            }
        });
    }
});
