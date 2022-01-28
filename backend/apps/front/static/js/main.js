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
  const roscado = document.querySelector("#statusRoscado")

  if (datosWs) {
    //Monitor
    rpmActual.innerHTML = datosWs.husillo_rpm.toFixed(1);
    torqueActual.innerHTML = datosWs.husillo_torque.toFixed(1);

    posicionActualV.innerHTML = datosWs.cabezal_pos.toFixed(1);
    velocidadActualV.innerHTML = datosWs.cabezal_vel.toFixed(1);

    posicionActualH.innerHTML = datosWs.avance_pos.toFixed(1);
    velocidadActualH.innerHTML = datosWs.avance_vel.toFixed(1);



    //cabezal
    datosWs.estado_eje_carga == 'initial'
    ? (cabezal.className = "bg-success indicadorMon") && (cabezal.innerHTML = 'Cabezal <br/> Initial')
    : (cabezal.className = "bg-secondary indicadorMon");

    datosWs.estado_eje_carga == 'homing'
    ? (cabezal.className = "bg-warning indicadorMon") && (cabezal.innerHTML = 'Cabezal <br/> Homming')
    : (cabezal.className = "bg-secondary indicadorMon");

    //eje lineal
    datosWs.estado_eje_avance == 'initial'
    ? (ejeLineal.className = "bg-success indicadorMon") && (ejeLineal.innerHTML = 'Eje lineal <br/> Initial')
    : (ejeLineal.className = "bg-secondary indicadorMon");

    datosWs.estado_eje_avance == 'homing'
    ? (ejeLineal.className = "bg-warning indicadorMon") && (ejeLineal.innerHTML = 'Eje lineal <br/> Homming')
    : (ejeLineal.className = "bg-secondary indicadorMon");


    //descarga
    datosWs.remote_outputs[1].encender_bomba_hidraulica == true 
     && datosWs.remote_inputs[1].clampeo_plato_expandido == true
     && datosWs.remote_inputs[0].puntera_descarga_contraida == true
     && datosWs.remote_inputs[0].brazo_descarga_expandido == true
     && datosWs.remote_inputs[0].boquilla_descarga_expandida == true
     && datosWs.remote_inputs[1].cupla_por_tobogan_descarga == true
     && datosWs.remote_inputs[1].pieza_en_boquilla_descarga == true
     && datosWs.remote_inputs[1].horiz_pinza_desc_contraido == true
     && datosWs.remote_inputs[1].vert_pinza_desc_contraido == true
     && datosWs.remote_inputs[0].pinza_descargadora_abierta == true && datosWs.remote_inputs[0].pinza_descargadora_cerrada == false
    ? (descarga.className = "bg-success indicadorMon")
    : (descarga.className = "bg-secondary indicadorMon");


    //carga
    datosWs.remote_outputs[1].encender_bomba_hidraulica == true
     && datosWs.remote_inputs[1].clampeo_plato_expandido == true
     && datosWs.remote_inputs[0].vertical_carga_contraido == true
     && datosWs.remote_inputs[0].puntera_carga_expandida == false && datosWs.remote_inputs[0].puntera_carga_contraida == true
     && datosWs.remote_inputs[0].brazo_cargador_expandido == true && datosWs.remote_inputs[0].brazo_cargador_contraido == false
     && datosWs.remote_inputs[0].boquilla_carga_expandida == true
     && datosWs.remote_inputs[1].presencia_cupla_en_cargador == true
     && datosWs.remote_inputs[1].pieza_en_boquilla_carga == true
    ? (carga.className = "bg-success indicadorMon")
    : (carga.className = "bg-secondary indicadorMon");

    //indexar
    datosWs.remote_inputs[1].clampeo_plato_contraido == false && datosWs.remote_inputs[1].clampeo_plato_expandido == true
     && datosWs.remote_inputs[1].acople_lubric_contraido == true
     && datosWs.remote_inputs[0].puntera_descarga_expandida == false && datosWs.remote_inputs[0].puntera_descarga_contraida == true
     && datosWs.remote_inputs[0].puntera_carga_expandida == false && datosWs.remote_inputs[0].puntera_carga_contraida == true
     && datosWs.avance_pos.toFixed(1) >= datosWs.posicion_de_inicio
     ? (indexar.className = "bg-success indicadorMon")
     : (indexar.className = "bg-secondary indicadorMon");


    //roscado
    datosWs.remote_outputs[1].encender_bomba_hidraulica == true
     && datosWs.remote_inputs[1].clampeo_plato_contraido == false && datosWs.remote_inputs[1].clampeo_plato_expandido == true
     && datosWs.estado_eje_avance == 'initial'
     && datosWs.cabezal_enable == false
     && datosWs.avance_pos.toFixed(1) == datosWs.posicion_de_inicio
     ? (roscado.className = "bg-success indicadorMon")
     : (roscado.className = "bg-secondary indicadorMon");
     
     
  }

    
}


  
