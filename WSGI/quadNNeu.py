#!user/bin/python3

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response


def app(environ, start_response):
    request = Request(environ)

    n_args = request.args.get("n")
    n = 1000000

    if n_args:
        n = int(n_args)

    content = "".join([str(i**2) + " " for i in range(n)])
    page = loadHtmlTemplates(content)

    r = Response(page) #erwartet einen String
    r.content_type = "text/html"

    return r(environ, start_response)




def loadHtmlTemplates(content):
    with open("Static_Page.tpl", "r") as f:
        return str(f.read()) % {"title": "N", "ueberschrift": "Quadratzahlen", "content": content}



if __name__ == "__main__":
    run_simple('localhost', 8080, app, use_reloader=True, use_debugger=True)

