## Watchdog-Integration

Zur Absicherung des Systems gegen dauerhafte Verbindungsprobleme wurde ein Hardware-Watchdog implementiert. Dieser stellt sicher, dass das System in einem definierten Zeitraum automatisch neu startet, wenn eine Wiederverbindung zum MQTT-Broker nicht gelingt. Diese Funktionalität ist besonders wichtig für produktive Anwendungen mit dauerhafter Datenübertragung, wie im MVP vorgesehen.

### Anforderungen

Im MVP war festgelegt, dass das Gerät sich nach einem Verbindungsverlust innerhalb von **30 Sekunden** wieder mit dem MQTT-Broker verbinden soll. Gelingt dies nicht innerhalb von **3 Versuchen**, muss ein automatischer Neustart erfolgen – idealerweise innerhalb von **20 Sekunden nach letztem Versuch**.
Diese Anforderungen wurden durch folgende Mechanismen erfüllt:

- **Reconnect-Logik** mit Zähler und Zeitfenster
- **Hardware-Watchdog**, der den Neustart auslöst, falls der Code „hängt“

### Vergleich alternativer Watchdog-Bibliotheken

Für SAMD21-kompatible Boards existieren mehrere Watchdog-Bibliotheken:

| Bibliothek        | Hardwarebasiert | Einfachheit | Max. Timeout | Verbreitung |
|------------------|-------------|---------|---------------|---------|
| `WDTZero`         | Ja          | Hoch    | 8 s           | Häufig  |
| `Sodaq_wdt`       | Ja          | Mittel | 8 s |️ Weniger verbreitet |
| `WDT_SAMD21`      | Ja          | Mittel | 16 s           |️ Selten |
| Software-Timer    | Nein        | Hoch    |️ frei wählbar | Häufig  |

Die Entscheidung fiel auf **WDTZero**, da sie:

- speziell für den verwendeten Mikrocontroller (MKR WiFi 1010, SAMD21) entwickelt wurde,
- eine saubere Trennung von Setup und Reset bietet,
- in der Community erprobt ist (GitHub und Arduino Forum),

### Implementierung

Für die Implementierung wurde die Bibliothek `WDTZero` verwendet. Diese bietet direkten Zugriff auf den Watchdog-Timer von SAMD21-basierten Boards und ist damit zuverlässiger als reine Softwarelösungen. Im Setup wird der Watchdog mit einem Timeout von 8 Sekunden aktiviert:

```cpp
#include <WDTZero.h>

WDTZero wdt;

void setup() {
    wdt.setup(WDT_SOFTCYCLE8S);  // Timeout auf 8 Sekunden setzen
    wdt.enable();
}
```

Im `loop()`-Block wird der Watchdog regelmäßig „gefüttert“ (reset), solange das System erwartungsgemäß funktioniert:

```cpp
wdt.reset();
```

Sobald alle Reconnect-Versuche aufgebraucht sind, wird kein `reset()` mehr ausgeführt. Der Watchdog erkennt das als Hängen des Systems und löst einen Neustart aus.

### Reconnect-Logik

Die Wiederverbindung erfolgt durch eine einfache Retry-Schleife:

```cpp
if (!mqttClient.connected()) {
    if (reconnectAttempts < 3) {
        connectToMQTT();  // Bei Erfolg wird wdt.reset() aufgerufen
        reconnectAttempts++;
    } else {
        // Keine weiteren Versuche → kein reset()
    }
}
```

Nach jedem erfolgreichen Verbindungsaufbau wird der Zähler zurückgesetzt. Bleibt die Verbindung über mehrere Intervalle hinweg bestehen, bleibt der Watchdog aktiv, aber ungefährlich – solange `reset()` regelmäßig erfolgt.

---

### Quellen

- [1] [WDTZero GitHub](https://github.com/javos65/WDTZero)
- [2] [Sodaq_Watchdog Github](https://github.com/SodaqMoja/Sodaq_wdt)
- [3] [WDT_SAMD21 GitHub (Alternative)](https://github.com/gpb01/wdt_samd21)
