# Datendomäne

## Datenmodellierung (Konzeptuell)
Vor der Auswahl einer spezifischen Datenbanktechnologie wird das fachliche Datenmodell definiert, das alle für das Überwachungssystem relevanten Informationen und deren Beziehungen
zueinander abbildet.
Das Modell basiert auf vier zentralen Entitäten:

* Lagerort: Repräsentiert einen physischen Ort (z.B. "Weinkeller A", "Lagerhalle B"), der überwacht wird. Jeder Lagerort besitzt eindeutige Attribute wie eine ID und einen Namen.
Ein Lagerort beinhaltet folgende Attribute:
  * **id**: Eindeutige ID des Lagerorts
  * **name**: Name des Lagerorts (z.B. "Weinkeller A")
  * **description**: Optionale Beschreibung des Lagerorts
  * **sensors**: Sensor-IDs, die diesem Lagerort zugeordnet sind <br>
<br>
* Benutzer: Stellt eine Person dar, die mit dem System interagiert.
Ein Benutzer beinhaltet folgende Attribute:
  * **id**: Eindeutige ID des Benutzers
  * **username**: Eindeutiger Benutzername
  * **password**: Passwort - gehasht gespeichert
  * **role**: Rolle des Benutzers (z.B. "Admin", "User")
  * **description**: Optionale Besdhreibung des Benutzers                          |
  * **storage_id**: Lagerort-IDs, auf die der Benutzer Zugriff hat <br>
<br>
* Messwert: Repräsentiert eine einzelne, zu einem exakten Zeitpunkt erfasste Messung (z.B. Temperatur, Luftfeuchtigkeit).
Ein Messwert beinhaltet folgende Attribute:
  * **timestamp**: Zeitpunkt der Messung
  * **value**: Der gemessene Wert
  * **unit**: Einheit des Messwertes (z.B. Temperatur in °C, Luftfeuchtigkeit in %)
  * **sensor_type**: Referenz auf den Sensor, der die Messung durchgeführt hat (z.B. "temperatur_sensor", "humidity_sensor")
  * **storage_id**: Referenz auf den Lagerort, zu dem der Messwert gehört

* Sensor: Stellt einen physischen Sensor dar, der Messwerte erfasst.
Ein Sensor beinhaltet folgende Attribute:
  * **id**: Eindeutige ID des Sensors
  * **type**: Typ des Sensors (z.B. "temperatur_sensor", "humidity_sensor")
  * **location_id**: Referenz auf den Lagerort, an dem der Sensor installiert ist
  * **description**: Optionale Beschreibung des Sensors

### ER-Diagramm

### Datenvolumen
Das erwartete Datenvolumen ist moderat, da das System in erster Linie Echtzeitdaten von Sensoren erfasst und speichert.

#### Datenmenge
Wie eingangs im [Projektüberblick](mvp.md#funktionale-anforderungen) beschrieben, besteht die Sensorik des Systems aus vier Sensoren die täglich für 2.5 Monate alle 30 Sekunden Messwerte erfassen.
Folgende Rechnung verdeutlicht die erwartete Datenmenge:
* Anzahl der Sensoren: 4
* Jeder Sensor sendet alle 30 Sekunden einen Messwert.
* Das ergibt:
  * Messungen pro Stunde pro Sensor: (60/30) x 60 = 120
  * Messungen pro Tag pro Sensor: 120 x 24 = 2.880
  * Messungen pro Tag gesamt (4 Sensoren): 2.880 x 4 = 11.520
  * Messungen für 2,5 Monate (ca. 75 Tage): 11.520 x 75 = **864.000 Messpunkte**

Die Gesamtzahl der Lagerorte und Benutzer ist begrenzt, was die Datenbankgröße überschaubar hält.

#### Datenstruktur


## Kriterien für die Datenbankauswahl
Die Auswahl der Datenbanktechnologie erfolgt anhand folgender Kriterien:

* Unterstützung des Datenmodells: Die Datenbank muss in der Lage sein, die definierten Entitäten und deren Beziehungen ([vgl. Datenmodellierung](data_eva.md#datenmodellierung)) effizient abzubilden.
* Entwicklungsaufwand / Komplexität: Die Implementierung des Datenmodells sollte sich insbesondere den fachlichen [Rahmenbedingungen](mvp.md#rahmenbedingungen) des Projekts anpassen. <br> Aufgrund der Projektlaufzeit von 2.5 Monaten und der Teamgröße von 4 Personen gilt es somit unnötige Komplexität zu vermeiden.
* Performance: Aufgrund der erwarteteten A
