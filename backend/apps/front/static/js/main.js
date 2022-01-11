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
    monitorHorizontal = document.querySelector("#component-monitor-horizontal");

});

window.addEventListener("DOMContentLoaded", () => {                         //todo el tiempo
    (window.location.hash);
    monitor = document.querySelector("#component-monitor");
    monitorHorizontal = document.querySelector("#component-monitor-horizontal");
});

socket.onmessage = function (event) {
  const datosWs = JSON.parse(event.data);
  console.log(datosWs)



  
  // Tabla de datos
  const rpmActual = document.querySelector("#frRPM");
  const torqueActual = document.querySelector("#fTorque");

  // Datos Eje vertical
  const posicionActualV = document.querySelector("#posVertical");
  const velocidadActualV = document.querySelector("#velVertical");

  // Datos Eje Horizontal
  const posicionActualH = document.querySelector("#posHorizontal");
  const velocidadActualH = document.querySelector("#velHorizontal");
  
  if (datosWs) {
    //Monitor
    rpmActual.innerHTML = datosWs.husillo_rpm.toFixed(1);
    torqueActual.innerHTML = datosWs.husillo_torque.toFixed(1);

    posicionActualV.innerHTML = datosWs.cabezal_pos.toFixed(1);
    velocidadActualV.innerHTML = datosWs.cabezal_vel.toFixed(1);

    posicionActualH.innerHTML = datosWs.avance_pos.toFixed(1);
    velocidadActualH.innerHTML = datosWs.avance_vel.toFixed(1);
  
    
    
    console.log(datosWs);  
      
  }
}
