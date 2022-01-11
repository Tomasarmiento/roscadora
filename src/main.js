import "jquery/dist/jquery";       
import "bootstrap"; 
import "bootstrap/dist/css/bootstrap.min.css";
import './main.css'
import './components/monitor/monitor.component.css'

import {router} from './router/index.routes'
import { Monitorear } from "./components/monitor/monitor.component";

router(window.location.hash);

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


window.addEventListener("hashchange", () => {                  //cuando tocas f5
    router(window.location.hash);
    monitor = document.querySelector("#component-monitor");
    monitorHorizontal = document.querySelector("#component-monitor-horizontal");

});

window.addEventListener("DOMContentLoaded", () => {                         //todo el tiempo
    router(window.location.hash);
    monitor = document.querySelector("#component-monitor");
    monitorHorizontal = document.querySelector("#component-monitor-horizontal");
});



// Escucha cierre de WebSocket
socket.onclose = function (event) {
    window.location.reload();
  };



socket.onmessage = function (event) {
    switch (window.location.hash) {
        case "#/home":
        case "#/referenciar":
        case "#/neumaticaManual":
        case "#/motoresManual":
          monitor && "data" in datosWs ? Monitorear(datosWs.data) : "";
          break;
    
        case "#/automatico":
        case "#/semiautomatico":
        case "#/sensores":
        case "#/monitorEstados":
      }
    
      if ("hash" in datosWs) {
        window.location.hash = datosWs.hash;
      }
    };