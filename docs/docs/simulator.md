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
