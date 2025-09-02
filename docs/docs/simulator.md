# STORASENSE – Simulator & Stresstest

## Überblick

Die STORASENSE-Simulationsumgebung ermöglicht das Testen, Entwickeln und Validieren der gesamten Sensorplattform – auch ohne echte Hardware. Sie umfasst:

- **SimulatedSensor**: Simuliert beliebige Sensortypen (z. B. Temperatur, Feuchte, CO₂, Ultraschall) und verhält sich wie ein echter Sensor.
- **StressSimulator**: Erzeugt viele virtuelle Sensoren gleichzeitig, um die Plattform unter hoher Last zu testen.

Beide Lösungen publizieren MQTT-Nachrichten im identischen Format wie die reale Hardware. Dadurch können Backend, Datenbank und UI unabhängig von tatsächlichen Geräten entwickelt und getestet werden.

---

## Build- und Laufzeitmodi

Die Betriebsart wird über Präprozessor-Schalter im Sketch gewählt:

```cpp
#define SIM_MODE     1   // 0 = echte Hardware, 1 = Simulation aktiv
#define STRESS_MODE  0   // 0 = normaler Betrieb (HW oder einfache Simulation), 1 = Stresstest
```

## Übersicht der Modi

### Hardware-Modus

Im Hardware-Modus (SIM_MODE = 0, STRESS_MODE = 0) läuft das Programm direkt auf echter Hardware und verwendet dabei reale, physisch angeschlossene Sensoren. Nur die tatsächlich verbundenen Sensoren werden ausgelesen und deren Messwerte über MQTT publiziert. Dieser Modus ist für den regulären Betrieb vorgesehen sowie für Praxistests mit realen Geräten, um das Verhalten des Gesamtsystems unter realen Bedingungen zu überprüfen.

### Simulations-Modus

Im Simulations-Modus (SIM_MODE = 1, STRESS_MODE = 0) werden die Sensorwerte vollständig durch Software simuliert, sodass keinerlei physische Hardware benötigt wird. Es werden einzelne virtuelle Sensoren erzeugt, die sich in ihrem Verhalten und in der Datenübertragung wie echte Geräte verhalten. Dieser Modus eignet sich insbesondere dazu, die gesamte Datenverarbeitungskette – vom Sensor über das Backend bis hin zur Benutzeroberfläche – zu testen, auch wenn keine Hardware zur Verfügung steht.

### Stresstest-Modus

Im Stresstest-Modus (SIM_MODE = 1, STRESS_MODE = 1) erzeugt die Simulationsumgebung eine große Anzahl virtueller Sensoren – von Dutzenden bis zu Hunderten – die gleichzeitig Daten senden. Die Sende- und Publikationsrate dieser Sensoren lässt sich flexibel konfigurieren. Dadurch kann das System gezielt unter hoher Last betrieben werden, um beispielsweise die Skalierbarkeit, Performance und Stabilität der Plattform zu testen.

---

## MQTT-Themen & Payload

Virtuelle und echte Sensoren publizieren identische MQTT-Nachrichten:

- **Topic:**
  ```
  storasense/sensor/<SENSOR_ID>/state
  ```

- **Payload (JSON):**
  ```json
  {
    "temperature": 21.3,
    "humidity": 48.1,
    "co2": 700,
    "distance": 123.4,
    "timestamp": 1718000000
  }
  ```
  - Felder je nach Sensortyp (z.B. Temperatur, Feuchte, CO₂, Distanz).
  - `timestamp` ist ein Unix-Zeitstempel.

---

## SimulatedSensor

### Konstruktion

Ein SimulatedSensor simuliert einen einzelnen Sensor. Er kann verschiedene Sensortypen abbilden und unterstützt verschiedene Werteverläufe.

**Beispiel:**
```cpp
SimulatedSensor tempSensor(
    SimulatedSensor::Type::TEMPERATURE,
    SimulatedSensor::Preset::SINEWAVE
);
```

### Presets

Für die Simulation der Sensordaten stehen verschiedene Presets zur Verfügung. Diese Presets bestimmen, wie sich die simulierten Werte im Zeitverlauf verhalten. Beispielsweise kann ein Wert konstant bleiben, sich zufällig innerhalb eines definierten Bereichs ändern, einem sinusförmigen Verlauf folgen (wie es etwa bei Temperaturverläufen typisch ist) oder linear ansteigen bzw. abfallen. Die Presets lassen sich miteinander kombinieren oder individuell anpassen, um möglichst realistische oder auch gezielt abweichende Szenarien zu simulieren.

---

## StressSimulator

Der StressSimulator erzeugt viele virtuelle Sensoren und publiziert deren Werte mit einstellbarer Rate.

### Parameter & Konfiguration

Der StressSimulator kann flexibel an verschiedene Testanforderungen angepasst werden. Die Anzahl der zu simulierenden Sensoren lässt sich frei wählen, beispielsweise können 100 oder mehr Sensoren gleichzeitig erzeugt werden. Ebenso ist die Publikationsrate, also das Intervall, in dem die Sensoren ihre Werte veröffentlichen, konfigurierbar (z. B. alle 5 Sekunden). Es können unterschiedliche Sensortypen wie Temperatur, Feuchte oder CO₂ simuliert werden, und auch die Art des Werteverlaufs, etwa zufällig oder sinusförmig, ist einstellbar.

**Konfiguration im Sketch:**
```cpp
#define STRESS_SENSOR_COUNT  100
#define STRESS_PUBLISH_MS    5000
```

### Initialisierung & Nutzung

```cpp
StressSimulator stressSim(
    STRESS_SENSOR_COUNT,
    STRESS_PUBLISH_MS,
    SimulatedSensor::Type::TEMPERATURE,
    SimulatedSensor::Preset::RANDOM
);
stressSim.begin();
```

Im Loop:
```cpp
stressSim.loop();
```

### Typische Nutzung

Typischerweise wird der StressSimulator eingesetzt, um die Skalierbarkeit des Backends zu überprüfen und Lasttests für MQTT-Broker sowie Datenbanken durchzuführen. Darüber hinaus eignet sich das Tool, um gezielt Ausfälle oder starke Fluktuationen im Datenstrom zu simulieren und so die Robustheit und Fehlertoleranz der Gesamtplattform zu testen.

---

## Umschalten im Sketch

Die Betriebsart wird durch Setzen der Präprozessor-Defines gewählt:

```cpp
#define SIM_MODE     1   // Simulation aktivieren
#define STRESS_MODE  1   // Stresstest aktivieren
```

Im Code wird anhand dieser Werte der jeweilige Modus initialisiert:

```cpp
#if SIM_MODE
  #if STRESS_MODE
    StressSimulator stressSim(...);
  #else
    SimulatedSensor simSensor(...);
  #endif
#else
  // Hardware-Sensor initialisieren
#endif
```

---

## Vorteile der Simulation

Die Simulation bietet zahlreiche Vorteile: Sie ermöglicht ein schnelles Testen der gesamten Plattform, ohne dass physische Sensorhardware benötigt wird. Dadurch lassen sich automatisierte Tests und Continuous-Integration-Prozesse einfach realisieren. Zudem kann die Skalierbarkeit des Systems durch gezielte Lasttests überprüft werden. Fehlerfälle wie der Ausfall von Sensoren oder Werte außerhalb des Normalbereichs können gezielt simuliert werden, um die Systemreaktion zu validieren. Insgesamt ermöglicht die Simulation eine parallele und unabhängige Entwicklung, auch wenn (noch) keine Hardware verfügbar ist.

---

## Quickstart

1. **Modus wählen:**
   Im Sketch die gewünschten Defines setzen:
   ```cpp
   #define SIM_MODE     1
   #define STRESS_MODE  0
   ```
2. **Sketch kompilieren und hochladen**
3. **MQTT-Broker konfigurieren**
   (z. B. Mosquitto lokal oder in der Cloud)
4. **Backend & UI starten**
   (Backend empfängt die simulierten Daten wie von echten Sensoren)

---

# Simulation & Stresstest: Ergebnisse & Bewertung

Diese Dokumentation fasst die **durchgeführten Tests**, die **Beobachtungen** im Betrieb sowie die **wichtigsten Erkenntnisse** zusammen. Sie dient als Nachweis dafür, dass sich die Plattform mit realen und simulierten Sensoren identisch verhält und wo die **Skalierungsgrenzen** im aktuellen Setup liegen.

---

## Versuchsaufbau

- **Quelle**: Arduino MKR1010 (WiFiNINA) mit drei Modi
  - Hardware (echte Sensoren)
  - Simulation (4 feste Sim-Sensoren)
  - Stresstest (viele virtuelle Sensoren)
- **Protokoll**: MQTT (QoS 0), identisches Topic-/Payload-Format wie im Realbetrieb
  - Topic: `dhbw/ai/si2023/4/<SENSOR_TYP>/<UUID>`
  - Beispiel-Payload:
    ```json
    {
      "timestamp": 1756578599,
      "value": [21.98],
      "sequence": 620,
      "meta": {
        "startup": 1756578558,
        "unit": "CELSIUS"
      }
    }
    ```
- **Ziel**: MQTT-Client → Backend → Datenbank (Logs beobachtet)

---

## Messergebnisse

Nachfolgend werden die vier zentralen Testfälle beschrieben.
Im Fokus stehen die **End-to-End-Latenz** (Zeit von Publish auf dem Board bis zum Auftauchen im Backend-Log), die Stabilität des Gesamtsystems sowie beobachtete Auffälligkeiten.
Die Tests wurden jeweils mehrere Minuten durchgeführt, um auch mögliche Instabilitäten sichtbar zu machen.

---

### 1) Live-Daten – echte Sensoren, ca. 1 Hz pro Sensor
In diesem Szenario wurden ausschließlich reale Sensoren eingesetzt (Temperatur, Feuchtigkeit, Gas und Ultraschall).
Die Sensoren publizieren etwa einmal pro Sekunde ihre Messwerte. Das Backend verarbeitet diese Daten so, wie es auch im späteren Produktivbetrieb vorgesehen ist.

Die Beobachtung zeigt, dass die Nachrichten nahezu in Echtzeit im Backend ankommen. Es gibt keine spürbaren Verzögerungen zwischen dem Moment der Messung und der Anzeige im Backend-Log. Die gemessene End-to-End-Latenz liegt konstant unter 200 ms.
Über eine Testdauer von mehr als zehn Minuten lief das System stabil. Lediglich vereinzelt traten Backend-Meldungen wie „Bad request“ auf, vermutlich durch Randwerte in den Messungen. Diese hatten aber keinen Einfluss auf den Gesamtdurchsatz oder die Stabilität.

![Live-Daten mit echten Sensoren bei 1 Hz](./docs/docs/images/simulation/live_daten.png)

---

### 2) Simulation – pro Sensortyp 1 Sensor, 1 Hz
Hier wurde die reale Hardware durch einen simulierten Sensor pro Sensortyp ersetzt. Jeder simulierte Sensor verhält sich dabei wie ein echter, publiziert jedoch rein softwaregenerierte Werte.
Die Struktur der MQTT-Nachrichten (Topic und JSON-Payload) ist identisch zur Hardware, sodass das Backend keinen Unterschied erkennt.

Das Verhalten war praktisch deckungsgleich mit den Live-Daten. Auch hier kamen die Nachrichten zuverlässig und ohne nennenswerte Verzögerung an. Die Latenz lag durchgängig unter 200 ms. Über mehrere Minuten hinweg gab es keinerlei Instabilitäten oder Ausfälle. Damit konnte bestätigt werden, dass die Simulation eine zuverlässige Testumgebung für Backend und Datenfluss darstellt.

![Simulation mit 1 Sensor pro Typ bei 1 Hz](./docs/docs/images/simulation/sim_eins_Sensor.png)

---

### 3) Simulation – pro Sensortyp 1 Sensor, 5 Hz (≈ 25 Msgs/s gesamt)
Im nächsten Test wurde die Last erhöht, indem die simulierten Sensoren fünfmal pro Sekunde Nachrichten sendeten. Bei fünf Sensortypen ergibt das etwa 25 Nachrichten pro Sekunde.
Dieser Durchsatz ist deutlich höher als im Normalbetrieb, eignet sich jedoch gut, um die Belastungsgrenze des Systems auszuloten.

Das Backend konnte die Daten kontinuierlich verarbeiten, allerdings zeigte sich eine leichte Erhöhung der Latenz. Während im 1-Hz-Szenario praktisch keine Verzögerung messbar war, lagen die Werte nun in vielen Fällen zwischen 200 und 500 ms, also immer noch im akzeptablen Bereich. Die Stabilität blieb über mehrere Minuten erhalten, lediglich vereinzelte Validierungsfehler auf Backend-Seite wurden sichtbar. Diese hatten jedoch keinen kritischen Einfluss auf den Testlauf.

![Simulation mit 1 Sensor pro Typ bei 5 Hz](./docs/docs/images/simulation/sim_ein_sensor_5hz.png)
---

### 4) Stresstest – 200 Sensoren je Typ, 5 Hz (≈ 10000 Msgs/s)
Der letzte Testfall sollte die Grenzen des Systems aufzeigen. Dazu wurden pro Sensortyp 200 virtuelle Sensoren erzeugt, die jeweils fünfmal pro Sekunde Nachrichten publizieren. Damit ergab sich eine Gesamtrate von rund 500 Nachrichten pro Sekunde.

Bei dieser hohen Parallelität stieg die Latenz deutlich an. Im Vergleich zu den vorherigen Szenarien waren Nachrichten teilweise erst nach mehreren Sekunden im Backend sichtbar. Zudem traten vermehrt sogenannte Drops auf, d. h. einzelne Nachrichten gingen unterwegs verloren. Das äußerte sich in Lücken innerhalb der Zeitreihen.

Auch die Stabilität war eingeschränkt: Nach kurzer Zeit nahm die Zahl der Fehler im Backend zu, und das Arduino-Board stieß spürbar an seine Leistungsgrenzen. Dieses Verhalten ist jedoch erwartbar, da die Hardware nicht für eine so extreme Last ausgelegt ist. Für Testzwecke ist dieses Szenario dennoch wertvoll, da es aufzeigt, wie sich das System bei stark erhöhter Datenrate verhält und wo mögliche Optimierungspotenziale liegen.

![Stresstest mit 200 Sensoren pro Typ bei 5 Hz](./docs/docs/images/simulation/sim_200_sensoren.png)

---

## Generierte Sensordaten – zusätzliche Testfälle

Neben den Last- und Latenztests wurden auch Szenarien mit **generierten Sensordaten** untersucht. Dabei ging es vor allem um die Frage, wie sich das System verhält, wenn Sensoren **nicht registriert** oder nur **teilweise im Frontend angelegt** werden.

### 1) Keine Sensoren registriert
- Mehrere virtuelle Sensoren erzeugten Daten, ohne dass sie im Frontend sichtbar waren.
- Ergebnis: Die Nachrichten wurden im Backend korrekt verarbeitet und in die Datenbank übernommen, auch ohne vorherige Registrierung.

### 2) Ein Teil der Sensoren im Frontend registriert
- Einige der generierten Sensoren wurden im Frontend angelegt und einem Storage zugewiesen.
- Ergebnis: Die Werte erschienen korrekt im **Dashboard** und in den **Analytics**.

![Dashboard mit Temperatur- und Feuchtigkeitswerten](./docs/docs/images/simulation/dashboard.png)
![Analytics mit KPIs und Min/Max je Sensor](./docs/docs/images/simulation/analytics.png)

### 3) Viele Werte pro Sensor im Sekundentakt
- Jeder Sensor publizierte viele Werte pro Sekunde.
- Ergebnis: Das Backend konnte diese kontinuierlich verarbeiten. Im Frontend wurden die Werte konsistent angezeigt, die Analytics zeigten korrekte Min/Max-Aggregationen.

---
## Zusammenfassung der Ergebnisse

Die durchgeführten Tests haben gezeigt, dass die Plattform in den meisten praxisnahen Szenarien sehr zuverlässig arbeitet.
Im **Normalbetrieb** mit Live-Daten (1 Hz pro Sensor) sowie in der **Simulation mit einzelnen virtuellen Sensoren** bei gleicher Frequenz liegt die End-to-End-Latenz konstant unter **200 ms**. Damit ist eine nahezu verzögerungsfreie Verarbeitung der Messwerte gewährleistet, unabhängig davon, ob die Daten von realer Hardware oder aus der Simulation stammen. Auch über längere Laufzeiten hinweg zeigte sich ein stabiler Durchsatz ohne Ausfälle.

Wird die **Nachrichtenrate erhöht** (5 Hz pro Sensortyp, etwa 25 Nachrichten pro Sekunde insgesamt), bleibt die Plattform weiterhin performant. Die Latenz steigt leicht an, bleibt aber in der Regel deutlich unter **500 ms**. Das bedeutet, dass auch Szenarien mit erhöhter Messfrequenz oder mehr Sensorknoten problemlos verarbeitet werden können. Vereinzelt kam es zu Backend-Validierungsfehlern, diese hatten jedoch keinen Einfluss auf den Gesamtdurchsatz.

Im **Stresstest** mit 200 Sensoren pro Typ und einer Frequenz von 5 Hz (insgesamt etwa 10000 Nachrichten pro Sekunde) wurde schließlich die Belastungsgrenze sichtbar. Die Latenz stieg deutlich an, und es traten erste **Drops** auf, bei denen einzelne Nachrichten nicht mehr verarbeitet wurden. Diese Beobachtung zeigt, dass das aktuelle Setup für hohe Skalierungen angepasst werden müsste, liefert aber wertvolle Erkenntnisse darüber, wo die Plattform heute steht.

Insgesamt bestätigen die Tests, dass das System im Normal- und Hochlastbetrieb robust funktioniert und sich Simulation und reale Daten nahtlos ergänzen. Erst bei extremen Lastszenarien werden klare Grenzen sichtbar, die als Ansatzpunkt für weitere Optimierungen dienen können.

---

## Beispiel‑Konfigurationen

### Simulation (einfach)
```cpp
#define SIM_MODE     1
#define STRESS_MODE  0

#define STRESS_NUM_SENSORS 5
#define STRESS_RATE_HZ     1.0f
```

### Stresstest (moderat)
```cpp
#define SIM_MODE     1
#define STRESS_MODE  1

#define STRESS_NUM_SENSORS 20
#define STRESS_RATE_HZ     5.0f
```

---

## Kurze Tabelle: Szenarien & Befunde

| Szenario | Konfiguration          | Rate (Msgs/s) | Latenz (gemessen) | Stabilität | Hinweis |
|---|------------------------|--------------:|------------------:|---|---|
| Live‑Daten | echte Sensoren         |            ~1 |       **<200 ms** | stabil | einzelne Backend‑„Bad request“ möglich |
| Simulation | 1 Sensor/Typ           |            ~5 |       **<200 ms** | stabil | deckungsgleich mit Live |
| Simulation | 1 Sensor/Typ, 5 Hz     |           ~25 |       **<500 ms** | stabil | erhöhte Rate, keine Drops |
| Stresstest | 200 Sensoren/Typ, 5 Hz |         ~1000 |   deutlich erhöht | Drops | Systemgrenze sichtbar |

---

## Fazit

Im **Normalbetrieb** und bei **moderater Last** verarbeitet die Plattform Daten **nahezu in Echtzeit**. Der **Stresstest** mit hunderten virtuellen Sensoren macht transparent, ab wann Latenz und Verlust ansteigen. Die Simulation ist damit ein wirksames Werkzeug, um ohne Hardware **Funktion, Performance und Skalierbarkeit** konsistent zu prüfen.
