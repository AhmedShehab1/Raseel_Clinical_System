function flask_moment_render(elem) {
    const timestamp = moment(elem.dataset.timestamp);
    const func = elem.dataset.function;
    const format = elem.dataset.format;
    const timestamp2 = elem.dataset.timestamp2;
    const no_suffix = elem.dataset.nosuffix;
    const units = elem.dataset.units;
    let args = [];
    if (format)
        args.push(format);
    if (timestamp2)
        args.push(moment(timestamp2));
    if (no_suffix)
        args.push(no_suffix);
    if (units)
        args.push(units);
    elem.textContent = timestamp[func].apply(timestamp, args);
    elem.classList.remove('flask-moment');
    elem.style.display = "";
}

function flask_moment_render_all() {
    const moments = document.querySelectorAll('.flask-moment');
    moments.forEach(function(moment) {
        flask_moment_render(moment);
        const interval = moment.dataset.refresh;
        if (interval && interval > 0) {

            setInterval((momentElement) => {
                if (momentElement.parentElement.id === "current-time") {
                    const timestamp = new Date();
                    momentElement.dataset.timestamp = timestamp.toISOString();
                }
                flask_moment_render(momentElement);
            }, 1000, arg0=moment);
        }
    })
}

document.addEventListener("DOMContentLoaded", flask_moment_render_all);

function checkMembersCount(membersTable, no_of_members) {
    const members = document.getElementById('members');
    const noMembersDiv = document.getElementById('no-members-found');
    const noMembersLabel = document.getElementById('no-members-found-label');

    if (no_of_members === 0) {
        if (!noMembersDiv && !noMembersLabel) {
            const noMembersLabel = document.createElement('p');
            const noMembersDiv = document.createElement('div');
            const noMembersImage = document.createElement('img');

            membersTable.style = "display:none;";

            noMembersLabel.className = 'text-center';
            noMembersLabel.style = "font-size:20px; font-weight:bold;";
            noMembersLabel.innerHTML = 'No results.';
            noMembersLabel.id = 'no-members-found-label';
            members.appendChild(noMembersLabel);

            noMembersImage.src = '../static/images/search_no_results.png';
            noMembersImage.width = '400';
            noMembersDiv.appendChild(noMembersImage);

            noMembersDiv.id = 'no-members-found';
            noMembersDiv.className = 'd-flex justify-content-center';
            members.appendChild(noMembersDiv);
        }
    } else {
        membersTable.style = "";
        if (noMembersLabel) {members.removeChild(noMembersLabel);}
        if (noMembersDiv) {members.removeChild(noMembersDiv);}
    }
}

function deleteAppointment(appointmentId) {
    swal({
        title: "Are you sure?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    }).then((willDelete) => {
        if (willDelete) {
            $.ajax({
                url: `/api/v1/appointments/${appointmentId}`,
                type: 'DELETE',
                contentType: 'application/json',
                success: function () {
                    swal({
                        title: 'Done',
                        text: 'Appointment deleted successfully.',
                        icon: 'success',
                        button: 'Ok',
                    }).then((value) => {
                        if (value) {
                            window.location.reload();
                        }
                    });
                },
                error: function (err) {
                    swal({
                        title: 'Error',
                        text: err.responseJSON.message,
                        icon: 'error',
                        button: 'Ok',
                    }).then((value) => {
                        if (value) {
                            window.location.reload();
                        }
                    });
                }
            });
        }
    });
}

function getSelectedBody(bodiesList, selectedId) {
    var selectedBody;

    bodiesList.forEach(body => {
        if (String(body.id) === selectedId) {
            selectedBody = body;
            body.style = "";
        }
        else {
            body.parentElement.style = "display:none;";
            body.style = "display:none;";
        }
    });

    return selectedBody;
}
