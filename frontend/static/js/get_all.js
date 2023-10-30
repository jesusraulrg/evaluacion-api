function getAll() {
    var request = new XMLHttpRequest;
    request.open('GET',"http://localhost:8000/contactos");
    request.send();

    request.onload = (e) => {
        const response = request.responseText;
        const json = JSON.parse(response);
        console.log("response: " + response);
        console.log("json: " + json);
        console.log("status_code: " + request.status);

        console.log("Email: " + json[0]["email"]);
        console.log("Nombre: " + json[0]["nombre"]);
        console.log("Teléfono: " + json[0]["telefono"]);

        const tbody_contactos = document.getElementById("tbody_contactos");

        var tr = document.createElement("tr");
        var td_email = document.createElement("td");
        var td_nombre = document.createElement("td");
        var td_telefono = document.createElement("td");

        td_email.innerHTML = json[1]["email"];
        td_nombre.innerHTML = json[1]["nombre"];
        td_telefono = json[1]["telefono"];

        tr.appendChild(td_email);
    };
};
