console.log('enter ws')

var monitor = null;
var monitorHorizontal = null;


function ConnectWebSocket() {
  if ("WebSocket" in window) {
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
    }
}


window.addEventListener("hashchange", () => {                  //cuando tocas f5
    (window.location.hash);
    monitor = document.querySelector("#component-monitor");
    monitorHorizontal = document.querySelector("#component-monitor-horizontal");

});

window.addEventListener("DOMContentLoaded", () => {                         //todo el tiempo
    (window.location.hash);
    monitor = document.querySelector("#component-monitor");
    monitorHorizontal = document.querySelector("#component-monitor-horizontal");
});




ConnectWebSocket();