//import { env } from "./enviroments";

export async function SemiAutomatico(comando, menu, modo, eje) {
  const continuar = document.getElementById("continue");
  const response = await fetch(env.URL_BASE + "menu/" + modo + "/", {
    method: "post",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({ menu: menu, comando: comando, eje }),
  });
  // response.status === 200
  //   ? (continuar.className = "btn btn-secondary btn-lg disabled")
  //   : "";
}
