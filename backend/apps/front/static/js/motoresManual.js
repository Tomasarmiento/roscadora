document.addEventListener("DOMContentLoaded", (e) => {
    
    let btn = document.getElementById('absMoveV');

    btn.addEventListener("click", (e) => {
        let rpm = document.getElementById('absPosV').value;
        send_command(btn.getAttribute('cmd'), {'rpm': rpm});
    })
});

function send_command(cmd, values){
    let data = {
        'command': cmd
    };
    if(values.pos) data.pos = values.pos;
    if(values.vel) data.vel = values.vel;
    if(values.rpm) data.rpm = values.rpm;

    $.post("http://localhost:8000/control/", data, function(resp){console.log(resp);});
}