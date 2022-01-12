document.addEventListener("DOMContentLoaded", (e) => {
    let btn_homming = document.getElementById('homeExec');

    btn_homming.addEventListener('click', (e) => {
        let routine = btn_homming.getAttribute('routine');
        startRoutine(routine);
    });
});

function startRoutine(routine){
    let url = "http://localhost:8000/control/semiautomatico/";
    let params = "routine=" + routine;

    // var params = "lorem=ipsum&name=alpha";
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params);
}