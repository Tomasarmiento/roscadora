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


        //SENSORES CARGA//
        const boquillaCargaAtras = document.querySelector("#boquillaLoaderBkwrd");
        const boquillaCargaAdelante = document.querySelector("#boquillaLoaderFwrd");
        const boquillaCargaLiberada = document.querySelector("#boquillaLoaderReleased");
        const boquillaCargaAccionada = document.querySelector("#boquillaLoaderActuated");
        const boquillaCargaConCupla = document.querySelector("#boquillaLoaderCupla");

        const giroBrazoCargaArriba = document.querySelector("#turnLoadUp");
        const giroBrazoCargaAbajo = document.querySelector("#turnLoadDown");

        const verticalCargaArriba = document.querySelector("#verticalLoadUp");
        const verticalCargaAbajo = document.querySelector("#verticalLoadDown");

        const presenciaCuplaEnCargador = document.querySelector("#presenceCuplaOnLoad");


        //SENSORES DESCARGA//
        const boquillaDescargaAtras = document.querySelector("#boquillaDownloadBkwrd");
        const boquillaDescargaAdelante = document.querySelector("#boquillaDownloadFwrd");
        const boquillaDescargaLiberada = document.querySelector("#boquillaDownloadReleased");
        const boquillaDescargaAccionada = document.querySelector("#boquillaDownloadActuated");
        const boquillaDescargaConCupla = document.querySelector("#boquillaDownloadCupla");

        const gripperDescargaVerticalArriba = document.querySelector("#gripVerticalDownloaderUp");
        const gripperDescargaVerticalAbajo = document.querySelector("#gripVerticalDownloaderDown");
        const gripperDescargaHorizontalAdelante = document.querySelector("#gripHorizontalDownloaderFwrd");
        const gripperDescargaHorizontalAtras = document.querySelector("#gripHorizontalDownloaderBkwrd");
        const gripperDescargaAccionado = document.querySelector("#gripDownloaderActuated");
        const gripperDescargaLiberado = document.querySelector("#gripDownloaderReleased");

        const giroBrazoDescargaArriba = document.querySelector("#turnArmDownloadUp");
        const giroBrazoDescargaAbajo = document.querySelector("#boquillaDownloadBkwrd");

        const cuplaPorTobogánDescarga = document.querySelector("#cuplaToboganDownload");


        //PLATO//
        const neumaticoClampeoPlatoContraido = document.querySelector("#neumaticClampPlateContracted");
        const neumaticoClampeoPlatoExtendido = document.querySelector("#neumaticClampPlateExtended");
        const acopleLubricanteContraido = document.querySelector("#acopleLubricantContracted");
        const acopleLubricanteExtendido = document.querySelector("#acopleLubricantExtended");


        //MOTORES SENSORES//
        const ejelinealLimiteForward = document.querySelector("#axisLinearFwrd");
        const ejeLinealHoming = document.querySelector("#axisLinearHom");
        const ejeCabezalHoming = document.querySelector("#axisCabezalHom");

    }
}