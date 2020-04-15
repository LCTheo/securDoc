// Create a request variable and assign a new XMLHttpRequest object to it.

function Download(){
    var request = new XMLHttpRequest();
    let user = localStorage.getItem('username');
    let token = localStorage.getItem('token');
// Open a new connection, using the GET request on the URL endpoint
    request.open('GET', 'http://localhost:5000/rsc/'+user+'?token='+token, true);

    request.onload = function() {
        var data = JSON.parse(this.response);
        alert()
        i = 0
        while(data["response"].length > i){
            document.getElementById("container_form").innerHTML += "<br><a href=\"http://localhost:5000/rsc/"+user+"/"+data["response"][i]+"?token="+token+"\" download>"+data["response"][i]+"</a>"
            i++
        }

        var blob = new Blob([request.response], { type: 'file' });
        var link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = this.response;

        document.body.appendChild(link);
      }
// Send request
    request.send()
}

function Upload(){
      let user = localStorage.getItem('username');
      let token = localStorage.getItem('token');
    var fd = new FormData();
    fd.append('file', document.forms['fileinfo']['myfile'].files[0] /*, optional filename */)

    var req = $.ajax({
        url: 'http://localhost:5000/rsc/'+user+'?token='+token,
        method: 'POST',
        data: fd,
        processData: false, // don't let jquery process the data
        contentType: false, // let xhr set the content type
        success: [function(){
            alert('File Uploaded');
        }],
        error: [function () {
            alert('Error with the upload of the file');
        }]
    });

    req.then(function(response) {
        console.log(response)
    }, function(xhr) {
        console.error('failed to fetch xhr', xhr)
    })

}

function Registration(){
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
        }],
        error: [function () {
            alert('Error on user creation');
        }]
    });

    req.then(function(response) {
        console.log(response)
    }, function(xhr) {
        console.error('failed to fetch xhr', xhr)
    })
}

function Connection(){

    let data = $("form").serialize()

    var req = $.ajax({
        url: 'http://localhost:5001/users/',
        type:'GET',
        data: data,
        success: [function(){
            alert('User Connected');
            window.location.reload(false);
        }],
        error: [function () {
            alert('Error on user connection');
        }]
    });

    req.then(function(response) {
        regex = /b'(?<token>.+)'/gm;
        while ((m = regex.exec(response["response"].toString())) !== null) {
    // This is necessary to avoid infinite loops with zero-width matches
    if (m.index === regex.lastIndex) {
        regex.lastIndex++;
    }
    newtoken = m[1]
}
        localStorage.setItem('token', newtoken);
        localStorage.setItem('username', document.getElementById('id').value);
    }, function(xhr) {
        console.error('failed to fetch xhr', xhr)
    })
}

function Disconnection() {
    localStorage.clear();
    window.location.reload(false);
}
