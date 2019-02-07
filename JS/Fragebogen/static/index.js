window.onload = function () {
    loadBoegen();
    document.getElementById("startButton").onclick = weiterleiten;


    //über
    function loadBoegen() {
        var req = new XMLHttpRequest;


        req.onload = function () {
            if (this.status === 200) {
                addFrageboegen(JSON.parse(this.response));
            }
        };

        req.open("GET", "/frageboegen");
        req.send();
    }


    function addFrageboegen(response) {
        var dropDown = document.querySelector("#dropdown"),
            select = document.createElement("select");
            select.setAttribute("id","dropdownSelect")

        for (var key in response) {
            select.options.add(new Option(response[key]));
        }

        dropDown.appendChild(select);
    }

    function weiterleiten() {
        var req = new XMLHttpRequest;

        req.onload = function () {
            window.location = "/"
        }
        req.open("POST", "/setBogen", true);

        var dropdown = document.getElementById("dropdownSelect");
        req.send(dropdown.options[dropdown.selectedIndex].value);


    }


}