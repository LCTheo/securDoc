// change this variable to set the IP where is deployed the project
const dockerIP = "192.168.137.12";


function Download(){
    let request = new XMLHttpRequest();
    let user = localStorage.getItem('username');
    let token = localStorage.getItem('token');
// Open a new connection, using the GET request on the URL endpoint
    request.open('GET', 'https://'+dockerIP+':5000/rsc/'+user+'?token='+token, true);

    request.onload = function() {
        let data = JSON.parse(this.response);
        alert()
        i = 0
        while(data["response"].length > i){
            document.getElementById("container_form").innerHTML += "<br><a href=\"https://"+dockerIP+":5000/rsc/"+user+"/"+data["response"][i]+"?token="+token+"\" download>"+data["response"][i]+"</a>"
            i++
        }

        let blob = new Blob([request.response], { type: 'file' });
        let link = document.createElement('a');
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
    let fd = new FormData();
    fd.append('file', document.forms['fileinfo']['myfile'].files[0] /*, optional filename */)

    let req = $.ajax({
        url: 'https://'+dockerIP+':5000/rsc/'+user+'?token='+token,
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

    let data = {
      id: document.getElementById('uname').value,
      password: document.getElementById('password').value,
    }

    let req = $.ajax({
        url: 'https://'+dockerIP+':5001/users/',
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

    let req = $.ajax({
        url: 'https://'+dockerIP+':5001/users/',
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
        let regex = /b'(?<token>.+)'/gm;
        let m;
        while ((m = regex.exec(response["response"].toString())) !== null) {
            // This is necessary to avoid infinite loops with zero-width matches
            if (m.index === regex.lastIndex) {
                regex.lastIndex++;
            }
        }
        localStorage.setItem('token', m[1]);
        localStorage.setItem('username', document.getElementById('id').value);
    }, function(xhr) {
        console.error('failed to fetch xhr', xhr)
    })
}

function Disconnection() {
    localStorage.clear();
    window.location.reload(false);
}
