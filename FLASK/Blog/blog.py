#!user/bin/python3
import os
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
import time
from urllib import parse



def show_home():
    bloglist = []

    for file in os.listdir("blogs/"):
        if file.endswith(".blog"):
            name = file[:-5]
            li = "<li> <a href='%(link)s'> %(name)s </a> </li>"
            li %= {"link": "/" + name, "name": name.capitalize()}
            bloglist.append(li)

    bloghtml = "".join(bloglist) #auflistung

    a = str(open("static/home.tpl").read()) % {"blogs_list": bloghtml},

    response = Response(a, content_type="text/html")
    return response



def showBlog(blogname):
    a = str(open("static/eintrag.tpl").read()) % {"blogname": blogname.capitalize(),
                                                  "content": open("blogs/" + blogname + ".blog").read(),
                                                  "kommentare": showcomments(blogname),
                                                  "kommentarInput": open("static/comment.tpl").read() }


    response = Response(a, content_type="text/html")

    return response

def show404(blogname):
    a = str(open("static/404.tpl").read()) % {"blogname": blogname.capitalize()},
    response = Response(a, content_type="text/html")
    return response


def blogexists(name):
    for file in os.listdir("blogs/"):
        if name == file[:-5]:
            return True
    return False

def showcomments(blogname):
    comments = open("blogs/"+blogname+".comments").readlines()
    a = "<li>Kommentar vom %(datum)s: </br> %(kommentar)s</li> </br>"
    b = " "
    for ele in comments:
        comment = ele.split("===:===")
        print(comment)
        datum = comment[0]
        text = comment[1]
        b += str(a %{"datum": datum, "kommentar":text})
    return b

def writeComments(comment, blogname):
    zeit = str(time.strftime("%d.%m.%Y %H:%M:%S"))

    with open("blogs/" + blogname + ".comments", "a") as file:
        file.writelines(zeit + "===:===" + comment + "\n")


def checkForComments(environ, request):
    form = request.form
    if len(form) > 0:
        comment = str(form["kommentar"])
        blogname = request.path
        writeComments(comment, blogname)
    else:
        return None





def app(environ, start_response):
    request = Request(environ)
    pfad = request.path[1:]
    response = Response


    #check if there is a new comment:
    checkForComments(environ, request)


    if request.path == "/":
        response = show_home()
    else:
        if blogexists(pfad):
            response = showBlog(pfad)
        else:
            response = show404(pfad)

    return response(environ, start_response)




if __name__ == "__main__":
    run_simple('localhost', 8080, app, use_reloader=True, use_debugger=True)