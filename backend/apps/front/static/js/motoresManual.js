document.addEventListener("DOMContentLoaded", (e) => {
    let btn_mov_husillo = document.getElementById('husilloMove');

    let btn_mov_abs_lin = document.getElementById('linealAbsMove');
    let btn_mov_rel_lin_fwd = document.getElementById('linealRelFwd');
    let btn_mov_rel_lin_bwd = document.getElementById('linealRelBwd');

    let btn_mov_abs_lin_cabezal = document.getElementById('cabezalAbsMove');
    let btn_mov_rel_fwd_cabezal = document.getElementById('cabezalAdd');
    let btn_mov_rel_bwd_cabezal = document.getElementById('cabezalSubtract');

    let btns_stop = document.getElementsByClassName('detener');

    //Enable buttons
    let btn_enable_lineal = document.getElementById('linealEnable');
    let btn_enable_cabezal = document.getElementById('cabezalEnable');
    let btn_enable_husillo = document.getElementById('husilloEnable');

    btn_enable_husillo.addEventListener('change', (e) => {
        let eje = btn_enable_husillo.getAttribute('eje');
        sendEnable(eje);
    });

    btn_enable_lineal.addEventListener('change', (e) => {
        let eje = btn_enable_lineal.getAttribute('eje');
        sendEnable(eje);
    });
    
    btn_enable_cabezal.addEventListener('change', (e) => {
        let eje = btn_enable_cabezal.getAttribute('eje');
        sendEnable(eje);
    });

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

function sendEnable(eje){
    let url = "http://localhost:8000/control/manual/motor/enable/";
    let params = "eje=" + eje;

    let xhr = new XMLHttpRequest();
    
    xhr.open("POST", url, true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params);
}