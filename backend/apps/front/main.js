import "core-js";
import "regenerator-runtime/runtime";


const socket = new WebSocket("ws://127.0.0.1:8000/ws/front/");

// Abre la conexión
socket.addEventListener("open", function (event) {
  socket.send(
    JSON.stringify({
      message: "datos",      
    })
  );
});

window.addEventListener("hashchange", () => {                  //cuando tocas f5
    (window.location.hash);                                    //router
    monitor = document.querySelector("#component-monitor");
    monitorHorizontal = document.querySelector("#component-monitor-horizontal");
});

window.addEventListener("DOMContentLoaded", () => {                         //todo el tiempo
    (window.location.hash);                                                 //router
    monitor = document.querySelector("#component-monitor");
    monitorHorizontal = document.querySelector("#component-monitor-horizontal");
});

// Escucha cierre de WebSocket
socket.onclose = function (event) {
    window.location.reload();
  };