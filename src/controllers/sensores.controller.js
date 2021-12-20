import views from "../views/sensores.html";

export function MonitorearSensores(dataWs) {
  // Indicadores PINZAS CARGA/DESCARGA
  const grippCarga_atras = document.querySelector("#gripperLoaderBkwrd");
  const grippCarga_adelante = document.querySelector("#gripperLoaderFwrd");
  const grippCarga_liberada = document.querySelector("#gripperLoaderReleased");
  const grippCarga_accionada = document.querySelector("#gripperLoaderActuated");
  const grippCarga_cupla = document.querySelector("#gripperLoaderCupla");
  const grippDescarga_atras = document.querySelector("#gripperDownloadBkwrd");
  const grippDescarga_adelante = document.querySelector("#gripperDownloadFwrd");
  const grippDescarga_liberada = document.querySelector("#gripperDownloadReleased");
  const grippDescarga_accionada = document.querySelector("#gripperDownloadActuated");
  const grippDescarga_cupla = document.querySelector("#gripperDownloadCupla");

  // Indicadores SERVO MOTORES
  const ejeLFwrdLim = document.querySelector("#axisLinearFwrd");
  const ejeLRvrseLim = document.querySelector("#axisLinearRvrse");
  const ejeLHomming = document.querySelector("#axisLinearHom");
  const ejeRhomming = document.querySelector("#axisRotativeHom");

  // Indicadores VERTICAL Y GIRO DE CARGA
  const vertCarga_arriba = document.querySelector("#verticalLoadUp");
  const vertCarga_abajo = document.querySelector("#verticalLoadDown");
  const giroCarga_arriba = document.querySelector("#turnLoadUp");
  const giroCarga_abajo = document.querySelector("#turnLoadDown");

  // Indicadores GRIPPER 2 DESCARGA
  const gripp2VDescarga_arriba = document.querySelector("#gripper2VerticalDownloaderUp");
  const gripp2VDescarga_abajo = document.querySelector("#gripper2VerticalDownloaderDown");
  const gripp2HDescarga_adelante = document.querySelector("#gripper2HorizontalDownloaderFwrd");
  const gripp2HDescarga_atras = document.querySelector("#gripper2HorizontalDownloaderBkwrd");
  const gripp2PDescarga_accionada = document.querySelector("#gripper2DownloaderActuated");
  const gripp2PDescarga_liberada = document.querySelector("#gripper2DownloaderReleased");

  // Indicadores GIRO DESCARGA
  const giroDescarga_arriba = document.querySelector("#turnDownloadUp");
  const giroDescarga_abajo = document.querySelector("#turnDownloadDown");







  const componenteMonitor = document.getElementsByClassName(" ");
 //console.log("Flags Fin V: ", dataWs.states.vertical.flags_fin.toString(2).split(''), dataWs.states.vertical.flags_fin) 
 //console.log("Flags Fin H: ", dataWs.states.horizontal.flags_fin.toString(2).split(''), dataWs.states.horizontal.flags_fin)
 console.log("Estado VER: ", dataWs.states.vertical.estado.toString(2).split(''), dataWs.states.vertical.estado) 
 console.log("Estado HOR: ", dataWs.states.horizontal.estado.toString(2).split(''), dataWs.states.horizontal.estado) 
  dataWs.states.ctrl.digin_0.toString(2)[10] == 1
    ? (sensorCuchillaIZq.className = "led led-green")
    : (sensorCuchillaIZq.className = "led led-grey");

  dataWs.states.ctrl.digin_1.toString(2)[10] == 1
    ? (sensorCuchillaDer.className = "led led-green")
    : (sensorCuchillaDer.className = "led led-grey");

  dataWs.states.ctrl.digin_0.toString(2)[9] == 1
    ? (rotPosIzq1.className = "led led-green")
    : (rotPosIzq1.className = "led led-grey");

  dataWs.states.ctrl.digin_1.toString(2)[9] == 1
    ? (rotPosDer1.className = "led led-green")
    : (rotPosDer1.className = "led led-grey");

  dataWs.states.ctrl.digin_0.toString(2)[8] == 1
    ? (rotPosIzq2.className = "led led-green")
    : (rotPosIzq2.className = "led led-grey");

  dataWs.states.ctrl.digin_1.toString(2)[8] == 1
    ? (rotPosDer2.className = "led led-green")
    : (rotPosDer2.className = "led led-grey");

  dataWs.states.ctrl.digin_0.toString(2)[7] == 1
    ? (liftPosIzq1.className = "led led-green")
    : (liftPosIzq1.className = "led led-grey");

  dataWs.states.ctrl.digin_1.toString(2)[7] == 1
    ? (liftPosDer1.className = "led led-green")
    : (liftPosDer1.className = "led led-grey");

  dataWs.states.ctrl.digin_0.toString(2)[6] == 1
    ? (liftPosIzq2.className = "led led-green")
    : (liftPosIzq2.className = "led led-grey");

  dataWs.states.ctrl.digin_1.toString(2)[6] == 1
    ? (liftPosDer2.className = "led led-green")
    : (liftPosDer2.className = "led led-grey");

  dataWs.states.ctrl.digin_0.toString(2)[5] == 1
    ? (grippPosIzq1.className = "led led-green")
    : (grippPosIzq1.className = "led led-grey");

  dataWs.states.ctrl.digin_1.toString(2)[5] == 1
    ? (grippPosDer1.className = "led led-green")
    : (grippPosDer1.className = "led led-grey");

  dataWs.states.ctrl.digin_0.toString(2)[4] == 1
    ? (grippPosIzq2.className = "led led-green")
    : (grippPosIzq2.className = "led led-grey");

  dataWs.states.ctrl.digin_1.toString(2)[4] == 1
    ? (grippPosDer2.className = "led led-green")
    : (grippPosDer2.className = "led led-grey");

  dataWs.states.ctrl.digin_0.toString(2)[3] == 1
    ? (grippShfPosIzq1.className = "led led-green")
    : (grippShfPosIzq1.className = "led led-grey");

  dataWs.states.ctrl.digin_1.toString(2)[3] == 1
    ? (grippShfPosDer1.className = "led led-green")
    : (grippShfPosDer1.className = "led led-grey");

  dataWs.states.ctrl.digin_0.toString(2)[2] == 1
    ? (grippShfPosIzq2.className = "led led-green")
    : (grippShfPosIzq2.className = "led led-grey");

  dataWs.states.ctrl.digin_1.toString(2)[2] == 1
    ? (grippShfPosDer2.className = "led led-green")
    : (grippShfPosDer2.className = "led led-grey");

  dataWs.states.ctrl.digin_0.toString(2)[1] == 1
    ? (bladeRestLeftDown.className = "led led-green")
    : (bladeRestLeftDown.className = "led led-grey");

  dataWs.states.ctrl.digin_1.toString(2)[1] == 1
    ? (bladeRestRightDown.className = "led led-green")
    : (bladeRestRightDown.className = "led led-grey");

  dataWs.states.ctrl.digin_0.toString(2)[0] == 1
    ? (bladeRestLeftUp.className = "led led-green")
    : (bladeRestLeftUp.className = "led led-grey");

  dataWs.states.ctrl.digin_1.toString(2)[0] == 1
    ? (bladeRestRightUp.className = "led led-green")
    : (bladeRestRightUp.className = "led led-grey");
}

export default () => {
  const divElement = document.createElement("div");
  divElement.className = "px-2 container-fluid";
  divElement.innerHTML = views;

 
  return divElement;
};
