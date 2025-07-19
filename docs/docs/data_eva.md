# Datendomäne

## Datenmodellierung (Konzeptuell)
Vor der Auswahl einer spezifischen Datenbanktechnologie wird das fachliche Datenmodell definiert, das alle für das System STORASENSE relevanten Informationen und deren Beziehungen
zueinander abbildet. Dieser ergeben sich aus den festgelegten [Anforderungen](mvp.md). <br> Insgesamt basiert das Modell auf **sechs Entitäten**:

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
* **Alert**: Repräsentiert einen Alarm, der ausgelöst wird, wenn ein Messwert außerhalb eines definierten Schwellenwerts liegt.
Ein Alarm beinhaltet folgende Attribute:
  * **id**: Eindeutige ID des Alarms
  * **timestamp**: Zeitpunkt, zu dem der Alarm ausgelöst wurde
  * **message**: Beschreibung des Alarms (z.B. "Temperatur zu hoch")
  * **severity**: Schweregrad des Alarms (z.B. "hoch", "mittel", "niedrig")
  * **sensor_id**: Referenz auf den Sensor, der den Alarm ausgelöst hat
  * **storage_id**: Referenz auf den Lagerort, zu dem der Alarm gehört <br>

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

## Nicht funktionale Anforderungen <=> Datendomaine

## Kriterien für die Datenbankauswahl
Die Auswahl der Datenbanktechnologie erfolgt nun anhand folgender Kriterien:

* Unterstützung des Datenmodells: Die Datenbank muss in der Lage sein, die definierten Entitäten und deren Beziehungen ([vgl. Datenmodellierung](data_eva.md#datenmodellierung)) effizient abzubilden.
* Entwicklungsaufwand, Komplexität: Die Implementierung des Datenmodells sollte sich insbesondere den fachlichen [Rahmenbedingungen](mvp.md#rahmenbedingungen) des Projekts anpassen. <br> Aufgrund der Projektlaufzeit von 2.5 Monaten und der Teamgröße von 4 Personen gilt es somit unnötige Komplexität zu vermeiden.
* Performance:

## SQL vs NoSQL

## SQL: Datenbanken
