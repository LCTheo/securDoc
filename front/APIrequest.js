// Create a request variable and assign a new XMLHttpRequest object to it.

function Download(){
    var request = new XMLHttpRequest();

// Open a new connection, using the GET request on the URL endpoint
    request.open('GET', 'http://localhost:5000/rsc/test3?token=\'test\'', true);

    request.onload = function() {
        var data = JSON.parse(this.response);
        document.getElementById("container_form").innerHTML += data;
        //alert(data);
    }

// Send request
    request.send()
}

function Upload(){

    var fd = new FormData();
    fd.append('file', document.forms['fileinfo']['myfile'].files[0] /*, optional filename */)

    var req = $.ajax({
        url: 'http://localhost:5000/rsc/test3?token=\'test\'',
        method: 'POST',
        data: fd,
        processData: false, // don't let jquery process the data
        contentType: false, // let xhr set the content type
        success: [function(){
            alert('File Uploaded');
        }]
    });

    req.then(function(response) {
        console.log(response)
    }, function(xhr) {
        console.error('failed to fetch xhr', xhr)
    })

}

function Inscription(){
    //fd.append('id', document.forms['form_inscription']['uname'].files[0]);
    //fd.append('password', document.forms['form_inscription']['psw'].files[0]);

    var data = {
      id: document.getElementById('uname').value,
      password: document.getElementById('password').value,
    }

    var req = $.ajax({
        url: 'http://localhost:5001/users/',
        type: 'POST',
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: "json",
        success: [function(){
            alert('User Created');
        }]
    });

    req.then(function(response) {
        console.log(response)
    }, function(xhr) {
        console.error('failed to fetch xhr', xhr)
    })
}
