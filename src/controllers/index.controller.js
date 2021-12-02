import Automatico from "./automatico.controller";
import Referenciar from "./referenciar.controller";
import Home from "./home.controller";
import Semiautomatico from "./semiautomatico.controller";
import NeumaticaManual from "./neumaticaManual.controller";
import MotoresManual from "./motoresManual.controller";
import Sensores from "./sensores.controller";
import MonitorEstados from "./monitorEstados.controller";
import ParametrosP1 from "./parametrosP1.controller";
import ParametrosP2 from "./parametrosP2.controller";


const pages = {
  home: Home,
  automatico: Automatico,
  referenciar: Referenciar,
  semiautomatico: Semiautomatico,
  neumaticaManual: NeumaticaManual,
  motoresManual: MotoresManual,
  sensores: Sensores,
  monitorEstados: MonitorEstados,
  parametrosP1: ParametrosP1,
  parametrosP2: ParametrosP2,
};

export { pages };
