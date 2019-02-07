import java.util.HashMap;
import java.util.Map;

/**
 * Rechnerobjekt, welches sich die aktuelle Seitenzahl merkt und alle Aufgaben als abfragbare Objekte in sich sammelt
 */
public class Rechner {
    private int aktSeite;
    private int maxFragen;
    private HashMap<Integer, Aufgabe> aufgaben;

    public Rechner(int maxFragen) {
        this.aktSeite = 1;
        this.maxFragen = maxFragen;
        aufgaben = new HashMap<>();

    }

    //Erstellt je nach Seitenzahl aufgaben und speichert diese direkt mit Ergebnis zwischen
    public Aufgabe getAktAufgabe() {
        int zahl1 = (int) ((Math.random()) * kopfrechentrainer.maxZahl + 1);
        int zahl2 = (int) ((Math.random()) * kopfrechentrainer.maxZahl + 1);

        if (aufgaben.get(aktSeite) == null && this.aktSeite <= maxFragen / 2) {
            Aufgabe a = new Aufgabe(Integer.toString(zahl1) + " + " + Integer.toString(zahl2), zahl1 + zahl2);
            aufgaben.put(aktSeite, a);
            return aufgaben.get(aktSeite);
        } else if (aufgaben.get(aktSeite) == null) {
            Aufgabe a = new Aufgabe(Integer.toString(zahl1) + " * " + Integer.toString(zahl2), zahl1 * zahl2);
            aufgaben.put(aktSeite, a);
            return aufgaben.get(aktSeite);
        } else
            return aufgaben.get(aktSeite);


    }

    public int getAktSeite() {
        return aktSeite;
    }

    public void naechsteSeite() {
        aktSeite++;
    }

    public int giveFortschritt() {
        return aktSeite * 100 / maxFragen;
    }

    public HashMap<Integer, Aufgabe> getAllAufgaben() {
        return this.aufgaben;
    }
}
