
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

**Sensorik (Hardware)**: Ein Netzwerk von IoT erfasst die physikalischen Messgrößen.
* Temperatursensor (2x)*: Messung der Raumtemperatur (Innen- und Außen- Raum) in Celsius.
* Luftfeuchtigkeitssensor*: Erfassung der relativen Luftfeuchtigkeit (in %).
* Luftqualitätssensor: Detektion von Verunreinigungen in der Luft.
* Ultraschallsensor: Zur Überprüfung des Zustandes der Tür – ist die Tür offen oder geschlossen.

**Software-Plattform (Kernsystem)**: Eine zentrale Anwendung, die folgende Funktionalitäten bereitstellt:
* Echtzeit-Dashboard: Grafische Visualisierung aller aktuellen (bspw. alle 30sec veröffentlichten) Sensorwerte.
* Historische Datenanalyse: Speicherung und Darstellung von Messdaten über Zeit, um Trends und Muster zu erkennen.
* Konfigurierbare Schwellenwerte: Ermöglicht dem Akteur (Lagerverantwortlicher), für jeden Sensor individuelle Min/Max-Grenzwerte zu definieren.
* Automatisiertes Alarmsystem: Versendet bei Grenzwertverletzungen automatisch Benachrichtigungen innerhalb kürzester  Zeit (bspw. Innerhalb der nächsten 90sec) – beispielsweise via E-Mail oder Push-Benachrichtigung.
* Proaktive Gegensteuerung: Bei einem kritischen Ereignis (insbesondere Grenzwertverletzungen) sendet das System eine Nachricht an das zuvor richtige ermittelte Topic. Eine auf dieses Topic abonnierte Entität – ein Aktor wie ein intelligentes Kühlaggregat empfängt diese Nachricht und führt automatisiert eine Aktion aus.

*Höchste Priorität

## Use-Case-Szenarien
Die folgenden Szenarien beschreiben beispielhaft die wichtigsten Anwendungsfälle des Systems:

### Primärer Use-Case: Kontinuierliche Überwachung im Normalbetrieb
| Phase           | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vorbedingungen  | Das System ist installiert, kalibriert und aktiv. Die Schwellenwerte für alle Sensoren sind konfiguriert.                                                                                                                                                                                                                                                                                                                                         |
| Ablauf          | 1. Die Sensoren erfassen kontinuierlich bzw. ggf. in definierten Intervallen die Umgebungsdaten.<br>2. Die Daten werden an die zentrale Software-Plattform übertragen.<br>3. Die Plattform validiert die Daten und vergleicht sie in Echtzeit mit den hinterlegten Schwellenwerten.<br>4. Solange alle Messwerte innerhalb der definierten Toleranzbereiche liegen, protokolliert das System die Daten und zeigt den Status "OK" im Dashboard an. |
| Nachbedingungen | Ein lückenloser, digitaler Nachweis \(Audit-Trail\) der optimalen Lagerbedingungen wird erstellt. Die Qualität der gelagerten Güter bleibt gesichert.                                                                                                                                                                                                                                                                                             |

### Sekundärer Use-Case: Abweichung und Alarmierung
| Phase           | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Trigger         | Ein Sensor meldet einen Messwert, der einen konfigurierten Schwellenwert über- oder unterschreitet \(z\.B\. Temperatur > 18 °C\)\.                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Ablauf          | 1\. Das System identifiziert die Grenzwertverletzung und klassifiziert das Ereignis als kritisch\.<br>2\. Ein Alarm wird ausgelöst und es passieren ggf\. folgende zwei Aktionen:<br>&nbsp;&nbsp;1\. Das System versendet sofort eine Alarm\-Benachrichtigung an alle vordefinierten Akteure \(Lagerverantwortliche\)\. Die Nachricht enthält den betroffenen Sensor, den Messwert und den Zeitpunkt des Ereignisses\.<br>&nbsp;&nbsp;2\. Das System sendet eine MQTT\-Nachricht an das zuvor richtig ermittelte Topic\. Eine auf das Topic abonnierte Entität, z\.B\. ein IoT\-Gerät, führt daraufhin eine Gegenmaßnahme aus\.<br>3\. Das Ereignis wird mit Zeitstempel und allen relevanten Daten in der System\-Logdatei als "Kritischer Vorfall" gespeichert\.<br>4\. Der verantwortliche Akteur empfängt die Nachricht, greift auf das Dashboard zu, analysiert die Situation und leitet Gegenmaßnahmen ein\.<br>5\. Nach Behebung der Ursache kann der Akteur den Alarm im System quittieren\. |
| Nachbedingungen | Der potenzielle Schaden an den Lagergütern wurde durch rechtzeitige Intervention verhindert\. Der Vorfall ist für spätere Analysen dokumentiert\.                                                                                                                                                                                                                                                                                                                                                                                                                                          |

# Qualitätsziele
Es lassen sich folgende Qualitätsziele, gestützt durch Qualitätsszenarien, definieren:

## Erweiterbarkeit

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

# Stakeholder
| Stakeholder           | Beschreibung                                                                                                                                                                                                                      |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Lagerverantwortlicher | Definiert die Soll-Werte für die Umgebungsbedingungen, überwacht den Systemstatus und ist der primäre Empfänger von Alarmmeldungen. Nutzt die historischen Daten für Prozessoptimierung und Qualitätsaudits.                      |
| Systemadministrator   | Verantwortlich für Installation, Konfiguration und Wartung des Systems (z\.B\. Hinzufügen neuer Platformnutzerprofile)\.                                                                                                           |
