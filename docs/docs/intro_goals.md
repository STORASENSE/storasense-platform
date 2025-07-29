
# Einführung und Ziele

Ziel dieses Projekts ist die Entwicklung eines softwaregestützten Überwachungssystems zur kontinuierlichen Kontrolle der Umgebungsbedingungen in Lagerräumen.
Das System dient der Qualitätssicherung und Verlustprävention bei der Lagerung verderblicher oder sensibler Güter, die spezifische klimatische Bedingungen erfordern.

Der primäre Anwendungsbereich umfasst die Überwachung von Lagern für wertvolle Güter – wie beispielsweise Lebensmittel oder Pharmazeutika - , deren Qualität von insbesondere folgenden Faktoren abhängig ist:

**Temperatur**: Einhaltung eines konstanten, kühlen Niveaus. <br>
**Luftfeuchtigkeit**: Vermeidung von zu hoher oder zu niedriger Feuchtigkeit. <br>
**Luftqualität**: Sicherstellung einer reinen, insbesondere von Schadstoffen freien Umgebung. <br>
Weiter erfolgt die Kontrolle des Lagerraums im Zuge der Überwachung des Zustandes der Eingangstür (offen / geschlossen).

# Aufgabenstellung
Es gilt ein System zu entwickeln, das sowohl aus Hardware- als auch aus Softwarekomponenten besteht, die ineinandergreifen.

**Sensorik (Hardware)**: Ein Netzwerk von IoT erfasst die physikalischen Messgrößen alle 30 Sekunden.

* Temperatursensor (2x): Messung der Raumtemperatur (Innen- und Außen- Raum) in Celsius.
* Luftfeuchtigkeitssensor: Erfassung der relativen Luftfeuchtigkeit (in %).
* Luftqualitätssensor: Detektion von Verunreinigungen in der Luft.
* Ultraschallsensor: Zur Überprüfung des Zustandes der Tür – ist die Tür offen oder geschlossen.

**Software-Plattform (Kernsystem)**: Eine zentrale Anwendung, die folgende Funktionalitäten bereitstellt:

* Echtzeit-Dashboard: Grafische Visualisierung aller aktuellen (bspw. alle 30sec veröffentlichten) Sensorwerte.
* Historische Datenanalyse: Speicherung und Darstellung von Messdaten über Zeit, um Trends und Muster zu erkennen.
* Konfigurierbare Schwellenwerte / Festlegen eines Toleranzbereichs: Ermöglicht dem Akteur (Lagerverantwortlicher), für jeden Sensor individuelle Min/Max-Grenzwerte zu definieren.
* Automatisiertes Alarmsystem: Versendet bei Grenzwertverletzungen automatisch Benachrichtigungen innerhalb kürzester  Zeit (bspw. Innerhalb der nächsten 90sec) – beispielsweise via E-Mail oder Push-Benachrichtigung. Speichert eine Alarmhistorie der letzten 500 Alarme pro Lagerort.
* Proaktive Gegensteuerung: Bei einem kritischen Ereignis (insbesondere Grenzwertverletzungen) sendet das System eine Nachricht an das zuvor richtige ermittelte Topic. Eine auf dieses Topic abonnierte Entität – ein Aktor wie ein intelligentes Kühlaggregat empfängt diese Nachricht und führt automatisiert eine Aktion aus.
* Das System verwaltet Benutzer (bis zu ~500), die verschiedene Rollen haben können (z. B. Admin, User).
* Weiter erlaubt das System die Verwaltung von Lagerorten (bis zu ~500), die jeweils mit den gegebenen Sensoren verbunden sein können.

*Höchste Priorität

## Use-Case-Szenarien
Die folgenden Szenarien beschreiben beispielhaft die wichtigsten Anwendungsfälle des Systems:

### Primärer Use-Case: Kontinuierliche Überwachung im Normalbetrieb
| Phase           | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vorbedingungen  | Das System ist installiert, kalibriert und aktiv. Die Schwellenwerte für alle Sensoren sind konfiguriert.                                                                                                                                                                                                                                                                                                                                     |
| Ablauf          | 1. Die Sensoren erfassen kontinuierlich bzw. ggf. in definierten Intervallen die Umgebungsdaten.<br>2. Die Daten werden an die zentrale Software-Plattform übertragen.<br>3. Die Plattform validiert die Daten und vergleicht sie in Echtzeit mit den hinterlegten Schwellenwerten.<br>4. Solange alle Messwerte innerhalb der definierten Toleranzbereiche liegen, protokolliert das System die Daten und zeigt den Status "OK" im Dashboard an. |
| Nachbedingungen | Die Qualität der gelagerten Güter bleibt gesichert.                                                                                                                                                                                                                                                                                             |

### Sekundärer Use-Case: Abweichung und Alarmierung
| Phase           | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Trigger         | Ein Sensor meldet einen Messwert, der einen konfigurierten Schwellenwert über- oder unterschreitet \(z\.B\. Temperatur > 18 °C\)\.                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Ablauf          | 1\. Das System identifiziert die Grenzwertverletzung und klassifiziert das Ereignis als kritisch\.<br>2\. Ein Alarm wird ausgelöst und es passieren ggf\. folgende zwei Aktionen:<br>&nbsp;&nbsp;1\. Das System versendet sofort eine Alarm\-Benachrichtigung an alle vordefinierten Akteure \(Lagerverantwortliche\)\. Die Nachricht enthält den betroffenen Sensor, den Messwert und den Zeitpunkt des Ereignisses\.<br>&nbsp;&nbsp;2\. Das System sendet eine MQTT\-Nachricht an das zuvor richtig ermittelte Topic\. Eine auf das Topic abonnierte Entität, z\.B\. ein IoT\-Gerät, führt daraufhin eine Gegenmaßnahme aus\.<br>3\. Das Ereignis wird mit Zeitstempel und allen relevanten Daten in der System\-Logdatei als "Kritischer Vorfall" gespeichert\.<br>4\. Der verantwortliche Akteur empfängt die Nachricht, greift auf das Dashboard zu, analysiert die Situation und leitet Gegenmaßnahmen ein\.<br>5\. Nach Behebung der Ursache kann der Akteur den Alarm im System quittieren\. |
| Nachbedingungen | Der potenzielle Schaden an den Lagergütern wurde durch rechtzeitige Intervention verhindert\. Der Vorfall ist für spätere Analysen dokumentiert\.                                                                                                                                                                                                                                                                                                                                                                                                                                          |

# Qualitätsziele
Es lassen sich folgende Qualitätsziele, gestützt durch Qualitätsszenarien, definieren:

## Erweiterbarkeit:

### Szenario 1: Erweiterung des Platform-Teilsystems „Monitoring“
Dieses Szenario definiert die Fähigkeit, die Funktionalität des bestehenden Monitoring-Moduls (bzw Teilsystems) zu erweitern, ohne das Kernsystem zu verändern. 
Ein typischer Fall ist die Anbindung eines neuen Sensortyps.

| Attribut        | Beschreibung                                                                                                                                                                                                                                                        |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Szenarioname    | Erweiterung Monitoring-Modul                                                                                                                                                                                                                                        |
| Quelle          | Kernentwickler / Externer Entwickler                                                                                                                                                                                                                                |
| Stimulus        | Es besteht die Anforderung, einen neuen, bisher nicht unterstützten Sensortyp in das System zu integrieren.                                                                                                                  |
| Artefakt        | Das Teilsystem „Monitoring“                                                                                                                                                                                                                                         |
| Umgebung        | System befindet sich in der Entwicklung / Wartung                                                                                                                                                                            |
| Reaktion        | Die Software-Architektur des Monitoring-Teilsystems ermöglicht die Anbindung des neuen Sensortyps. Bestehende Funktionen (wie die Verarbeitung der Daten von Temperatur- oder Feuchtigkeitssensoren) bleiben davon unberührt und funktionieren weiterhin korrekt. |
| Reaktionsmaß    | Die Integration des neuen Sensortyps (inklusive Datenverarbeitung, Speicherung und Visualisierung) ist von einem Entwickler innerhalb von sieben Tagen ohne Regressionsfehler in anderen Teilen des Systems umsetzbar.        |

### Szenario 2: Erweiterung der Plattform um neue Teilsysteme
Dieses Szenario beschreibt die Erweiterbarkeit der gesamten Plattform-Architektur.
Das Ziel ist es, komplett neue Funktionalitätsblöcke als eigenständige Teilsysteme hinzuzufügen, wie zum Beispiel ein Modul "Anleitungsbibliothek".
Dabei soll bestehende zentrale Funkktionalität wiederverwendet werden.

| Attribut      | Beschreibung                                                                                                                                                                                                                                                                                                                                                                  |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Szenarioname  | Erweiterung Plattform                                                                                                                                                                                                                                                                                                                                                         |
| Quelle        | Kernentwickler / Externer Entwickler                                                                                                                                                                                                                                                                                                                                         |
| Stimulus      | Die Plattform soll um ein neues Teilsystem "Anleitungsbibliothek" erweitert werden, das es Nutzern ermöglicht, Handlungsanweisungen zu hinterlegen und abzurufen.                                                                                                                               |
| Artefakt      | Die gesamte Software-Plattform, insbesondere ihre Kernarchitektur und die definierten Schnittstellen.                                                                                                                                                                                                                                 |
| Umgebung      | System befindet sich in der Weiterentwicklung                                                                                                                                                                                                                                                                                                                                |
| Reaktion      | Die Plattform-Architektur stellt klar definierte Erweiterungspunkte beziehungsweise eine offene API bereit.<br>Das neue Teilsystem kann als eigenständiges Modul oder Service entwickelt und in die Plattform integriert werden, ohne den Code der bestehenden Teilsysteme (z.B. "Monitoring") zu modifizieren.<br>Bestehende Plattformlogik (z.B. Benutzerverwaltung) wird wiederverwendet bzw. integriert. |
| Reaktionsmaß  | Das neue Teilsystem kann ohne Ausfallzeit des Gesamtsystems ("Zero Downtime Deployment") in Betrieb genommen werden.<br>Der Entwicklungsaufwand für die reine Integration (Anbindung an die zentrale Navigation, Benutzerverwaltung, etc.) beträgt weniger als eine Woche.                                                            |


## Performance:

### Szenario: Alarmierungszeit ≤ 90 Sekunden ab Grenzwertüberschreitung
Ein rasches Überschreiten oder Unterschreiten definierter Schwellenwerte der
Umgebungsparameter – wie Temperatur, oder Luftfeuchtigkeit – kann potenziell erhebliche
Schäden verursachen. Ziel des Alarmierungssystems ist es daher, eine zuständige Entität
(z.B. eine Nutzerperson oder ein autonom agierendes IoT-System) innerhalb kürzester
Zeit (90 Sekunden nach Detektion) zu informieren, um präventive oder mitigierende
Maßnahmen einzuleiten.

Die Benachrichtigung erfolgt dabei dual:

* **Push-Benachrichtigung** an Endgeräte zur unmittelbaren menschlichen Wahrnehmung
* **MQTT-Nachricht** an ein vordefiniertes Topic zur automatisierten Weiterverarbeitung durch angeschlossene Systeme

| Attribut        | Beschreibung                                                                                                                                                                        |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Szenarioname    | Schnelles Alarmierungssystem                                                                                                                                                        |
| Quelle          | Sensorik / Arduino / Software-Plattform (z\.B\. App)                                                                                                                                |
| Stimulus        | Gemessener Messwert verletzt den festgelegten Toleranzbereich für länger als 30s\.                                                                                                  |
| Artefakt        | Arduino mit Sensorik, die Software inklusive UI, Benachrichtigungssystem \(z\.B\. Email-Client\) und MQTT\-Publisher\.                                                              |
| Umgebung        | Das System befindet sich im produktiven Normalbetrieb\.                                                                                                                             |
| Reaktion        | Durch kontinuierliche Datenübertragung kann schnell ein abnormaler Zustand detektiert werden\. Daraufhin werden betreffende Entitäten alarmiert – Nutzer und ggf\. weitere Systeme\. |
| Reaktionsmaß    | Nach Detektion wird innerhalb von 90 Sekunden sowohl eine Push\-Benachrichtigung, als auch eine MQTT\-Nachricht versendet\.                                                         |

## Sicherheit:

### Szenario: Sichere Authentifizierung und Autorisierung
Dieses Szenario stellt sicher, dass nur berechtigte Personen auf die Plattform zugreifen können und dort nur die Aktionen ausführen dürfen, die ihrer Rolle entsprechen.

| Attribut        | Beschreibung                                                                                                                                                                                                                                   |
|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Szenarioname    | Authentifizierungs-, Autorisierungs- Service                                                                                                                                                                                                  |
| Quelle          | Ein registrierter Nutzer (z\.B\. ein Lagerverantwortlicher oder Systemadministrator)\.                                                                                                                  |
| Stimulus        | Der Nutzer versucht, sich über die Login\-Maske der Plattform am System anzumelden, um auf das Dashboard zuzugreifen oder Konfigurationen vorzunehmen\.                                                 |
| Artefakt        | Authentifizierungs\-, Autorisierungs\-Service der Software\-Plattform\.                                                                                                                                 |
| Umgebung        | Das System befindet sich im produktiven Normalbetrieb\.                                                                                                                                                 |
| Reaktion        | Das System validiert die eingegebenen Anmeldedaten \(z\.B\. Benutzername und Passwort\) gegen die hinterlegte Datenbank\. Bei erfolgreicher Authentifizierung gewährt das System dem Nutzer Zugriff entsprechend seiner vordefinierten Rolle \(z\.B\. Lesezugriff für einen Auditor, Vollzugriff für einen Administrator\)\. Bei fehlerhafter Eingabe wird der Zugriff verweigert und der fehlgeschlagene Versuch sicher protokolliert\. |
| Reaktionsmaß    | Die Anmeldung eines autorisierten Nutzers erfolgt in weniger als 2 Sekunden\.                                                                                                                          |

## Verfügbarkeit:

### Szenario 1: Fehlertoleranz und automatische Wiederherstellung
Kritische Lagerbedingungen erfordern ein System, das möglichst durchgängig verfügbar ist, um eine lückenlose Echtzeitüberwachung sicherzustellen.
Falls das System über einen längeren Zeitraum nicht verfügbar ist, ist der Zustand des Lagerguts unbekannt, und es könnten unbemerkte Schäden entstehen, wenn beispielsweise eine Temperaturschwelle überschritten wird.

| Attribut      | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Szenarioname  | System-Resilienz                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Quelle        | Ein interner Fehlerzustand                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Stimulus      | Ein unerwarteter Ausfall einer kritischen Komponente, z.B. der Absturz der Server-Anwendung, ein "Einfrieren" des Mikrocontrollers oder ein temporärer Verlust der Netzwerkverbindung.                                                                                                                                                                                                                                                                     |
| Artefakt      | Die gesamte Systeminfrastruktur: Sensor-Einheit (Hardware), Software-Plattform (Backend) und die Kommunikationskanäle.                                                                                                                                                                                                                                                                                                                                                                            |
| Umgebung      | Das System befindet sich im produktiven Normalbetrieb.                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Reaktion      | Das System leitet automatisch Maßnahmen zur Wiederherstellung der vollen Funktionsfähigkeit ein. Diese Maßnahmen umfassen insbesondere:<br>- Automatisierte Neustarts: Software-Dienste werden durch Prozess-Manager (z.B. systemd) und Mikrocontroller durch Hardware-Watchdog-Timer bei einem Absturz sofort neu gestartet.<br>- Robuste Wiederverbindungslogik: Das System versucht bei einem Verbindungsabbruch (z.B. zum WLAN oder MQTT-Broker) proaktiv und in regelmäßigen Intervallen, die Verbindung wiederherzustellen.<br>- Zustandsüberwachung (Health Check): Intern lässt sich der Zustand der Anwendung überprüfen. |
| Reaktionsmaß  | Kritische Systemkomponenten stellen ihre Funktionsfähigkeit nach einem behebbaren Ausfall automatisch und ohne manuellen Eingriff wieder her.<br>Ein Administrator wird über den Vorfall und die erfolgreiche Wiederherstellung informiert.                                                                                                                                                                                                                                                        |


### Szenario 2: 99% Systemverfügbarkeit
Das System ist im produktiven Einsatz. Das folgende Szenario zeigt die im Snzenario 1 beschriebene Maßnahme zur automatischen Wiederherstellung und Fehlertoleranz

| Attribut      | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Szenarioname  | Systemverfügbarkeit                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Quelle        | Ein interner Fehlerzustand                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Stimulus      | Das System stürzt während des laufenden Betriebs ab, während Umweltdaten erfasst werden.                                                                                                                                                                                                                                                                     |
| Artefakt      | Die Serveranwendungen, die MQTT-Nachrichten verarbeitet und Daten speichert.                                                                                                                                                                                                                                                                                                                                                                            |
| Umgebung      | Das System befindet sich im produktiven Normalbetrieb.                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Reaktion      | Der Absturz wird erkannt. Innerhalb weniger sekunden erfolgen bis zu drei automatischen Neustartversuchen. Gelingt ein Neustart, werden MQTT-Client und Datenbankverbindung reinitialisiert. Die ANzeige im Dashboard wird nach kurzer Unterbrechung automatisch aktualisiert. Bei Erfolg wird der Vorfall protokolliert und optional gemeldet.  |
| Reaktionsmaß  | Die Anwendung ist innerhalb von 30 Sekunden wieder voll funktionsfähig, ein manuelles Eingreifen ist nicht erforderlich. Die durchgängige Verfügbarkeit bleibt erhalten - die Ausfallzeit liegt unterhalb der zulässigen 1% in einem Zeitraum von 72 Stunden.                                                                                                                                                                                                                                                        |

# Stakeholder
| Stakeholder           | Beschreibung                                                                                                                                                                                                                      |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Lagerverantwortlicher | Definiert die Soll-Werte für die Umgebungsbedingungen, überwacht den Systemstatus und ist der primäre Empfänger von Alarmmeldungen. Nutzt die historischen Daten für Prozessoptimierung und Qualitätsaudits.                      |
| Systemadministrator   | Verantwortlich für Installation, Konfiguration und Wartung des Systems (z\.B\. Hinzufügen neuer Platformnutzerprofile)\.                                                                                                           |
