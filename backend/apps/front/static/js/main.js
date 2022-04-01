var monitor = null;


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
    monitor = document.querySelector("#component-monitor");
});
var listaMensajesErrores = [];
socket.onmessage = function (event) {
  const datosWs = JSON.parse(event.data);
  if (datosWs.mensajes_error.length > 0) {
    listaMensajesErrores.push(datosWs.mensajes_error);
    sessionStorage.setItem("mensajesError", listaMensajesErrores);
  };

 

  // Tabla de datos
  const rpmActual = document.querySelector("#frRPM");
  const torqueActual = document.querySelector("#fTorque");

  // Datos Eje vertical
  const posicionActualV = document.querySelector("#posVertical");
  const velocidadActualV = document.querySelector("#velVertical");

  // Datos Eje Horizontal
  const posicionActualH = document.querySelector("#posHorizontal");
  const velocidadActualH = document.querySelector("#velHorizontal");

  // Estados De los Ejes
  const estadoActualHusillo = document.querySelector("#fHusillo");
  const estadoActualV = document.querySelector("#estVertical");
  const estadoActualH = document.querySelector("#estHorizontal");

  // Contador de cuplas
  const contadorCuplas = document.querySelector("#countCuplas");
    

  //Cabezal
  const cabezal = document.querySelector("#statusHead")
  //Eje Lineal
  const ejeLineal = document.querySelector("#statusLinealAxis")
  //Descarga
  const descarga = document.querySelector("#statusDownloader");
  //Carga
  const carga = document.querySelector("#statusLoader");
  //Indexar
  const indexar = document.querySelector("#statusIndex");
  //Roscado
  const roscado = document.querySelector("#statusRoscado");
  //Safe
  const safe = document.querySelector("#statusSafe");
  
  if (datosWs) {


    //Monitor
    rpmActual.innerHTML = datosWs.husillo_rpm.toFixed(1);
    torqueActual.innerHTML = datosWs.husillo_torque.toFixed(1);
    estadoActualHusillo.innerHTML = datosWs.estado_eje_giro;

    posicionActualV.innerHTML = datosWs.cabezal_pos.toFixed(1);
    velocidadActualV.innerHTML = datosWs.cabezal_vel.toFixed(1);
    estadoActualV.innerHTML = datosWs.estado_eje_carga;

    posicionActualH.innerHTML = datosWs.avance_pos.toFixed(1);
    velocidadActualH.innerHTML = datosWs.avance_vel.toFixed(1);
    estadoActualH.innerHTML = datosWs.estado_eje_avance;

    contadorCuplas.innerHTML = datosWs.roscado_contador;




    // //cabezal
    // if (datosWs.estado_eje_carga == 'initial'){
    //   (cabezal.className = "bg-success indicadorMon") && (cabezal.innerHTML = 'Cabezal <br/> Initial') 
    //   }

    //   else if (datosWs.estado_eje_carga == 'homing'){
    //   (cabezal.className = "bg-warning indicadorMon") && (cabezal.innerHTML = 'Cabezal <br/> Homming')
    //   }

    // else (cabezal.className = "bg-secondary indicadorMon");
    
    
    // //eje lineal
    // if (datosWs.estado_eje_avance == 'initial'){
    //   (ejeLineal.className = "bg-success indicadorMon") && (ejeLineal.innerHTML = 'Eje lineal <br/> Initial') 
    //   }

    //   else if (datosWs.estado_eje_avance == 'homing'){
    //   (ejeLineal.className = "bg-warning indicadorMon") && (ejeLineal.innerHTML = 'Eje lineal <br/> Homming')
    //   }

    // else (ejeLineal.className = "bg-secondary indicadorMon");
     
    //Cabezal
    const homeok = document.querySelector("#homeOk");
      // datosWs.cabezal_cero_desconocido = false
      // datosWs.lineal_cero_desconocido = false
      // datosWs.homing_on_going = false
    if (datosWs){
      if (datosWs.lineal_cero_desconocido == false && datosWs.cabezal_cero_desconocido == false && datosWs.homing_on_going == true){
        (homeok.className = "bg-warning rounded-pill text-white text-center p-3")  && (homeok.innerHTML = 'HOMING')
      }
      else if (datosWs.lineal_cero_desconocido == false && datosWs.cabezal_cero_desconocido == false){
        (homeok.className = "bg-success rounded-pill text-white text-center p-3") && (homeok.innerHTML = 'HOME OK')  
      }
      else if (datosWs.homing_on_going == true){
        (homeok.className = "bg-warning rounded-pill text-white text-center p-3")  && (homeok.innerHTML = 'HOMING')
      }

      else (homeok.className = "bg-secondary rounded-pill text-white text-center p-3") && (homeok.innerHTML = 'HOME OK');

      // else (homeok.className = "bg-secondary rounded-pill text-white text-center p-3");
     

      
      // if (datosWs.lineal_cero_desconocido == false && datosWs.cabezal_cero_desconocido == false){
      //   (homeok.className = "bg-success rounded-pill text-white text-center p-3")   
      // }
      // else if (datosWs.homing_on_going == true){
      //   (homeok.className = "bg-warning rounded-pill text-white text-center p-3") && (homeok.innerHTML = 'HOMMING')
      // }
      // else (homeok.className = "bg-secondary rounded-pill text-white text-center p-3");


console.log();
    //descarga
     datosWs.condiciones_init_descarga_ok == true
    ? (descarga.className = "bg-success indicadorMon")
    : (descarga.className = "bg-secondary indicadorMon");


    //carga
     datosWs.condiciones_init_carga_ok == true
    ? (carga.className = "bg-success indicadorMon")
    : (carga.className = "bg-secondary indicadorMon");

    //indexar
    datosWs.condiciones_init_indexar_ok == true
     ? (indexar.className = "bg-success indicadorMon")
     : (indexar.className = "bg-secondary indicadorMon");


    //roscado
    datosWs.condiciones_init_roscado_ok == true
     ? (roscado.className = "bg-success indicadorMon")
     : (roscado.className = "bg-secondary indicadorMon");

    //safe
    (datosWs.estado_eje_carga == 'safe')
     && (datosWs.estado_eje_avance == 'safe')
     && (datosWs.estado_eje_giro == 'safe')
     ?  (safe.className = "bg-danger indicadorMonSafe")
     :  (safe.className = "bg-secondary indicadorMonSafe");


  }
}};


    



  
