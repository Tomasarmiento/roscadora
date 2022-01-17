
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

socket.onmessage = function (event) {
    const datosWs = JSON.parse(event.data);

    if (datosWs) {


       


        console.log(datosWs);
    }
}