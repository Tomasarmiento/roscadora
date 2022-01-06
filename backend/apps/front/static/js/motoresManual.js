document.addEventListener("DOMContentLoaded", (e) => {
    
    let btn = document.getElementById('absMoveV');

    btn.addEventListener("click", (e) => {
        let rpm = document.getElementById('absPosV').value;
        sendCommand(btn.getAttribute('cmd'), {'ref': parseFloat(rpm)});
    })
});


function sendCommand(cmd, args){
    let url = "http://localhost:8000/control/";
    let params = "command=" + cmd;
    // var params = "lorem=ipsum&name=alpha";
    let xhr = new XMLHttpRequest();
    Object.entries(args).forEach(([key, value]) => {
        params += "&" + key + "=" + value;
    });
    xhr.open("POST", url, true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params);
}