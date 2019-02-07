#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import randint
import cgi, cgitb
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach()) #UTF8
cgitb.enable() #fehlermeldungsansicht


#Erzeugt die Aufgaben und liefert das Tupel mit Aufgabe und Ergebnis, nach 3 Aufgaben wechselt er zu *
def rechner(seitenzahl):
    zahl1 = randint(0, 10)
    zahl2 = randint(0, 10)

    if seitenzahl < 4:
        return (str(zahl1) + " + " + str(zahl2) + " = ", str(zahl1+zahl2))
    elif seitenzahl > 3 and seitenzahl <7:
        return (str(zahl1) + " * " + str(zahl2) + " = ", str(zahl1*zahl2))
    if seitenzahl == 7:
        return (" ", " ")

#Erzeugt immer 6 inputs, das aktuelle wird auf sichtbar gestellt
def erzeugeInputs(query_string, seitenzahl, ergebnis):
    inputs = []

    if seitenzahl == 7:
        return erzeugeErgebnisseite(query_string)

    for i in range(1, 7):
        if i < seitenzahl: #Alle schon beantworteten Fragen ziehe aus Query
            inputs.append(createInput(i, query_string[str(i)].value, False))
        if i > seitenzahl: #Alle noch unbeantworteten Fragen fuelle mit leer
            inputs.append(createInput(i, "", False))
        if i == seitenzahl: #DAS Aktuelle Feld mache sichtbar, jedoch noch ohne Inhalt
            inputs.append(createInput(i, "", True))


    #Abschicken Button anhängen
    inputs.append("""<input type="submit" value="Abschicken" />""")
    s = " "

    return s.join(inputs)


#hilfsmethode zum erzeugen der Inputs
def createInput(pos, value, show):
    type = "hidden"
    if show:
        type = "text"

    return """<input type="%s" value="%s" name="%s" />""" %(type, value, pos)

#Wird auf der letzten Seite aufgerufen
def erzeugeErgebnisseite(query):
    s = """
    <h1> Ergebnisse </h1>
    """
    return s



def g(key, query_string):
    if key in query_string:
        return query_string[key]
    else:
        return ""



if __name__ == "__main__":
    print("Content-Type: text/html\n\n")  # html markup follows

    form = cgi.FieldStorage()
    seitenzahl = int(len(form))+1
    aufgabe = rechner(seitenzahl)


    print("""
    <!doctype html>
    <html>
        <head>
            <meta charset="utf-8" />
        </head>

        <body>
            <h1> Mein Ultra, Üüüüüäöbertrieben guter Kopfrechentrainer </h1>
            %s
            <form style="display: inline" action="kopfrechner.cgi" method="get">

            %s

            </form>
            <br/> <br/> <br/>
            Seite: %s



        </body>
    </html>
    """ % (aufgabe[0], erzeugeInputs(form, seitenzahl, aufgabe[1]), seitenzahl))
