# Datendomäne

## Datenmodellierung (Konzeptuell)
Vor der Auswahl einer spezifischen Datenbanktechnologie wird das fachliche Datenmodell definiert, das alle für das Überwachungssystem relevanten Informationen und deren Beziehungen
zueinander abbildet. <br> Das Modell basiert auf **sechs Entitäten**:

* **Storage**: Repräsentiert einen physischen Ort (z.B. "Weinkeller A", "Lagerhalle B"), der überwacht wird. Jeder Lagerort besitzt eindeutige Attribute wie eine ID und einen Namen.
Ein Lagerort beinhaltet folgende Attribute:
  * **id**: Eindeutige ID des Lagerorts
  * **name**: Name des Lagerorts (z.B. "Weinkeller A")
  * **description**: Optionale Beschreibung des Lagerorts
  * **sensor**: Sensor-IDs, die diesem Lagerort zugeordnet sind <br>
<br>
* **User**: Stellt eine Person dar, die mit dem System interagiert.
Ein Benutzer beinhaltet folgende Attribute:
  * **id**: Eindeutige ID des Benutzers
  * **username**: Eindeutiger Benutzername
  * **password**: Gehasht gespeichertes Passwort
  * **role_id**: Refrenz auf die Rolle des Benutzers
  * **description**: Optionale Besdhreibung des Benutzers
  * **storage_id**: Lagerort-IDs, auf die der Benutzer Zugriff hat <br>
<br>
* **Role**: Definiert die Rolle eines Benutzers im System, um Zugriffsrechte zu steuern.
Eine Rolle beinhaltet folgende Attribute:
  * **id**: Eindeutige ID der Rolle
  * **name**: Name der Rolle (z.B. "Admin", "User")
  * **description**: Optionale Beschreibung der Rolle <br>
<br>
* **Measurement**: Repräsentiert eine einzelne, zu einem exakten Zeitpunkt erfasste Messung (z.B. Temperatur, Luftfeuchtigkeit).
Ein Messwert beinhaltet folgende Attribute:
  * **timestamp**: Zeitpunkt der Messung
  * **value**: Der gemessene Wert
  * **unit**: Einheit des Messwertes (z.B. Temperatur in °C, Luftfeuchtigkeit in %)
  * **sensor_type**: Referenz auf den Sensor, der die Messung durchgeführt hat (z.B. "temperatur_sensor", "humidity_sensor")
  * **storage_id**: Referenz auf den Lagerort, zu dem der Messwert gehört <br>
<br>
* **Sensor**: Stellt einen physischen Sensor dar, der Messwerte erfasst.
Ein Sensor beinhaltet folgende Attribute:
  * **id**: Eindeutige ID des Sensors
  * **type**: Typ des Sensors (z.B. "temperatur_sensor", "humidity_sensor")
  * **location_id**: Referenz auf den Lagerort, an dem der Sensor installiert ist
  * **description**: Optionale Beschreibung des Sensors <br>
<br>
* **Alert**: Repräsentiert eine Benachrichtigung, die ausgelöst wird, wenn ein Messwert außerhalb eines definierten Schwellenwerts liegt.
Ein Alarm beinhaltet folgende Attribute:
  * **id**: Eindeutige ID des Alarms
  * **timestamp**: Zeitpunkt, zu dem der Alarm ausgelöst wurde
  * **message**: Beschreibung des Alarms (z.B. "Temperatur zu hoch")
  * **severity**: Schweregrad des Alarms (z.B. "hoch", "mittel", "niedrig")
  * **sensor_id**: Referenz auf den Sensor, der den Alarm ausgelöst hat
  * **storage_id**: Referenz auf den Lagerort, zu dem der Alarm gehört <br>

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

#### Weitre Entitäten:
Die weiteren Entitäten (Storage, User, Role, Sensor, Alert) haben eine deutlich geringere Anzahl an Instanzen und sind daher zu vernachlässigen.

### Datengröße

Die Messwerte sind in der Regel numerisch (z.B. Temperatur, Luftfeuchtigkeit) und benötigen daher wenig Speicherplatz. <br>


## Kriterien für die Datenbankauswahl
Die Auswahl der Datenbanktechnologie erfolgt anhand folgender Kriterien:

* Unterstützung des Datenmodells: Die Datenbank muss in der Lage sein, die definierten Entitäten und deren Beziehungen ([vgl. Datenmodellierung](data_eva.md#datenmodellierung)) effizient abzubilden.
* Entwicklungsaufwand / Komplexität: Die Implementierung des Datenmodells sollte sich insbesondere den fachlichen [Rahmenbedingungen](mvp.md#rahmenbedingungen) des Projekts anpassen. <br> Aufgrund der Projektlaufzeit von 2.5 Monaten und der Teamgröße von 4 Personen gilt es somit unnötige Komplexität zu vermeiden.
* Performance: Aufgrund der erwarteteten A
