document.addEventListener("DOMContentLoaded", (e) => {
    let btn_mov_husillo = document.getElementById('husilloMove');
    let btn_mov_abs = document.getElementById('linealAbsMove');
    let btn_mov_rel_lin_fwd = document.getElementById('linealRelFwd');
    let btn_mov_rel_lin_bwd = document.getElementById('linealRelBwd');

    btn_mov_husillo.addEventListener("click", (e) => {
        let rpm = document.getElementById('rpmValue').value;
        cmd = btn_mov_husillo.getAttribute('cmd');
        eje = parseInt(btn_mov_husillo.getAttribute('eje'));
        sendCommand(cmd, eje, {'ref': parseFloat(rpm)});
    });

    btn_mov_abs.addEventListener("click", (e) => {
        let ref = document.getElementById('linealAbsPosValue').value;
        cmd = btn_mov_abs.getAttribute('cmd');
        eje = parseInt(btn_mov_abs.getAttribute('eje'));
        sendCommand(cmd, eje, {'ref': parseFloat(ref), 'abs': true});
    });
    
    btn_mov_rel_lin_fwd.addEventListener("click", (e) => {
        let pos = document.getElementById('linealRelPosValue').value;
        cmd = btn_mov_rel_lin_fwd.getAttribute('cmd');
        eje = parseInt(btn_mov_rel_lin_fwd.getAttribute('eje'));
        sendCommand(cmd, eje,{'ref': parseFloat(pos), 'abs': false});
    });

    btn_mov_rel_lin_bwd.addEventListener("click", (e) => {
        let pos = document.getElementById('linealRelPosValue').value;
        cmd = btn_mov_rel_lin_bwd.getAttribute('cmd');
        eje = parseInt(btn_mov_rel_lin_bwd.getAttribute('eje'));
        sendCommand(cmd, eje, {'ref': parseFloat(pos), 'abs': false});
    });
});


function sendCommand(cmd, eje, args){
    let url = "http://localhost:8000/control/manual/lineal/";
    let params = "command=" + cmd + "&eje=" + eje;

    // var params = "lorem=ipsum&name=alpha";
    let xhr = new XMLHttpRequest();
    Object.entries(args).forEach(([key, value]) => {
        params += "&" + key + "=" + value;
    });
    xhr.open("POST", url, true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params);
}