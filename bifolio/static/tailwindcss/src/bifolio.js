const serialize_form = form => JSON.stringify(
    Array.from(new FormData(form).entries())
        .reduce((m, [key, value]) => Object.assign(m, {[key]: value}), {})
);

function make_transaction(data, url) {
    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        data: data,
        contentType: 'application/json'
    }).done(function(data) {
        window.location = window.location;
    }).fail(function() {
        alert("Sorry. Server unavailable. ");
    });
}
