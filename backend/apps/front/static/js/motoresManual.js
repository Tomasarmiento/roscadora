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

    // Enables Motores Manual
    const enableLineal = document.querySelector("#linealEnable")
    const enableCabezal = document.querySelector("#cabezalEnable")
    const enableHusillo = document.querySelector("#husilloEnable")

    //Sincronizar Husillo
    const syncHusillo = document.querySelector("#husilloSync")

    

    socket.onmessage = function (event) {
        const datosWs = JSON.parse(event.data);
        if (datosWs) {
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
        cmd = btn_mov_husillo.getAttribute('cmd');
        eje = parseInt(btn_mov_husillo.getAttribute('eje'));
        sendCommand(cmd, eje, {'ref': parseFloat(rpm)});
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