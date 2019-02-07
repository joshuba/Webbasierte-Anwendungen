#!usr/bin/python3

from random import randint
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from urllib import parse #so in python3 :)
import http.cookies # umbenannt in Python 3


#Schreibt nach jedem Aufruf den Context in die Cookies
def render_context(content, context, last):
    response = Response(content, content_type="text/html")

    for k,v in context.items(): #in python 3 items nicht iteritems...
        response.set_cookie(k,v)
        if last:
            response.set_cookie(k, expires=0) #löscht cookies an bestimmter stelle
    return response



#erstellt die Aufgaben
def erstelleAufgabe(seitenzahl):
    zahl1 = randint(0, 10)
    zahl2 = randint(0, 10)

    if seitenzahl < 4:
        return (str(zahl1) + " + " + str(zahl2) + " = ", str(zahl1+zahl2))
    elif seitenzahl > 3 and seitenzahl <7:
        return (str(zahl1) + " * " + str(zahl2) + " = ", str(zahl1*zahl2))
    if seitenzahl == 7:
        return (" ", " ")



def zeigeAufgabenseite(args, seite, form):

    content = ""
    content += "Aufgabe Nr. " + args["seite"] + "</br> </br> </br>"

    a = erstelleAufgabe(seite)
    content += a[0]  # nur die aufgabe
    args[str(seite) + "A"] = str(a[0])  # Aufgabe mit einem A makiert z.B. 1A für Ergebnisseite
    args[str(seite) + "L"] = str(a[1])  # loesung mit einem L makiert z.B. 1L
    print(args)

    content += """<form style="display: inline" action="Kopfrechner.wsgi" method="get">"""  #Form
    content += """<input type="text" value="" name="eingabe" />"""#Feld
    content += """<input type ="submit" "name = "ok" value="Weiter" /> </form>"""  #Button

    # zaehle seite hoch
    args["seite"] = str(int(args["seite"]) + 1)
    page = loadHtmlTemplates(content)
    response = render_context(page, args, False)  # false = cookies nicht löschen
    return response




def zeigeErgebnisse(args):
    content = ""
    p =""

    for i in range(1,7):
        #Falls keine Antwort gegeben wurde
        if str(i) not in args:
            p = "__"
        else:
            p = args[str(i)]
        content += str(args[str(i)+"A"]) + p



        if p == (args[str(i)+"L"]):
            content += "    -> RICHTIG</br>"
        else:
            content += "-> FALSCH -> " +str(args[str(i)+"L"]) + "</br>"


    content += """<form style="display: inline" action="Kopfrechner.wsgi" method="get">"""  # Form
    content += """<input type ="submit" "name = "ok" value="Neue Runde" /> </form>"""  # Button

    page = loadHtmlTemplates(content)
    response = render_context(page, args, True)  # löscht die Cookies wieder auf der letzten seite
    return response





def app(environ, start_response):
    request = Request(environ)

    # aktuelle cookies in einem DIC
    args = dict(request.cookies)

    #Seitenzahlen
    if "seite" not in args:
        args['seite'] = "1"
    seite = int(args["seite"])

    #Query String der Eingaben (Immer um 1 versetzt)
    form = parse.parse_qs(environ['QUERY_STRING'])
    # ziehe QueryString mit letzter Eingabe
    # schreibe letzte antwort an die jeweils richtige stelle (Immer um eine Seite verzoegert)
    if "eingabe" in form:
        args[str(seite - 1)] = str(form["eingabe"][0])



    #Erzeuge je nach Seitenzahl die Ensprechende Seite
    if seite != 7:
        response = zeigeAufgabenseite(args, seite, form)
    else:
        response = zeigeErgebnisse(args)


    return response(environ, start_response)





def loadHtmlTemplates(content):
    with open("Static_Page.tpl", "r") as f:
        return str(f.read()) % {"title": "Kopfrechner", "ueberschrift": "Der WSGI-🍪-Megakrasse Kopfrechentrainer, Vorsicht: Hier werden ihre Cookies penetriert", "content": content}




if __name__ == "__main__":
    run_simple('localhost', 8080, app, use_reloader=True, use_debugger=True)