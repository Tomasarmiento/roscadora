socket.onmessage = function (event) {
    const datosWs = JSON.parse(event.data);

    if (datosWs) {
        
        // Tabla de datos
        const rpmActual = document.querySelector("#frRPM");
        const torqueActual = document.querySelector("#fTorque");
        
        // Datos Eje vertical
        const posicionActualV = document.querySelector("#posVertical");
        const velocidadActualV = document.querySelector("#velVertical");
        
        // Datos Eje Horizontal
        const posicionActualH = document.querySelector("#posHorizontal");
        const velocidadActualH = document.querySelector("#velHorizontal");
        
        //Monitor
        rpmActual.innerHTML = datosWs.husillo_rpm.toFixed(1);
        torqueActual.innerHTML = datosWs.husillo_torque.toFixed(1);

        posicionActualV.innerHTML = datosWs.cabezal_pos.toFixed(1);
        velocidadActualV.innerHTML = datosWs.cabezal_vel.toFixed(1);

        posicionActualH.innerHTML = datosWs.avance_pos.toFixed(1);
        velocidadActualH.innerHTML = datosWs.avance_vel.toFixed(1);

      
        //Carga
        const horizontalCargaAdelante = document.querySelector("#horizontalCargaAdelanteOk");
        const horizontalCargaAtras = document.querySelector("#horizontalCargaAtrasOk");
        
        const verticalArriba = document.querySelector("#verticalCargaArribaOk");
        const verticalAbajo = document.querySelector("#verticalCargaAbajoOk");
        
        const boquillaCargaCierra = document.querySelector("#boquillaCargaCierraOk");
        const boquillaCargaAbre = document.querySelector("#boquillaCargaAbreOk");
        
        const giroCargaArriba = document.querySelector("#giroCargaArribaOk");
        const giroCargaAbajo = document.querySelector("#giroCargaAbajoOk");
        
        
        //Descarga
        const horizontalDescargaAtras = document.querySelector("#horizontalDescAtrasOk");
        const horizontalDescargaAdelante = document.querySelector("#horizontalDescAdelanteOk");
        
        const giroDescargaArriba = document.querySelector("#giroDescArribaOk");
        const giroDescargaAbajo = document.querySelector("#giroDescAbajoOk");
        
        const boquillaDescargaCierra = document.querySelector("#boquillaDescCierraOk");
        const boquillaDescargaAbre = document.querySelector("#boquillaDescAbreOk");

        const horizontalGripperAdelante = document.querySelector("#horizontalGrAdelanteOk");
        const horizontalGripperAtras = document.querySelector("#horizontalGrAtrasOk");
        
        const verticalGripperArriba = document.querySelector("#verticalGrArribaOk");
        const verticalGripperAbajo = document.querySelector("#verticalGrAbajoOk");
        
        const gripperDescargaCierra = document.querySelector("#gripperDescCierraOk");
        const gripperDescargaAbre = document.querySelector("#gripperDescAbreOk");
        
        
        //Cabezal
        const clampeoSi = document.querySelector("#clampeoSiOk");
        const clampeoNo = document.querySelector("#clampeoNoSiOk");
        
        const presionSi = document.querySelector("#presionSiOk");
        const presionNo = document.querySelector("#presionNoOk");
        
        const boquilla1Cierra = document.querySelector("#boquilla1CierraOk");
        const boquilla1Abre = document.querySelector("#boquilla1AbreOk");
        
        const boquilla2Cierra = document.querySelector("#boquilla2CierraOk");
        const boquilla2Abre = document.querySelector("#boquilla2AbreOk");
        
        const boquilla3Cierra = document.querySelector("#boquilla3CierraOk");
        const boquilla3Abre = document.querySelector("#boquilla3AbreOk");
        
        const acoplaSolubleSi = document.querySelector("#acoplaSolSiOk");
        const acoplaSolubleNo = document.querySelector("#acoplaSolNoOk");
        
        const bombaSolubleOn = document.querySelector("#bombaSolOnOk");
        const bombaSolubleOff = document.querySelector("#bombaSolOffOk");
        
        const bombaHidraulicaOn = document.querySelector("#bombaHidrOnOk");
        const bombaHidraulicaOff = document.querySelector("#bombaHidrOffOk");


          //CARGA//
          //Horizontal
          datosWs.puntera_carga_expandida == true && datosWs.puntera_carga_contraida == false
          ? (horizontalCargaAdelante.className = "led led-grey")
          : (horizontalCargaAdelante.className = "led led-green");

          datosWs.puntera_carga_expandida == false && datosWs.puntera_carga_contraida == true   
          ? (horizontalCargaAtras.className = "led led-grey")
          : (horizontalCargaAtras.className = "led led-green");

          //Vertical
          datosWs.expandir_vertical_carga == false
          ? (verticalArriba.className = "led led-grey")
          : (verticalArriba.className = "led led-green");

          datosWs.expandir_vertical_carga == true
          ? (verticalAbajo.className = "led led-grey")
          : (verticalAbajo.className = "led led-green");

          //Boquilla carga
          datosWs.contraer_boquilla_carga == false
          ? (boquillaCargaCierra.className = "led led-grey")
          : (boquillaCargaCierra.className = "led led-green");

          datosWs.contraer_boquilla_carga == true
          ? (boquillaCargaAbre.className = "led led-grey")
          : (boquillaCargaAbre.className = "led led-green");

          //Giro
          datosWs.expandir_brazo_cargador == true && datosWs.contraer_brazo_cargador == false
          ? (giroCargaArriba.className = "led led-grey")
          : (giroCargaArriba.className = "led led-green");

          datosWs.expandir_brazo_cargador == false && datosWs.contraer_brazo_cargador == true   
          ? (giroCargaAbajo.className = "led led-grey")
          : (giroCargaAbajo.className = "led led-green");


          //DESCARGA//
          //Horizontal
          datosWs.expandir_puntera_descarga == true && datosWs.contraer_brazo_cargador == false
          ? (horizontalDescargaAtras.className = "led led-grey")
          : (horizontalDescargaAtras.className = "led led-green");

          datosWs.expandir_puntera_descarga == false && datosWs.contraer_brazo_cargador == true   
          ? (horizontalDescargaAdelante.className = "led led-grey")
          : (horizontalDescargaAdelante.className = "led led-green");

          //Giro
          datosWs.expandir_brazo_descargador == true && datosWs.contraer_brazo_descargador == false
          ? (giroDescargaArriba.className = "led led-grey")
          : (giroDescargaArriba.className = "led led-green");

          datosWs.expandir_brazo_descargador == false && datosWs.contraer_brazo_descargador == true   
          ? (giroDescargaAbajo.className = "led led-grey")
          : (giroDescargaAbajo.className = "led led-green");

          //Boquilla descarga
          datosWs.contraer_boquilla_descarga == false
          ? (boquillaDescargaCierra.className = "led led-grey")
          : (boquillaDescargaCierra.className = "led led-green");

          datosWs.contraer_boquilla_descarga == true
          ? (boquillaDescargaAbre.className = "led led-grey")
          : (boquillaDescargaAbre.className = "led led-green");

          //Horizontal Gripper
          datosWs.expandir_horiz_pinza_desc == false
          ? (horizontalGripperAdelante.className = "led led-grey")
          : (horizontalGripperAdelante.className = "led led-green");

          datosWs.expandir_horiz_pinza_desc == true
          ? (horizontalGripperAtras.className = "led led-grey")
          : (horizontalGripperAtras.className = "led led-green");

          //Vertical Gripper
          datosWs.expandir_vert_pinza_desc == false
          ? (verticalGripperArriba.className = "led led-grey")
          : (verticalGripperArriba.className = "led led-green");

          datosWs.expandir_vert_pinza_desc == true
          ? (verticalGripperAbajo.className = "led led-grey")
          : (verticalGripperAbajo.className = "led led-green");

          //Gripper Descarga
          datosWs.abrir_pinza_descargadora == true && datosWs.cerrar_pinza_descargadora == false
          ? (gripperDescargaCierra.className = "led led-grey")
          : (gripperDescargaCierra.className = "led led-green");

          datosWs.abrir_pinza_descargadora == false && datosWs.cerrar_pinza_descargadora == true   
          ? (gripperDescargaAbre.className = "led led-grey")
          : (gripperDescargaAbre.className = "led led-green");
 

          //CABEZAL//
          //Clampeo
          datosWs.contraer_clampeo_plato == true && datosWs.expandir_clampeo_plato == false   
          ? (clampeoSi.className = "led led-grey")
          : (clampeoSi.className = "led led-green");

          datosWs.contraer_clampeo_plato == false && datosWs.expandir_clampeo_plato == true   
          ? (clampeoNo.className = "led led-grey")
          : (clampeoNo.className = "led led-green");

          //Presion
          datosWs.presurizar == true && datosWs.presurizar == false   
          ? (presionSi.className = "led led-grey")
          : (presionSi.className = "led led-green");

          datosWs.presurizar == false && datosWs.presurizar == true   
          ? (presionNo.className = "led led-grey")
          : (presionNo.className = "led led-green");

          //Boquilla 1
          datosWs.abrir_boquilla_1 == true && datosWs.cerrar_boquilla_1 == false   
          ? (boquilla1Cierra.className = "led led-grey")
          : (boquilla1Cierra.className = "led led-green");

          datosWs.abrir_boquilla_1 == false && datosWs.cerrar_boquilla_1 == true   
          ? (boquilla1Abre.className = "led led-grey")
          : (boquilla1Abre.className = "led led-green");

          //Boquilla 2
          datosWs.abrir_boquilla_2 == true && datosWs.cerrar_boquilla_2 == false   
          ? (boquilla2Cierra.className = "led led-grey")
          : (boquilla2Cierra.className = "led led-green");

          datosWs.abrir_boquilla_2 == false && datosWs.cerrar_boquilla_2 == true   
          ? (boquilla2Abre.className = "led led-grey")
          : (boquilla2Abre.className = "led led-green");

          //Boquilla 3
          datosWs.abrir_boquilla_3 == true && datosWs.cerrar_boquilla_3 == false   
          ? (boquilla3Cierra.className = "led led-grey")
          : (boquilla3Cierra.className = "led led-green");

          datosWs.abrir_boquilla_3 == false && datosWs.cerrar_boquilla_3 == true   
          ? (boquilla3Abre.className = "led led-grey")
          : (boquilla3Abre.className = "led led-green");

          //Acopla Soluble
          datosWs.expandir_acople_lubric == false
          ? (acoplaSolubleSi.className = "led led-grey")
          : (acoplaSolubleSi.className = "led led-green");

          datosWs.expandir_acople_lubric == true
          ? (acoplaSolubleNo.className = "led led-grey")
          : (acoplaSolubleNo.className = "led led-green");

          //Bomba Soluble
          datosWs.encender_bomba_soluble == false
          ? (bombaSolubleOn.className = "led led-grey")
          : (bombaSolubleOn.className = "led led-green");

          datosWs.encender_bomba_soluble == true
          ? (bombaSolubleOff.className = "led led-grey")
          : (bombaSolubleOff.className = "led led-green");

          //Bomba Hidraulica
          datosWs.encender_bomba_hidraulica == false
          ? (bombaHidraulicaOn.className = "led led-grey")
          : (bombaHidraulicaOn.className = "led led-green");

          datosWs.encender_bomba_hidraulica == true
          ? (bombaHidraulicaOff.className = "led led-grey")
          : (bombaHidraulicaOff.className = "led led-green");

        }
    }




document.addEventListener("DOMContentLoaded", (e) => {

    let btns_carga = document.getElementsByTagName('button');
    
    for(let i=0; i < btns_carga.length; i++){
        if(btns_carga[i].hasAttribute('menu')){
            btns_carga[i].addEventListener('click', (e) => {
                let menu = btns_carga[i].getAttribute('menu');
                let cmd = btns_carga[i].getAttribute('cmd');
                let name = btns_carga[i].getAttribute('id');
                name = name.slice(0, name.indexOf('OnOff'));
                sendCommand(cmd, menu, name);
            });
        }
    }
});


function sendCommand(cmd, menu, name){
    let url = "http://localhost:8000/control/manual/neummatica/";
    let params = "command=" + cmd + "&menu=" + menu + "&name=" + name;

    // var params = "lorem=ipsum&name=alpha";
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params);
}