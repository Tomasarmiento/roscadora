var data = []
var monitor = null;
var monitorHorizontal = null;

    const socket = new WebSocket("ws://127.0.0.1:8000/ws/front/");
    socket.addEventListener("open", function (event) {
        socket.send(
          JSON.stringify({
            message: "datos",      
          })
        );
    });
    // Escucha cierre de WebSocket
    socket.onclose = function (event) {
        window.location.reload();
      };
    
window.addEventListener("hashchange", () => {                  //cuando tocas f5
    (window.location.hash);
    monitor = document.querySelector("#component-monitor");

});

window.addEventListener("DOMContentLoaded", () => {                         //todo el tiempo
    (window.location.hash);
    cuadroDeErrores = document.querySelector("#terminalDeTexto");
    if (sessionStorage.getItem("mensajesError") && cuadroDeErrores) {
        console.log('aca');
        let ul = document.getElementById("cuadroMensajesErrores");
        const listaMensajes = sessionStorage.getItem("mensajesError").split(",").reverse();
        for (let i = 0; i < listaMensajes.length; i++) {
            const li = document.createElement("li");
            li.setAttribute("style", "list-style: none;");
            li.innerHTML = listaMensajes[i];
            ul.appendChild(li);
        }
    }

    let btn_servo1 = document.getElementById('servo1');

        btn_servo1.addEventListener('click', (e) => {
            let url = "http://localhost:8000/control/auto/";
    
            let xhr = new XMLHttpRequest();
    
            xhr.open("POST", url, true);
    
            //Send the proper header information along with the request
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    
            xhr.send();
        });

    let btn_servo2 = document.getElementById('servo2');

        btn_servo2.addEventListener('click', (e) => {
            let url = "http://localhost:8000/control/auto/";
    
            let xhr = new XMLHttpRequest();
    
            xhr.open("POST", url, true);
    
            //Send the proper header information along with the request
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    
            xhr.send();
        });

    let btn_servo3 = document.getElementById('servo3');

        btn_servo3.addEventListener('click', (e) => {
            let url = "http://localhost:8000/control/auto/";

            let xhr = new XMLHttpRequest();

            xhr.open("POST", url, true);

            //Send the proper header information along with the request
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

            xhr.send();
        });
        
});
    window.onload = function() {
    var listaMensajesErrores = [];
    socket.onmessage = function (event) {
    const datosWs = JSON.parse(event.data);
    console.log(datosWs)


    if (datosWs.mensajes_error.length > 0) {
        listaMensajesErrores.push(datosWs.mensajes_error);
        sessionStorage.setItem("mensajesError", listaMensajesErrores);
        InsertarTextoErrores(datosWs.mensajes_error);
    };
}};