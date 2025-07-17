# MVP – STORASENSE

## Ziel des MVP

Ziel dieses Minimal Viable Products (MVP) ist die Entwicklung eines einfachen, funktionalen Systems zur Erfassung und Überwachung von Umweltdaten – konkret Temperatur und Luftfeuchtigkeit – über Sensoren, deren Messwerte gespeichert, ausgewertet und überwacht werden. Das System dient als Grundlage für eine spätere Erweiterung mit zusätzlichen Sensoren und Benachrichtigungsmechanismen.

## Systemüberblick

Das System basiert auf einer Hardwarekomponente (z. B. Arduino mit angeschlossenen Sensoren), welche die gemessenen Umweltdaten regelmäßig über das MQTT-Protokoll an einen Server übermittelt.

Die empfangenen Messwerte werden in einer permanenten Datenbank gespeichert und über eine grafische Benutzeroberfläche visualisiert. Darüber hinaus kann der Benutzer individuelle Schwellenwerte für Temperatur definieren. Wird ein definierter Temperaturbereich überschritten oder unterschritten, so wird automatisch eine Warnung ausgegeben und an den MQTT-Broker gesendet. Bei Grenzwertüberschreitungen wird zudem ein neues MQTT-Topic veröffentlicht, das von anderen Komponenten abonniert werden kann, um z. B. automatisierte Reaktionen auszulösen.

## Funktionale Anforderungen

- Das System misst regelmäßig die **Temperatur** und **Luftfeuchtigkeit** über angeschlossene Sensoren.
- Die Messergebnisse werden in einer **permanenten Datenbank** gespeichert.
- Der Benutzer kann über eine **grafische Benutzeroberfläche** einen **Temperatur-Mindestwert** und einen **Temperatur-Höchstwert** definieren.
- Liegt die gemessene Temperatur **außerhalb des definierten Bereichs**, wird automatisch eine **Warnung** erzeugt.
- Die Warnung wird über den **MQTT-Broker** veröffentlicht: Bei einer Grenzwertverletzung wird eine Nachricht auf ein dafür vorgesehenes **MQTT-Topic** geschickt, auf das andere Systeme oder Komponenten zugreifen können (z. B. zur Steuerung von Aktoren).
- Die Benutzeroberfläche stellt ein **aktives Dashboard** dar, das die aktuellen Sensordaten in Echtzeit visualisiert.

## Nicht-funktionale Anforderungen

- **Verfügbarkeit des Systems**:
    - Das System soll eine **Verfügbarkeit von 99% innerhlab eines Zeitraums von drei Tagen** aufweisen.
    - Falls das System abstürzt, wird es versuchen, sich **automatisch bis zu drei Mal in kurzen Abständen neu zu starten**.
- **Sicherheit des Systems**: Authentifizierung und Autorisierung
- **Performance des Systems**: Schnelles Alamierungssystem - Push-Benachrichtigung und MQTT-Benachrichtigung.

## Optionale Erweiterungen

Die folgenden Funktionen sind nicht Bestandteil des MVPs, können jedoch zu einem späteren Zeitpunkt ergänzt werden:

- **Sensor zur Erkennung von Kohlenwasserstoffen** zur Überwachung der Luftqualität
- **Ultraschallsensor zur Türüberwachung**, z. B. zur Anwesenheitserkennung oder Zutrittskontrolle
- **Benachrichtigung per Push-Nachricht** bei Grenzwertüberschreitungen oder anderen definierten Ereignissen

## System-FMEA Analyse
Folgende SFMEA-Analyse dient der Identifizierung potenzieller Schwachstellen des Systems - insbesondere des oben beschriebenen MVPs:
Zunächst wird das Gesamtsystem STORASENSE in seine Teilsysteme gegliedert und analysiert:

### 1. Teilsystem: Sensor-Einheit (Hardware):
Verantwortlich für die Erfassung der physikalischen Messwerte.

| Fehlermöglichkeit                        | Fehlerfolge (Auswirkung)                                                                 | B  | Fehlerursache                                                     | A  | Maßnahmen                                                                                                                                     | E  | RPZ |
|------------------------------------------|------------------------------------------------------------------------------------------|----|-------------------------------------------------------------------|----|-----------------------------------------------------------------------------------------------------------------------------------------------|----|-----|
| Sensor liefert dauerhaft falsche Werte   | Falsche Daten werden gespeichert; Alarme werden fälschlicherweise ausgelöst oder unterbleiben. | 9  | Sensor defekt oder dekalibriert; Programmierfehler beim Auslesen. | 4  | Plausibilitäts-Checks im Backend (z\.B\. Temperatur springt nicht von 10°C auf 50°C). Implementierung von Algorithmen zur Ausreißer-Erkennung | 5  | 180 |
| Mikrocontroller (Arduino) friert ein     | Keine neuen Messwerte werden mehr gesendet; Überwachung fällt komplett aus.              | 10 | Software-Bug (z.B. Endlosschleife); Speicherüberlauf.             | 3  | Hardware-Watchdog-Timer, der den Arduino automatisch neu startet (vgl. NF-Req Verfügbarkeit). Einsatz eines robusten Watchdog-Timers.         | 2  | 60  |
| Verlust der WLAN-Verbindung              | Keine neuen Messwerte werden an den MQTT-Broker gesendet.                                | 8  | WLAN-Router ausgefallen; falsches Passwort; schwaches Signal.     | 5  | Implementierte Wiederverbindungs-Logik auf dem Mikrocontroller (vgl. NF-Req Verfügbarkeit). Backend überwacht den Zeitstempel der letzten Nachricht pro Sensor und löst einen "Verbindungsverlust"-Alarm aus.                                                  | 3  | 120 |

### 2.

## Hinweise

Da es sich um ein MVP handelt, liegt der Fokus zunächst auf der Umsetzung der Kernfunktionen (Datenaufnahme, Speicherung, Warnung). Erweiterte Funktionalitäten, Sicherheit auf Anwendungsebene sowie Skalierbarkeit sind nicht Bestandteil des ersten Releases, können aber im Rahmen weiterer Iterationen realisiert werden.
