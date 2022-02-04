
document.addEventListener("DOMContentLoaded", (e) => {
    let btn_continue = document.getElementById('continue');

    btn_continue.addEventListener('click', (e) => {
        let url = "http://localhost:8000/control/auto/";

        let xhr = new XMLHttpRequest();

        xhr.open("POST", url, true);

        //Send the proper header information along with the request
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        xhr.send();
    });

    
    cuadroDeTextoIndex = document.querySelector("#terminalDeTexto");
    if (sessionStorage.getItem("mensajes") && cuadroDeTextoIndex) {
        console.log('aca');
        let ul = document.getElementById("cuadroMensajes");
        const listaMensajes = sessionStorage.getItem("mensajes").split(",");
        for (let i = 0; i < listaMensajes.length; i++) {
            const li = document.createElement("li");
            li.setAttribute("style", "list-style: none;");
            li.innerHTML = listaMensajes[i];
            ul.appendChild(li);
        }
    }
});
    function InsertarTexto(datosWs) {
        var ul = document.getElementById("cuadroMensajes");
        for (let i = 0; i < datosWs.length; i++) {
        const li = document.createElement("li");
        li.setAttribute("style", "list-style: none;");
        li.innerHTML = datosWs[i];
        ul.prepend(li);
        }
    }

    var listaMensajes = [];
    socket.onmessage = function (event) {
       
        
    const datosWs = JSON.parse(event.data);
    if (datosWs) {
        listaMensajes.push(datosWs);
        sessionStorage.setItem("mensajes", listaMensajes);
        InsertarTexto(datosWs);
    }
    };