document.addEventListener("DOMContentLoaded", (e) => {

    let btns_carga = document.getElementsByTagName('button');
    
    for(let i=0; i < btns_carga.length; i++){
        if(btns_carga[i].hasAttribute('menu')){
            btns_carga[i].addEventListener('click', (e) => {
                let menu = btns_carga[i].getAttribute('menu');
                let cmd = btns_carga[i].getAttribute('cmd');
                let name = btns_carga[i].getAttribute('id');
                name = name.slice(0, name.indexOf('OnOff'));
                sendCommand(cmd, menu, name);
            });
        }
    }
});


function sendCommand(cmd, menu, name){
    let url = "http://localhost:8000/control/manual/neummatica/";
    let params = "command=" + cmd + "&menu=" + menu + "&name=" + name;

    // var params = "lorem=ipsum&name=alpha";
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params);
}