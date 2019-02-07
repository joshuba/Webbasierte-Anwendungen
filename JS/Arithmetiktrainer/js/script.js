/**
 * Created by Josh on 16.07.17.
 */

const anzMult = 3;
const anzAdd = 3;
const maxZahl = 10;
const minZahl = 0;

window.onload = function () {
    var rechner = new Rechner(minZahl, maxZahl);
    sessionStorage.setItem("nummer", 0);

    next();


    document.getElementById("nextButton").onclick = next;


    //methode
    function next() {
        if (sessionStorage.getItem("nummer") != 0) { //Wenn bereits eine Aufgabe gestellt wurde
            // Eingabe
            var eingabe = document.getElementById("eingabe").value;
            if (eingabe.length === 0) { //Falls Eingabefeld 0
                alert("Bitte ein Antwort eingeben!");
            } else {
                //Setze ergebnis aus letzter Aufgabe
                rechner.aktAufgabe.eingabe = eingabe;
                naechsteAufgabe();
            }

        } else { //Beim Starten
            naechsteAufgabe();

        }


    }

    function naechsteAufgabe() {
        //Nächste Aufgabe
        sessionStorage.setItem("nummer", parseInt(sessionStorage.getItem("nummer")) + 1); //erhohe Aufgabennummer
        var nummer = sessionStorage.getItem("nummer");
        //aktualisiere Seitenzahl
        document.getElementById("seitenzahl").innerHTML = "Seite " + nummer;


        //Stelle nächste Aufgabe
        if (nummer < anzAdd) {
            rechner.aktAufgabe = rechner.nextAdd();
            rechner.alleAufgaben.push(rechner.aktAufgabe)
            document.getElementById("aufgabe").innerHTML = rechner.aktAufgabe.aufgabe;


        } else if (nummer > anzAdd && nummer < (anzAdd + anzMult)) {
            rechner.aktAufgabe = rechner.nextMult();
            rechner.alleAufgaben.push(rechner.aktAufgabe)
            document.getElementById("aufgabe").innerHTML = rechner.aktAufgabe.aufgabe;

        } else if (nummer > (anzAdd + anzMult)) {
            showErgebnis();
        }


    }

    function showErgebnis() {
        var nummer = sessionStorage.getItem("nummer");


        //Lösche Aufgabenelemente
        var element = document.getElementById("rechner");
        while (element.firstChild) {
            element.removeChild(element.firstChild);
        }

        var ueberschrift = document.createElement("h1");
        ueberschrift.innerHTML = "Ergebnisse";
        element.appendChild(ueberschrift);


        //Erstelle Tabelle
        var myTable = document.createElement("table");
        element.appendChild(myTable);


        for(var i = 0; i<nummer; i++){
            var zeile = document.createElement("tr");
            var aufgabe = document.createElement("td");
            var eingabe = document.createElement("td");
            var loesung = document.createElement("td");



            aufgabe.innerHTML = rechner.alleAufgaben[i].aufgabe;
            eingabe.innerHTML = rechner.alleAufgaben[i].eingabe;
            loesung.innerHTML = rechner.alleAufgaben[i].loesung;


            myTable.appendChild(zeile);
            zeile.appendChild(aufgabe);
            zeile.appendChild(eingabe);
            zeile.appendChild(loesung);




        }






    }


    //Aufgabenobjekt
    function Aufgabe(aufgabe, loesung) {
        this.aufgabe = aufgabe;
        this.loesung = loesung;
        this.eingabe = undefined;
    }

    //Rechnerobjekt
    function Rechner(minZahl, maxZahl) {
        this.aktAufgabe = undefined;
        this.alleAufgaben = [];


        this.nextMult = function () {
            zahl1 = Math.round(Math.random() * (maxZahl - minZahl) + minZahl);
            zahl2 = Math.round(Math.random() * (maxZahl - minZahl) + minZahl);

            return new Aufgabe(zahl1 + " * " + zahl2 + " =", zahl1 * zahl2);
        }

        this.nextAdd = function () {
            zahl1 = Math.round(Math.random() * (maxZahl - minZahl) + minZahl);
            zahl2 = Math.round(Math.random() * (maxZahl - minZahl) + minZahl);

            return new Aufgabe(zahl1 + " + " + zahl2 + " =", zahl1 + zahl2);
        }

        this.istRichtig = function () {
            if (this.aktAufgabe.eingabe == this.aktAufgabe.loesung) {
                return true;
            } else {

                return false;
            }
        }


    }


}



