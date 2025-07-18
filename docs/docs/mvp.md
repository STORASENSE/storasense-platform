# MVP – STORASENSE

## Ziel des MVP

Ziel dieses Minimal Viable Products (MVP) ist die Entwicklung eines einfachen, funktionalen Systems zur Erfassung und Überwachung von Umweltdaten – konkret Temperatur und Luftfeuchtigkeit – über Sensoren, deren Messwerte gespeichert, ausgewertet und überwacht werden. Das System dient als Grundlage für eine spätere Erweiterung mit zusätzlichen Sensoren und Benachrichtigungsmechanismen.

## Systemüberblick

Das System basiert auf einer Hardwarekomponente (Arduino mit angeschlossenen Sensoren), welche die gemessenen Umweltdaten regelmäßig über das MQTT-Protokoll an einen Server übermittelt.

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
- **Performance des Systems**: Schnelles Alamierungssystem - Push-Benachrichtigung und MQTT-Benachrichtigung innerhalb von 90 Sekunden.

## Optionale Erweiterungen

Die folgenden Funktionen sind nicht Bestandteil des MVPs, können jedoch zu einem späteren Zeitpunkt ergänzt werden:

- **Sensor zur Erkennung von Kohlenwasserstoffen** zur Überwachung der Luftqualität
- **Ultraschallsensor zur Türüberwachung**, z. B. zur Anwesenheitserkennung oder Zutrittskontrolle
- **Benachrichtigung per Push-Nachricht** bei Grenzwertüberschreitungen oder anderen definierten Ereignissen

## Software-FMEA Analyse
Folgende SFMEA-Analyse dient der Identifizierung potenzieller Schwachstellen des Systems - insbesondere des oben beschriebenen MVPs:
Dafür wird das Gesamtsystem STORASENSE in seine Teilsysteme gegliedert und analysiert:

### Legende:
**Bedeutung (B)**: Auswirkung des Fehlers (1 = keine Auswirkung, 10 = totaler Schaden)

**Auftreten (A)**: Wahrscheinlichkeit des Auftretens der Ursache (1 = sehr unwahrscheinlich, 10 = sehr wahrscheinlich)

**Entdeckung (E)**: Wahrscheinlichkeit, dass der Fehler entdeckt wird, bevor er Schaden anrichtet (1 = sehr wahrscheinlich entdeckt, 10 = nicht zu entdecken)

**Risikoprioritätszahl (RPZ)**: B × A × E (hoher Wert = Handlungsbedarf)

### 1. Teilsystem: Sensor-Einheit (Hardware):
Verantwortlich für die Erfassung der physikalischen Messwerte.

| Fehlermöglichkeit                        | Fehlerauswirkung                                                                           | B  | Fehlerursache                                                        | A  | Maßnahmen                                                                                                                                     | E  | RPZ |
|------------------------------------------|--------------------------------------------------------------------------------------------|----|----------------------------------------------------------------------|----|-----------------------------------------------------------------------------------------------------------------------------------------------|----|-----|
| Sensor liefert dauerhaft falsche Werte   | Falsche Daten werden gespeichert; Alarme werden fälschlicherweise ausgelöst oder gar nicht. | 9  | Sensor defekt oder Programmierfehler beim Auslesen.                  | 4  | Plausibilitäts-Checks im Backend (z\.B\. Temperatur springt nicht von 10°C auf 50°C). Implementierung von Algorithmen zur Ausreißer-Erkennung | 5  | 180 |
| Mikrocontroller (Arduino) friert ein     | Keine neuen Messwerte werden mehr gesendet und Überwachung fällt komplett aus.             | 10 | Software-Bug (z.B. Endlosschleife) oder Speicherüberlauf.            | 3  | Hardware-Watchdog-Timer, der den Arduino automatisch neu startet (vgl. NF-Req Verfügbarkeit). Einsatz eines robusten Watchdog-Timers.         | 2  | 60  |
| Verlust der WLAN-Verbindung              | Keine neuen Messwerte werden an den MQTT-Broker gesendet.                                  | 8  | WLAN-Router ausgefallen oder falsches Passwort. | 5  | Implementierte Wiederverbindungs-Logik auf dem Mikrocontroller (vgl. NF-Req Verfügbarkeit). Backend überwacht den Zeitstempel der letzten Nachricht pro Sensor und löst einen "Verbindungsverlust"-Alarm aus.                                                  | 3  | 120 |

### 2. Teilsystem: Backend (FastAPI-Anwendung)
Verantwortlich für die Datenverarbeitung, Speicherung, Alarmierung und API-Bereitstellung.

| Fehlermöglichkeit                        | Fehlerauswirkung                                                                                                                | B  | Fehlerursache                                                                                   | A  | Maßnahmen                                                                                                                                                                                                                                                     | E  | RPZ |
|------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|----|-------------------------------------------------------------------------------------------------|----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----|-----|
| FastAPI-Anwendung stürzt ab              | Das gesamte System ist offline.                                                                                                 | 10 | Unbehandelter Fehler im Code (z.B. TypeError).                                                  | 4  | Einsatz eines Prozess-Managers (z.B. systemd), der die Anwendung bei einem Absturz automatisch neu startet. Implementierung eines zentralen Logging-Systems (zur Analyse der Absturzursache) und Einrichten eines HEALTH-API-Endpunktes.                      | 2  | 80  |
| Verbindung zur Datenbank (MongoDB/SQLite) geht verloren | Eingehende Messwerte können nicht gespeichert werden; Nutzer können sich nicht anmelden oder Daten abrufen.                     | 8  | Datenbank-Server ist offline; Netzwerkproblem bzw Docker-Problem; falsche Zugangsdaten.         | 3  | Fehlerbehandlung (try-except Exception Handling) im Code; Wiederverbindungs-Logik im Datenbanktreiber. | 4  | 96  |
| Alarm wird nicht ausgelöst                | Ein kritischer Zustand (z.B. zu hohe Temperatur) wird erkannt, aber der Nutzer wird nicht benachrichtigt. Der Schaden passiert. | 10 | Fehler im Alarmierungs-Code; externer E-Mail/Push-Dienst ist ausgefallen; falsche Konfiguration. | 2  | Unit-Tests für die Alarm-Logik.                                                                                                                    | 6  | 120 |


## Hinweise

Da es sich um ein MVP handelt, liegt der Fokus zunächst auf der Umsetzung der Kernfunktionen (Datenaufnahme, Speicherung, Warnung). Erweiterte Funktionalitäten, Sicherheit auf Anwendungsebene sowie Skalierbarkeit sind nicht Bestandteil des ersten Releases, können aber im Rahmen weiterer Iterationen realisiert werden.
