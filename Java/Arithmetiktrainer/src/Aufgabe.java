/**
 * Diese Klasse bildet eine Matheaufgabe mit Ergebnis und Antwort ab
 */
public class Aufgabe {
    private String aufgabe;
    private int antwort;
    private int richtigesErgebnis;

    public Aufgabe(String aufgabe, int richtigesErgebnis) {
        this.aufgabe = aufgabe;
        this.richtigesErgebnis = richtigesErgebnis;
    }

    public void setRichtigesErgebnis(int richtigesErgebnis) {
        this.richtigesErgebnis = richtigesErgebnis;
    }

    public int getAntwort() {
        return this.antwort;
    }

    public int getRichtigesErgebnis() {
        return this.richtigesErgebnis;
    }

    public String getAufgabe() {
        return this.aufgabe;
    }

    public void setAntwort(int antwort) {
        this.antwort = antwort;
    }
}
