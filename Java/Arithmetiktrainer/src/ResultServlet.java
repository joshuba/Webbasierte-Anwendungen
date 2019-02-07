import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;

/**
 * erstellt eine Liste mit allen Ergebnissen aus dem Rechnerobjekt
 */
public class ResultServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        PrintWriter out = resp.getWriter();

        Rechner r = (Rechner) req.getSession().getAttribute("rechner");

        String a = new String(Files.readAllBytes(Paths.get("/Users/Josh/IdeaProjects/Web-Basierte-AnwendungenPrivate/Blatt 4/Arithmetiktrainer/web/WEB-INF/templates/results.html")));


        StringBuilder ergebnisse = new StringBuilder();
        HashMap<Integer, Aufgabe> aufgaben = r.getAllAufgaben();

        for (int i = 1; i <= kopfrechentrainer.maxAufgaben; i++) {
            String aufgabenstellung = aufgaben.get(i).getAufgabe();
            int antwort = aufgaben.get(i).getAntwort();
            int richtig = aufgaben.get(i).getRichtigesErgebnis();

            if (antwort == richtig) {
                ergebnisse.append("<li class=\"list-group-item list-group-item-success\">" + i + ".  " + aufgabenstellung
                        + " = " + antwort + " </li>");

            } else {
                ergebnisse.append("<li class=\"list-group-item list-group-item-danger\">" + i + ".  " + aufgabenstellung
                        + " = " + antwort + "  --> " + richtig + " </li>");


            }


        }

        String seite = String.format(a, "Deine Ergebnisse", ergebnisse);
        out.print(seite);


    }
}
