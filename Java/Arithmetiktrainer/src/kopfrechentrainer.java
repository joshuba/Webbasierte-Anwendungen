import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

/**
 * Hauptklasse, wird bei bei jedem Neuladen aufgerufen
 */
public class kopfrechentrainer extends HttpServlet {
    static int maxZahl = 0;
    static int maxAufgaben = 0;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        readXMLValues(); //liest die statischen Variablen aus der WebXML ein
        HttpSession session = request.getSession();

        //Erstellt ein Rechnerobjekt und speichert dieses direkt in der aktuellen Session
        if (session.isNew()) {
            session.setAttribute("rechner", new Rechner(maxAufgaben));
        }

        //Leite weiter an doPost, um die ergebnisse abzufangen
        doPost(request, response);


    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {

        //Falls "neu" gesetzt, lösche die Session und beginne von vorne
        if (req.getParameter("neu") != null && req.getParameter("neu").equals("ja")) {
            req.removeAttribute("neu");
            req.getSession().invalidate();
            resp.sendRedirect("/");
            return; //macht man so
        } else {
            //Ziehe aktuelles Rechnerobjekt aus Session
            Rechner r = (Rechner) req.getSession().getAttribute("rechner");


            //Wenn die aktuelle seitennummer schon ein ergebniseintrag hat (schon beantwortet wurde)
            if (req.getParameter(Integer.toString(r.getAktSeite())) != null) {
                r.getAktAufgabe().setAntwort(Integer.parseInt(req.getParameter(Integer.toString(r.getAktSeite())))); //Setze das ergebnis
                r.naechsteSeite(); //Zähle Seite im Rechnerobjekt um 1 hoch
            }
            System.out.println("doPost Aufruf 🙄");


            //Je nach Seitenzahl leite auf anderes Servlet weiter, halb addition, halb multiplikation
            if (r.getAktSeite() <= maxAufgaben / 2) {
                resp.sendRedirect("/plus");
            } else if (r.getAktSeite() <= maxAufgaben) {
                resp.sendRedirect("/mal");
            } else {
                resp.sendRedirect("/done");
            }
        }


    }


    public void readXMLValues() {
        Context env = null;

        try {
            env = (Context) new InitialContext().lookup("java:comp/env");
            maxZahl = (Integer) env.lookup("MaxZahl");
            maxAufgaben = (Integer) env.lookup("AnzAufgaben");

        } catch (NamingException e) {
            e.printStackTrace();
        }


    }
}
