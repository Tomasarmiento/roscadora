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
        const clampeoNo = document.querySelector("#clampeoNoOk");
        
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

          //CARGA//
          //Horizontal
          datosWs.remote_inputs[0].puntera_carga_expandida == false && datosWs.remote_inputs[0].puntera_carga_contraida == true
          ? (horizontalCargaAdelante.className = "led led-grey")
          : (horizontalCargaAdelante.className = "led led-green");

          datosWs.remote_inputs[0].puntera_carga_expandida == true && datosWs.remote_inputs[0].puntera_carga_contraida == false   
          ? (horizontalCargaAtras.className = "led led-grey")
          : (horizontalCargaAtras.className = "led led-green");

          //Vertical
          datosWs.remote_inputs[0].vertical_carga_expandido == false
          ? (verticalArriba.className = "led led-grey")
          : (verticalArriba.className = "led led-green");

          datosWs.remote_inputs[0].vertical_carga_contraido == true
          ? (verticalAbajo.className = "led led-green")
          : (verticalAbajo.className = "led led-grey");

          //Boquilla carga
          datosWs.remote_inputs[0].boquilla_carga_contraida == false
          ? (boquillaCargaCierra.className = "led led-grey")
          : (boquillaCargaCierra.className = "led led-green");

          datosWs.remote_inputs[0].boquilla_carga_expandida == false
          ? (boquillaCargaAbre.className = "led led-grey")
          : (boquillaCargaAbre.className = "led led-green");

          //Giro
          datosWs.remote_inputs[0].brazo_cargador_expandido == true && datosWs.remote_inputs[0].brazo_cargador_contraido == false
          ? (giroCargaArriba.className = "led led-grey")
          : (giroCargaArriba.className = "led led-green");

          datosWs.remote_inputs[0].brazo_cargador_expandido == false && datosWs.remote_inputs[0].brazo_cargador_contraido == true   
          ? (giroCargaAbajo.className = "led led-grey")
          : (giroCargaAbajo.className = "led led-green");


          //DESCARGA//
          //Horizontal
          datosWs.remote_inputs[0].puntera_descarga_expandida == true && datosWs.remote_inputs[0].puntera_descarga_contraida == false
          ? (horizontalDescargaAtras.className = "led led-green")
          : (horizontalDescargaAtras.className = "led led-grey");

          datosWs.remote_inputs[0].puntera_descarga_expandida == true && datosWs.remote_inputs[0].puntera_descarga_contraida == false   
          ? (horizontalDescargaAdelante.className = "led led-grey")
          : (horizontalDescargaAdelante.className = "led led-green");

          //Giro
          datosWs.remote_inputs[0].brazo_descarga_expandido == true && datosWs.remote_inputs[0].brazo_descarga_contraido == false
          ? (giroDescargaArriba.className = "led led-grey")
          : (giroDescargaArriba.className = "led led-green");

          datosWs.remote_inputs[0].brazo_descarga_expandido == false && datosWs.remote_inputs[0].brazo_descarga_contraido == true   
          ? (giroDescargaAbajo.className = "led led-grey")
          : (giroDescargaAbajo.className = "led led-green");

          //Boquilla descarga
          datosWs.remote_inputs[0].boquilla_descarga_contraida == false
          ? (boquillaDescargaCierra.className = "led led-grey")
          : (boquillaDescargaCierra.className = "led led-green");

          datosWs.remote_inputs[0].boquilla_descarga_expandida == false
          ? (boquillaDescargaAbre.className = "led led-grey")
          : (boquillaDescargaAbre.className = "led led-green");

          //Horizontal Gripper
          datosWs.remote_inputs[1].horiz_pinza_desc_contraido == true
          ? (horizontalGripperAdelante.className = "led led-grey")
          : (horizontalGripperAdelante.className = "led led-green");

          datosWs.remote_inputs[1].horiz_pinza_desc_expandido == true
          ? (horizontalGripperAtras.className = "led led-grey")
          : (horizontalGripperAtras.className = "led led-green");

          //Vertical Gripper
          datosWs.remote_inputs[1].vert_pinza_desc_expandido == true
          ? (verticalGripperArriba.className = "led led-grey")
          : (verticalGripperArriba.className = "led led-green");

          datosWs.remote_inputs[1].vert_pinza_desc_contraido == true
          ? (verticalGripperAbajo.className = "led led-grey")
          : (verticalGripperAbajo.className = "led led-green");

          //Gripper Descarga
          datosWs.remote_inputs[0].pinza_descargadora_abierta == true && datosWs.remote_inputs[0].pinza_descargadora_cerrada == false
          ? (gripperDescargaCierra.className = "led led-grey")
          : (gripperDescargaCierra.className = "led led-green");

          datosWs.remote_inputs[0].pinza_descargadora_abierta == false && datosWs.remote_inputs[0].pinza_descargadora_cerrada == true   
          ? (gripperDescargaAbre.className = "led led-grey")
          : (gripperDescargaAbre.className = "led led-green");
 

          //CABEZAL//
          //Clampeo
          datosWs.remote_inputs[1].clampeo_plato_contraido == true && datosWs.remote_inputs[1].clampeo_plato_expandido == false   
          ? (clampeoSi.className = "led led-grey")
          : (clampeoSi.className = "led led-green");

          datosWs.remote_inputs[1].clampeo_plato_contraido == false && datosWs.remote_inputs[1].clampeo_plato_expandido == true   
          ? (clampeoNo.className = "led led-grey")
          : (clampeoNo.className = "led led-green");

          //Presion
          datosWs.remote_outputs[1].presurizar == true
          ? (presionSi.className = "led led-green")
          : (presionSi.className = "led led-grey");

          datosWs.remote_outputs[1].presurizar == true
          ? (presionNo.className = "led led-grey")
          : (presionNo.className = "led led-green");

          //Boquilla 1
          datosWs.remote_outputs[1].abrir_boquilla_1 == true && datosWs.remote_outputs[1].cerrar_boquilla_1 == false 
          ? (boquilla1Cierra.className = "led led-grey")
          : (boquilla1Cierra.className = "led led-green");

          datosWs.remote_outputs[1].abrir_boquilla_1 == false && datosWs.remote_outputs[1].cerrar_boquilla_1 == true
          ? (boquilla1Abre.className = "led led-grey")
          : (boquilla1Abre.className = "led led-green");

          //Boquilla 2
          datosWs.remote_outputs[1].abrir_boquilla_2 == true && datosWs.remote_outputs[1].cerrar_boquilla_2 == false
          ? (boquilla2Cierra.className = "led led-grey")
          : (boquilla2Cierra.className = "led led-green");

          datosWs.remote_outputs[1].abrir_boquilla_2 == false && datosWs.remote_outputs[1].cerrar_boquilla_2 == true
          ? (boquilla2Abre.className = "led led-grey")
          : (boquilla2Abre.className = "led led-green");

          //Boquilla 3
          datosWs.remote_outputs[1].abrir_boquilla_3 == true && datosWs.remote_outputs[1].cerrar_boquilla_3 == false
          ? (boquilla3Cierra.className = "led led-grey")
          : (boquilla3Cierra.className = "led led-green");

          datosWs.remote_outputs[1].abrir_boquilla_3 == false && datosWs.remote_outputs[1].cerrar_boquilla_3 == true
          ? (boquilla3Abre.className = "led led-grey")
          : (boquilla3Abre.className = "led led-green");

          //Acopla Soluble
          datosWs.remote_inputs[1].acople_lubric_expandido == false
          ? (acoplaSolubleSi.className = "led led-grey")
          : (acoplaSolubleSi.className = "led led-green");

          datosWs.remote_inputs[1].acople_lubric_contraido == false
          ? (acoplaSolubleNo.className = "led led-grey")
          : (acoplaSolubleNo.className = "led led-green");

          //Bomba Soluble
          datosWs.remote_outputs[1].encender_bomba_soluble == false
          ? (bombaSolubleOn.className = "led led-grey")
          : (bombaSolubleOn.className = "led led-green");

          datosWs.remote_outputs[1].encender_bomba_soluble == true
          ? (bombaSolubleOff.className = "led led-grey")
          : (bombaSolubleOff.className = "led led-green");

          //Bomba Hidraulica
          datosWs.remote_outputs[1].encender_bomba_hidraulica == false
          ? (bombaHidraulicaOn.className = "led led-grey")
          : (bombaHidraulicaOn.className = "led led-green");

          datosWs.remote_outputs[1].encender_bomba_hidraulica == true
          ? (bombaHidraulicaOff.className = "led led-grey")
          : (bombaHidraulicaOff.className = "led led-green");
        console.log(datosWs);
          
        }
    }




document.addEventListener("DOMContentLoaded", (e) => {

    let btns = document.getElementsByTagName('button');
    
    for(let i=0; i < btns.length; i++){
        if(btns[i].hasAttribute('menu')){
            btns[i].addEventListener('click', (e) => {
                let menu = btns[i].getAttribute('menu');
                let cmd = btns[i].getAttribute('cmd');
                let name = btns[i].getAttribute('id');
                let btn = name.slice(name.indexOf('X')+1)
                name = name.slice(0, name.indexOf('X'));
                sendCommand(cmd, menu, name, btn);
            });
        }
    }
});


function sendCommand(cmd, menu, name, btn){
    let url = "http://localhost:8000/control/manual/neummatica/";
    let params = "command=" + cmd + "&menu=" + menu + "&name=" + name + "&btn=" + btn;

    // var params = "lorem=ipsum&name=alpha";
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params);
}