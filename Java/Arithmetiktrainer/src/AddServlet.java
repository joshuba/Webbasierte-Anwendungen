import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;

/**
 * wird nur bei Additionen aufgerufen, füllt das index.html template
 */
public class AddServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        PrintWriter out = resp.getWriter();

        Rechner r = (Rechner) req.getSession().getAttribute("rechner");

        String a = new String(Files.readAllBytes(Paths.get("/Users/Josh/IdeaProjects/Web-Basierte-AnwendungenPrivate/Blatt 4/Arithmetiktrainer/web/WEB-INF/templates/index.html")));
        String seite = String.format(a, "Addition", r.getAktAufgabe().getAufgabe(), r.getAktSeite(), Integer.toString(r.giveFortschritt()) + "%", r.getAktSeite(), kopfrechentrainer.maxAufgaben);
        out.print(seite);


    }

}