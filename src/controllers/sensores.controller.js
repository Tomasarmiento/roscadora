import views from "../views/sensores.html";

export function MonitorearSensores(dataWs) {
  // Indicadores ROTADOR
  const rotPosDer1 = document.querySelector("#rotRightPos1");
  const rotPosIzq1 = document.querySelector("#rotLeftPos1");
  const rotPosDer2 = document.querySelector("#rotRightPos2");
  const rotPosIzq2 = document.querySelector("#rotLeftPos2");

  // Indicadores ELEVADOR
  const liftPosDer1 = document.querySelector("#liftRightPos1");
  const liftPosIzq1 = document.querySelector("#liftLeftPos1");
  const liftPosDer2 = document.querySelector("#liftRightPos2");
  const liftPosIzq2 = document.querySelector("#liftLeftPos2");

  // Indicadores Gripper
  const grippPosDer1 = document.querySelector("#gripperRightPos1");
  const grippPosIzq1 = document.querySelector("#gripperLeftPos1");
  const grippPosDer2 = document.querySelector("#gripperRightPos2");
  const grippPosIzq2 = document.querySelector("#gripperLeftPos2");

  // Indicadores Avance de Grippers
  const bladeRestRightUp = document.querySelector("#bladeRestRightUp");
  const bladeRestRightDown = document.querySelector("#bladeRestRightDown");
  const bladeRestLeftUp = document.querySelector("#bladeRestLeftUp");
  const bladeRestLeftDown = document.querySelector("#bladeRestLeftDown");

  // Indicadores Avance de Grippers
  const grippShfPosDer1 = document.querySelector("#gripperShiftRightPos1");
  const grippShfPosIzq1 = document.querySelector("#gripperShiftLeftPos1");
  const grippShfPosDer2 = document.querySelector("#gripperShiftRightPos2");
  const grippShfPosIzq2 = document.querySelector("#gripperShiftLeftPos2");

  // Indicadores CUCHILLA
  const sensorCuchillaDer = document.querySelector("#bladePresenceRight");
  const sensorCuchillaIZq = document.querySelector("#bladePresenceLeft"); 

  const componenteMonitor = document.getElementsByClassName("sensores");
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
