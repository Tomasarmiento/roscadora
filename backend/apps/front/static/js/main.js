console.log('enter ws')

//const{Monitorear} = require ('./monitor.component')

//import { Monitorear } from "./monitorComponent.js";

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


function Monitorear(dataWs) {
  
  // Tabla de datos
  const rpmActual = document.querySelector("#frRPM");
  const torqueActual = document.querySelector("#fTorque");

  // Datos Eje vertical
  const posicionActualV = document.querySelector("#posVertical");
  const velocidadActualV = document.querySelector("#velVertical");

  // Datos Eje Horizontal
  const posicionActualH = document.querySelector("#posHorizontal");
  const velocidadActualH = document.querySelector("#velHorizontal");
  
    

  if (dataWs) {
    //Monitor
    rpmActual.innerHTML = dataWs.husillo_rpm.toFixed(1);
    torqueActual.innerHTML = dataWs.husillo_torque.toFixed(1);

    posicionActualV.innerHTML = dataWs.cabezal_pos.toFixed(1);
    velocidadActualV.innerHTML = dataWs.cabezal_vel.toFixed(1);

    posicionActualH.innerHTML = dataWs.avance_pos.toFixed(1);
    velocidadActualH.innerHTML = dataWs.avance_vel.toFixed(1);
  
    
    
    console.log(dataWs);  
      
  }
}
ConnectWebSocket();