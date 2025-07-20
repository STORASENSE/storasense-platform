# Datendomäne

## Datenmodellierung (Konzeptuell)
Vor der Auswahl einer spezifischen Datenbanktechnologie wird das fachliche Datenmodell definiert, das alle für das System STORASENSE relevanten Informationen und deren Beziehungen
zueinander abbildet. Diese ergeben sich aus den definierten [Anforderungen](mvp.md). <br> Insgesamt basiert das Modell auf **sechs Entitäten**:

* **Storage**: Repräsentiert einen physischen Ort (z.B. "Weinkeller A", "Lagerhalle B"), der überwacht wird. Jeder Lagerort besitzt eindeutige Attribute wie eine ID und einen Namen.
Ein Lagerort beinhaltet folgende Attribute:
  * `id`: Eindeutige ID des Lagerorts
  * `name`: Name des Lagerorts (z\.B\. "Weinkeller A")
  * `description`: Optionale Beschreibung des Lagerorts
  * `sensor`: Sensor\-IDs, die diesem Lagerort zugeordnet sind <br>
  <br>
* **User**: Stellt eine Person dar, die mit dem System interagiert.
Ein Benutzer beinhaltet folgende Attribute:
  * `id`: Eindeutige ID des Benutzers
  * `username`: Eindeutiger Benutzername
  * `password`: Gehasht gespeichertes Passwort
  * `role_id`: Referenz auf die Rolle des Benutzers
  * `description`: Optionale Beschreibung des Benutzers
  * `storage_id`: Lagerort-IDs, auf die der Benutzer Zugriff hat <br>
  <br>
* **Role**: Definiert die Rolle eines Benutzers im System, um Zugriffsrechte zu steuern.
Eine Rolle beinhaltet folgende Attribute:
  * `id`: Eindeutige ID der Rolle
  * `name`: Name der Rolle (z\.B\. "Admin", "User")
  * `description`: Optionale Beschreibung der Rolle <br>
  <br>
* **Measurement**: Repräsentiert eine einzelne, zu einem exakten Zeitpunkt erfasste Messung (z.B. Temperatur, Luftfeuchtigkeit).
Ein Messwert beinhaltet folgende Attribute:
  * `timestamp`: Zeitpunkt der Messung
  * `value`: Der gemessene Wert
  * `unit`: Einheit des Messwertes (z\.B\. Temperatur in °C, Luftfeuchtigkeit in %)
  * `sensor_type`: Referenz auf den Sensor, der die Messung durchgeführt hat
  * `storage_id`: Referenz auf den Lagerort, zu dem der Messwert gehört <br>
  <br>
* **Sensor**: Stellt einen physischen Sensor dar, der Messwerte erfasst.
Ein Sensor beinhaltet folgende Attribute:
  * `id`: Eindeutige ID des Sensors
  * `type`: Typ des Sensors (z\.B\. "temperatur_sensor", "humidity_sensor")
  * `location_id`: Referenz auf den Lagerort, an dem der Sensor installiert ist
  * `description`: Optionale Beschreibung des Sensors <br>
  <br>
* **Alert**: Repräsentiert einen Alarm, der ausgelöst wird, wenn ein Messwert außerhalb eines definierten Schwellenwerts liegt.
Ein Alarm beinhaltet folgende Attribute:
  * `id`: Eindeutige ID des Alarms
  * `timestamp`: Zeitpunkt, zu dem der Alarm ausgelöst wurde
  * `message`: Beschreibung des Alarms (z\.B\. "Temperatur zu hoch")
  * `severity`: Schweregrad des Alarms (z\.B\. "hoch", "mittel", "niedrig")
  * `sensor_id`: Referenz auf den Sensor, der den Alarm ausgelöst hat
  * `storage_id`: Referenz auf den Lagerort, zu dem der Alarm gehört <br>

### ER-Diagramm

## Datenvolumen
Das erwartete Datenvolumen ist moderat, da das System in erster Linie Echtzeitdaten von Sensoren erfasst und speichert.

### Datenmenge
#### Measurement:
Wie eingangs im [Projektüberblick](mvp.md#funktionale-anforderungen) beschrieben, besteht die Sensorik des Systems aus vier Sensoren die täglich für 2.5 Monate alle 30 Sekunden Messwerte erfassen.
Folgende Rechnung verdeutlicht die erwartete Datenmenge:
* Anzahl der Sensoren: 4
* Jeder Sensor sendet alle 30 Sekunden einen Messwert.
* Das ergibt:
  * Messungen pro Stunde pro Sensor: (60/30) x 60 = 120
  * Messungen pro Tag pro Sensor: 120 x 24 = 2.880
  * Messungen pro Tag gesamt (4 Sensoren): 2.880 x 4 = 11.520
  * Messungen für 2,5 Monate (ca. 75 Tage): 11.520 x 75 = **864.000 Messpunkte**

Insgesamt werden also ca. **864.000 Messpunkte** erwartet, die in der Datenbank gespeichert werden müssen.

#### Weitere Entitäten:
Die weiteren Entitäten haben eine deutlich geringere Anzahl an Instanzen:
* Wie bereits im [Projektüberblick](mvp.md#funktionale-anforderungen) beschrieben unterstützt das System bis zu 500 Benutzer und 50 Lagerorte.
* Weiter sind 2 Rollen vorgesehen, die den Benutzern zugeordnet werden können.
* Die letzten 500 Alarme eines Lagerorts werden ebenfalls gespeichert. So ergibt sich eine maximale Anzahl von maximal 25.000 Alarm-Einträgen (500 Alarme x 50 Lagerorte).

Insgesamt sind die weiteren Entitäten also zu vernachlässigen, da sie nur eine geringe Anzahl an Instanzen haben. <br>
**Außerdem gilt es zu beachten, dass der Großteil der Daten der weiteren Entitäten sich in der Regel nicht ständig ändern, sondern einmal angelegt werden und ggf. selten aktualisiert werden.**


### Datengröße
#### Measurement:
Die Messwerte sind in der Regel numerisch (z.B. Temperatur, Luftfeuchtigkeit) und benötigen daher wenig Speicherplatz. <br>

| Datenfeld     | Typ         | Größe (Bytes) | Beschreibung                        |
|--------------|-------------|----------|-------------------------------------|
| timestamp           | Datetime     | 8        | Timestamp           |
| value         | Float      | 4        | Numerisch                  |
| unit  | String      | 2        |  Einheit als Kurzstring (z.B. "C")              |
| sensor_type    | String    | 2-4      | Sensortyp            |
| storage_id        | Integer       | 2        | Lagerortreferenz                   |
| Gesamt         | -      | **~18**  | Durchschnittlich pro Messung               |

**Gesamtvolumen:**
864.000 Messungen × ~ 18 Byte = **~15,5 MB**

#### Weitere Entitäten:
Der Speicherbedarf der weiteren Entitäten ist ebenfalls gering, da sie nur wenige Attribute haben und in der Regel nicht sehr viele Instanzen existieren. <br>

* Anschaulich lässt sich dies am Beispiel der User-Entität darstellen, die folgende Attribute hat:

| Datenfeld    | Typ      | Größe (Bytes) |
|--------------|----------|---------------|
| id           | Integer  | 4             |
| username     | String   | 20           |
| password (hash)    | String   | 64            |
| role_id      | Integer  | 2             |
| description  | String   | 50          |
| storage_id   | Integer[]  | 8           |
| Gesamt       | -        | **~150**      |

**Gesamtvolumen für 500 User:**
500 User × ~ 150 Byte = **~75 KB**

## Nichtfunktionale Anforderungen <=> Datendomäne

### **Einfluss der nicht-funktionalen Anforderungen auf die Datendomäne**

Die definierten nicht-funktionalen Anforderungen übersetzen die allgemeinen Systemziele in konkrete Erwartungen an die Datenspeicherung und -verarbeitung. Somit sind sind ein entscheidender Faktor für die Auswahl der richtigen Datenbanktechnologie.

#### **Performance und schnelle Alarmierung**

Die Anforderung, einen Alarm innerhalb von 90 Sekunden auszulösen, *nachdem* ein Grenzwert für über 30 Sekunden verletzt wurde, stellt eine hohe Anforderung an die Datenbank-Performance. Dies erfordert mehr als nur eine schnelle Einzelabfrage. Die Datenbank muss folgende Operationen sehr effizient unterstützen:
1.  **Schnelles Schreiben (Ingestion):** Jeder neue `Measurement`-Datensatz muss mit minimaler Latenz gespeichert werden, damit die Alarmierungskette sofort starten kann.
2.  **Effiziente Zeitfenster-Abfragen:** Um eine 30-sekündige Grenzwertverletzung zu erkennen, muss das System eine Abfrage wie "Gib mir alle Messwerte von `sensor_x` der letzten 30-40 Sekunden" sehr schnell ausführen können. Dies verlangt Indexierungsfähigkeiten, insbesondere auf den Feldern `timestamp` und `sensor_id`.

#### **Hohe Verfügbarkeit**

Die geforderte Verfügbarkeit von 99% über einen Zeitraum von drei Tagen erlaubt eine maximale Ausfallzeit von ca. 43 Minuten.
*   **Stabilität und Datenpersistenz:** Die Datenbank muss ein robuster, stabiler Dienst sein, der Daten zuverlässig auf die Festplatte schreibt. Bei einem Neustart dürfen so keine Daten verloren gehen (was beispielsweise reine In-Memory-Datenbanken ausschließt). Basierend auf der Anforderung einer Verfügbarkeit von 99% muss die Technologie stabil innerhalb einer Docker-Umgebung laufen.
*   **Unterstützung für Resilienz:** Die Anforderung des automatischen Neustarts wird von der Infrastruktur (Docker Compose) umgesetzt. Die Datenbank muss diesen Prozess jedoch zuverlässig unterstützen, d.h. nach einem unerwarteten Herunterfahren schnell und konsistent wieder hochfahren.

#### **Sicherheit (Authentifizierung & Autorisierung)**

Diese Anforderung betrifft primär die Anwendungslogik, aber die Datenbank muss die sichere Implementierung unterstützen:
*   **Sichere Datenspeicherung:** Die Datenbank muss sensible Daten wie gehashte Passwörter in der `User`-Entität sicher speichern.
*   **Unterstützung relationaler Integrität:** Um die Autorisierung (wer darf auf welchen `Storage` zugreifen?) sicherzustellen, muss die Datenbank die Beziehungen zwischen `User`, `Role` und `Storage` zuverlässig abbilden können. Ein System, das diese Beziehungen durch **Constraints** und **Fremdschlüssel** auf Datenbankebene garantiert, ist hier also wichtig, da es das Risiko von Fehlern in der Anwendungslogik reduziert.

## Kriterien für die Datenbankauswahl
Die Auswahl der Datenbanktechnologie erfolgt nun anhand folgender Kriterien:

* **Unterstützung des Datenmodells**: Die Datenbank muss in der Lage sein, die definierten Entitäten und deren Beziehungen ([vgl. Datenmodellierung](data_eva.md#datenmodellierung)) effizient abzubilden. Beispielsweise gilt es die Grundlage für die Sicherheit des Systems zu schaffen (vgl. [Nichtfunktionale Anforderungen <=> Datendomäne](data_eva.md#nicht-funktionale-anforderungen--datendomäne)). <br>
<br>
* **Komplexität**: Die Implementierung des Datenmodells sollte sich insbesondere den fachlichen [Rahmenbedingungen](mvp.md#rahmenbedingungen) des Projekts anpassen. <br> Aufgrund der Projektlaufzeit von 2.5 Monaten und der Teamgröße von 4 Personen gilt es somit unnötige Komplexität zu vermeiden. <br>
  * *Anmerkung: Das berechnete [Datenvolumen](data_eva.md#datenvolumen) ist mit unter 1 MB pro Woche sehr gering. Daher sind Skalierungsmechanismen (wie z.B. horizontales Sharding) für dieses Projekt nicht relevant. Das Kriterium bewertet stattdessen, wie gut die Datenbanktechnologie mit diesem spezifischen, moderaten Datenvolumen umgeht, ohne unnötigen administrativen oder ressourcentechnischen Overhead zu erzeugen. <br>*


* **Performance**: Die Leistungsfähigkeit der Datenbank ist entscheidend für die Realisierung des schnellen Alarmsystems (vgl. [Nichtfunktionale Anforderungen <=> Datendomäne](data_eva.md#nicht-funktionale-anforderungen--datendomäne)). Hierbei gilt es insbesondere die Messdaten, die den Großteil des [Datenvolumens](data_eva.md#datenvolumen) ausmachen, effizient zu verwalten. <br>
<br>

* **Betriebsstabilität**: Die Datenbank sollte robust im Betrieb sein - entscheidend ist es, einen konsistenten Betrieb mit minimaler Ausfallzeit zu gewährleisten (vgl. [Nichtfunktionale Anforderungen <=> Datendomäne](data_eva.md#nicht-funktionale-anforderungen--datendomäne)). <br>
<br>
* **Datenintegrität und Konsistenz**: Dieses Kriterium bewertet die Fähigkeit der Datenbank, die Korrektheit und Widerspruchsfreiheit der Daten sicherzustellen. Weiter ist die Garantie wichtig, dass Daten nach dem Speichern nicht verloren gehen oder korrumpiert werden (Datenpersistenz). Dies ist insbesondere für die Verwaltung der Nutzer mit ihren Rechten wichtig. <br>
<br>
* **Abfragemöglichkeiten für Visualisierung**: Die Fähigkeit der Abfragesprache, komplexere Aggregationen (z.B. Durchschnittswerte, Gruppierungen) und Verknüpfungen zu formulieren, die für die Erstellung eines Dashboards wichtig sind. Die Kompatibilität mit Standard-Visualisierungstools ist hier ebenfalls relevant.

## SQL vs NoSQL
Die folgende Tabelle evaluiert einen relationalen SQL-Ansatz und einen dokumentenorientierten NoSQL-Ansatz anhand der festgelegten Kriterien:

*Anmerkung: Für den Vergleich wird als NoSQL-Typ die dokumentorientierte Datenbank initial ausgewählt, da jeder Measurement-Datensatz eine in sich geschlossene Informationseinheit darstellt (Zeitstempel, Wert, Sensor-ID etc.), die sich nativ als ein JSON-ähnliches Dokument abbilden lässt. Dieser Ansatz ist als einziger NoSQL-Typ flexibel genug, um sowohl die zeitreihenbasierten Measurement-Daten als auch die eher strukturierten Entitäten wie User und Storage in separaten Collections zu verwalten.*

| Kriterium                           | SQL-Ansatz (Relational)                                                                                                                                                                                                                                                                 | NoSQL-Ansatz (Dokumentenorientiert)                                                                                                                                                                                                                                                                |
|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Unterstützung des Datenmodells       | Sehr gut. Das relationale Modell eignet sich sehr gut, um die klar strukturierten Beziehungen zwischen User, Role und Storage durch Foreign Keys abzubilden. Die Measurement-Daten passen in eine separate, nach Zeitstempel indizierte Tabelle.                                        | Okay. Sehr gut für die flexiblen Measurement-Daten. Die Abbildung der relationalen Benutzer- und Zugriffsdaten ist jedoch umständlich. Beziehungen müssen in der Anwendungslogik (über Referenzen oder eingebettete Dokumente) verwaltet werden, was die Komplexität erhöht.                       |
| Komplexität                         | Gering. Das Datenmodell lässt sich intuitiv auf Tabellen abbilden. Die Datenbank übernimmt die Logik der Beziehungsintegrität. Das moderate Datenvolumen erfordert keinen administrativen Mehraufwand.                                                                                  | Mittel. Während das Speichern der IoT-Daten einfach ist, erfordert die konsistente Abbildung der Benutzer-Zugriffsrechte mehr Entwicklungsaufwand. Der größte Vorteil – die einfache Skalierung bei riesigen Datenmengen – ist hier nicht relevant und führt zu unnötigem konzeptionellen Overhead. |
| Performance                          | Sehr gut. Moderne SQL-Datenbanken können das moderate Datenvolumen mühelos verarbeiten. Schnelle Schreibvorgänge und effiziente Zeitfenster-Abfragen für die Alarmierung sind durch Standard-Indizes auf den Zeitstempel- und Sensor-Feldern ohne Probleme und performant realisierbar. | Sehr gut. Hohe Schreibleistung ist eine Kernstärke der meisten NoSQL Datenbanken. Die Abfragegeschwindigkeit für die Alarmierung wäre ebenfalls sehr gut. Bei diesem Anwendungsfall mit der geringen Datenmenge ist ein Performancevorteil jedoch fraglich.                                        |
| Betriebsstabilität                   | Sehr hoch. Etablierte SQL-Datenbanken wie PostgreSQL sind für ihre Robustheit und stabilen Betrieb bekannt. Sie unterstützen einen zuverlässigen Neustart nach Ausfällen und fügen sich nahtlos in Docker-Umgebungen ein.                                                               | Sehr hoch. Moderne NoSQL-Datenbanken sind ebenfalls für den stabilen Dauerbetrieb ausgelegt und für ihre Resilienz in verteilten Systemen bekannt.                                                            |
| Datenintegrität & Konsistenz         | Sehr hoch (nativ). Durch ACID-Transaktionen und Constraints (UNIQUE, FOREIGN KEY) wird die Konsistenz der Daten auf Datenbankebene erzwungen. Dies ist besonders für die Verwaltung von Benutzerrechten und die Sicherheit des Systems ein entscheidender Vorteil.                      | Mittel. Bietet standardmäßig schwächere Konsistenzmodelle (Eventual Consistency). Obwohl moderne Systeme auch ACID-Transaktionen unterstützen, liegt die Verantwortung für die Datenintegrität bei relationalen Verknüpfungen größtenteils beim Entwickler im Anwendungscode.        |
| Abfragemöglichkeiten für Visualisierung | Sehr gut. Die standardisierte Abfragesprache SQL ist geeignet für komplexe Aggregationen (GROUP BY) und Verknüpfungen (JOIN), die für Dashboards wichtig sind (z.B. Anzeige von Lagerortnamen zu Messwerten).                                                                           | Gut. Proprietäre Abfragesprachen sind mächtig, aber weniger standardisiert. Das Verknüpfen von Daten aus unterschiedlichen Collections ist oft aufwendiger als ein SQL-JOIN.                                            |

Der Vergleich zeigt, dass der SQL-Ansatz für das Projekt die bessere Wahl ist.
Die Stärken des relationalen Modells in Bezug auf Datenintegrität, Konsistenz und die einfache Abbildung der Beziehungen zwischen den Entitäten sind entscheidend.
Insgesamt lässt sich das Datenmodell so leichter (und schneller) umsetzen.
Performance und Betriebsstabilität sind in beiden Fällen hoch, aber der SQL-Ansatz bietet eine klarere Struktur für die Verwaltung der Benutzerrechte und Zugriffe. <br>
Weiter lässt sich die Performance in der SQL-Datenbank durch Indizes auf beispielsweise den Zeitstempel manuell beziehungsweise durch Nutzung einer spezialisierten SQL-Datenbank (Timeseries) verbessern. <br>
Auch die Abfragemöglichkeiten im Zuge der Visualisierung mittels eines Dashboards sind im SQL-Ansatz gegeben, da SQL eine standardisierte und mächtige Abfragesprache bietet, die komplexe Aggregationen und Verknüpfungen unterstützt. <br>

## SQL: Datenbanken
