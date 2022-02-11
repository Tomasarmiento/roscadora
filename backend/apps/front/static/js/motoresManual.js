document.addEventListener("DOMContentLoaded", (e) => {
    let btn_mov_husillo = document.getElementById('husilloMove');

    let btn_mov_abs_lin = document.getElementById('linealAbsMove');
    let btn_mov_rel_lin_fwd = document.getElementById('linealRelFwd');
    let btn_mov_rel_lin_bwd = document.getElementById('linealRelBwd');

    let btn_mov_abs_lin_cabezal = document.getElementById('cabezalAbsMove');
    let btn_mov_rel_fwd_cabezal = document.getElementById('cabezalAdd');
    let btn_mov_rel_bwd_cabezal = document.getElementById('cabezalSubtract');

    let btns_stop = document.getElementsByClassName('detener');

    //On buttons
    let btn_on_lineal = document.getElementById('onLineal');
    let btn_on_cabezal = document.getElementById('onCabezal');
    let btn_on_husillo = document.getElementById('onHusillo');

    let btn_on_sync = document.getElementById('onSync');

    //Off buttons
    let btn_off_lineal = document.getElementById('offLineal');
    let btn_off_cabezal = document.getElementById('offCabezal');
    let btn_off_husillo = document.getElementById('offHusillo');

    let btn_off_sync = document.getElementById('offSync');


    // Enables Motores Manual
    const enableLineal = document.querySelector("#linealEnable")
    const enableCabezal = document.querySelector("#cabezalEnable")
    const enableHusillo = document.querySelector("#husilloEnable")

    //Sincronizar Husillo
    const syncHusillo = document.querySelector("#husilloSync")

    

    socket.onmessage = function (event) {
        const datosWs = JSON.parse(event.data);
            
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
        //Safe
        const safe = document.querySelector("#statusSafe");

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

            // Estados De los Ejes
            const estadoActualHusillo = document.querySelector("#fHusillo");
            const estadoActualV = document.querySelector("#estVertical");
            const estadoActualH = document.querySelector("#estHorizontal");
                        
            //Monitor
            rpmActual.innerHTML = datosWs.husillo_rpm.toFixed(1)/6;
            torqueActual.innerHTML = datosWs.husillo_torque.toFixed(1);
            estadoActualHusillo.innerHTML = datosWs.estado_eje_giro;

            posicionActualV.innerHTML = datosWs.cabezal_pos.toFixed(1);
            velocidadActualV.innerHTML = datosWs.cabezal_vel.toFixed(1);
            estadoActualV.innerHTML = datosWs.estado_eje_carga;

            posicionActualH.innerHTML = datosWs.avance_pos.toFixed(1);
            velocidadActualH.innerHTML = datosWs.avance_vel.toFixed(1);
            estadoActualH.innerHTML = datosWs.estado_eje_avance;

            // //cabezal
            // if (datosWs.estado_eje_carga == 'initial'){
            // (cabezal.className = "bg-success indicadorMon") && (cabezal.innerHTML = 'Cabezal <br/> Initial') 
            // }

            //     else if (datosWs.estado_eje_carga == 'homing'){
            //     (cabezal.className = "bg-warning indicadorMon") && (cabezal.innerHTML = 'Cabezal <br/> Homming')
            //     }

            // else (cabezal.className = "bg-secondary indicadorMon");
            
            
            // //eje lineal
            // if (datosWs.estado_eje_avance == 'initial'){
            // (ejeLineal.className = "bg-success indicadorMon") && (ejeLineal.innerHTML = 'Eje lineal <br/> Initial') 
            // }

            //     else if (datosWs.estado_eje_avance == 'homing'){
            //     (ejeLineal.className = "bg-warning indicadorMon") && (ejeLineal.innerHTML = 'Eje lineal <br/> Homming')
            //     }

            // else (ejeLineal.className = "bg-secondary indicadorMon");


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

            //safe
            (datosWs.estado_eje_carga == 'safe')
            && (datosWs.estado_eje_avance == 'safe')
            && (datosWs.estado_eje_giro == 'safe')
            ?  (safe.className = "bg-danger indicadorMonSafe")
            :  (safe.className = "bg-secondary indicadorMonSafe");

            //Enables
            datosWs.lineal_enable == true
                ? (enableLineal.className = "box box-green")
                : (enableLineal.className = "box box-grey");
        
            datosWs.cabezal_enable == true
                ? (enableCabezal.className = "box box-green")
                : (enableCabezal.className = "box box-grey");
        
            datosWs.husillo_enable == true
                ? (enableHusillo.className = "box box-green")
                : (enableHusillo.className = "box box-grey");
        
            datosWs.sync_on_avance == true
                ? (syncHusillo.className = "box box-green")
                : (syncHusillo.className = "box box-grey");

                console.log(datosWs);
        }
    }



    btn_mov_husillo.addEventListener("click", (e) => {
        let rpm = document.getElementById('rpmValue').value;
        rpmMultiply = rpm*6;
        cmd = btn_mov_husillo.getAttribute('cmd');
        eje = parseInt(btn_mov_husillo.getAttribute('eje'));
        sendCommand(cmd, eje, {'ref': parseFloat(rpmMultiply)});
    });

    btn_mov_abs_lin.addEventListener("click", (e) => {
        let ref = document.getElementById('linealAbsPosValue').value;
        let ref_rate = document.getElementById('linealAbsVelocityValue').value;
        cmd = btn_mov_abs_lin.getAttribute('cmd');
        eje = parseInt(btn_mov_abs_lin.getAttribute('eje'));
        sendCommand(cmd, eje, {'ref': parseFloat(ref), 'ref_rate': parseFloat(ref_rate), 'abs': true});
    });
    
    btn_mov_rel_lin_fwd.addEventListener("click", (e) => {
        let pos = document.getElementById('linealRelPosValue').value;
        let ref_rate = document.getElementById('linealRelVelocityValue').value;
        cmd = btn_mov_rel_lin_fwd.getAttribute('cmd');
        eje = parseInt(btn_mov_rel_lin_fwd.getAttribute('eje'));
        sendCommand(cmd, eje,{'ref': parseFloat(pos), 'ref_rate': parseFloat(ref_rate), 'abs': false});
    });

    btn_mov_rel_lin_bwd.addEventListener("click", (e) => {
        let pos = document.getElementById('linealRelPosValue').value;
        let ref_rate = document.getElementById('linealRelVelocityValue').value;
        cmd = btn_mov_rel_lin_bwd.getAttribute('cmd');
        eje = parseInt(btn_mov_rel_lin_bwd.getAttribute('eje'));
        sendCommand(cmd, eje, {'ref': parseFloat(pos), 'ref_rate': parseFloat(ref_rate), 'abs': false});
    });

    btn_mov_abs_lin_cabezal.addEventListener("click", (e) => {
        let ref = document.getElementById('cabezalAbsAngleValue').value;
        let ref_rate = document.getElementById('cabezalAbsVelocityValue').value;
        cmd = btn_mov_abs_lin_cabezal.getAttribute('cmd');
        eje = parseInt(btn_mov_abs_lin_cabezal.getAttribute('eje'));
        sendCommand(cmd, eje, {'ref': parseFloat(ref), 'ref_rate': parseFloat(ref_rate), 'abs': true});
    });
    
    btn_mov_rel_fwd_cabezal.addEventListener("click", (e) => {
        let pos = document.getElementById('cabezalRelPosValue').value;
        let ref_rate = document.getElementById('cabezalRelVelocityValue').value;
        cmd = btn_mov_rel_fwd_cabezal.getAttribute('cmd');
        eje = parseInt(btn_mov_rel_fwd_cabezal.getAttribute('eje'));
        sendCommand(cmd, eje,{'ref': parseFloat(pos), 'ref_rate': parseFloat(ref_rate), 'abs': true});
    });

    btn_mov_rel_bwd_cabezal.addEventListener("click", (e) => {
        let pos = document.getElementById('cabezalRelPosValue').value;
        let ref_rate = document.getElementById('cabezalRelVelocityValue').value;
        cmd = btn_mov_rel_bwd_cabezal.getAttribute('cmd');
        eje = parseInt(btn_mov_rel_bwd_cabezal.getAttribute('eje'));
        sendCommand(cmd, eje, {'ref': parseFloat(pos), 'ref_rate': parseFloat(ref_rate), 'abs': true});
    });

    btn_on_lineal.addEventListener("click", (e) => {
        cmd = parseInt(btn_on_lineal.getAttribute('cmd'));
        eje = parseInt(btn_on_lineal.getAttribute('eje'));
        sendEnable(cmd, eje);
    });

    btn_on_cabezal.addEventListener("click", (e) => {
        cmd = parseInt(btn_on_cabezal.getAttribute('cmd'));
        eje = parseInt(btn_on_cabezal.getAttribute('eje'));
        sendEnable(cmd, eje);
    });

    btn_on_husillo.addEventListener("click", (e) => {
        cmd = parseInt(btn_on_husillo.getAttribute('cmd'));
        eje = parseInt(btn_on_husillo.getAttribute('eje'));
        sendEnable(cmd, eje);
    });

    btn_on_sync.addEventListener("click", (e) => {
        let paso = parseFloat(document.getElementById('pasoValue').value);
        cmd = parseInt(btn_on_sync.getAttribute('cmd'));
        sendSync(cmd, paso);
    });


    btn_off_lineal.addEventListener("click", (e) => {
        cmd = parseInt(btn_off_lineal.getAttribute('cmd'));
        eje = parseInt(btn_off_lineal.getAttribute('eje'));
        sendEnable(cmd, eje);
    });

    btn_off_cabezal.addEventListener("click", (e) => {
        cmd = parseInt(btn_off_cabezal.getAttribute('cmd'));
        eje = parseInt(btn_off_cabezal.getAttribute('eje'));
        sendEnable(cmd, eje);
    });

    btn_off_husillo.addEventListener("click", (e) => {
        cmd = parseInt(btn_off_husillo.getAttribute('cmd'));
        eje = parseInt(btn_off_husillo.getAttribute('eje'));
        sendEnable(cmd, eje);
    });

    btn_off_sync.addEventListener("click", (e) => {
        cmd = btn_off_sync.getAttribute('cmd');
        sendSync(cmd);
    });
    
    for(let i=0; i < btns_stop.length; i++){
        btns_stop[i].addEventListener('click', (e) => {
            let cmd = btns_stop[i].getAttribute('cmd');
            let eje = btns_stop[i].getAttribute('eje');
            sendStopAxisCommand(cmd, eje);
        });
    }
});


function sendCommand(cmd, eje, args){
    let url = "http://localhost:8000/control/manual/motor/";
    let params = "command=" + cmd + "&eje=" + eje;

    let xhr = new XMLHttpRequest();
    if(args){
        Object.entries(args).forEach(([key, value]) => {
            params += "&" + key + "=" + value;
        });
    }
    xhr.open("POST", url, true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params);
}

function sendStopAxisCommand(cmd, eje){
    let url = "http://localhost:8000/control/manual/stop-axis/";
    let params = "command=" + cmd + "&eje=" + eje;

    let xhr = new XMLHttpRequest();
    
    xhr.open("POST", url, true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params);
}

function sendEnable(cmd, eje){
    let url = "http://localhost:8000/control/manual/motor/enable/";
    let params = "command=" + cmd + "&eje=" + eje;

    let xhr = new XMLHttpRequest();
    
    xhr.open("POST", url, true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params);
}

function sendSync(cmd, paso=null){
    let url = "http://localhost:8000/control/manual/motor/sync/";
    let params = "command=" + cmd;
    if(paso){
        params += "&paso=" + paso;
    }

    let xhr = new XMLHttpRequest();
    
    xhr.open("POST", url, true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params);
}