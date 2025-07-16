# MVP – Überwachungssystem für Temperatur und Luftfeuchtigkeit

## Ziel des MVP

Ziel dieses Minimal Viable Products (MVP) ist die Entwicklung eines einfachen, funktionalen Systems zur Erfassung und Überwachung von Umweltdaten – konkret Temperatur und Luftfeuchtigkeit – über Sensoren, deren Messwerte gespeichert, ausgewertet und überwacht werden. Das System dient als Grundlage für eine spätere Erweiterung mit zusätzlichen Sensoren und Benachrichtigungsmechanismen.

## Systemüberblick

Das System basiert auf einer Hardwarekomponente (z. B. Arduino mit angeschlossenen Sensoren), welche die gemessenen Umweltdaten regelmäßig über das MQTT-Protokoll an einen Server übermittelt. Die Kommunikation zwischen Sensorgerät und MQTT-Server ist passwortgeschützt, um die Integrität und Sicherheit der übertragenen Daten zu gewährleisten.

Die empfangenen Messwerte werden in einer permanenten Datenbank gespeichert und über eine grafische Benutzeroberfläche visualisiert. Darüber hinaus kann der Benutzer individuelle Schwellenwerte für Temperatur definieren. Wird ein definierter Temperaturbereich überschritten oder unterschritten, so wird automatisch eine Warnung ausgegeben und an den MQTT-Broker gesendet. Bei Grenzwertüberschreitungen wird zudem ein neues MQTT-Topic veröffentlicht, das von anderen Komponenten abonniert werden kann, um z. B. automatisierte Reaktionen auszulösen.

## Funktionale Anforderungen

- Das System misst regelmäßig die **Temperatur** und **Luftfeuchtigkeit** über angeschlossene Sensoren.
- Die Messergebnisse werden in einer **permanenten Datenbank** gespeichert.
- Der Benutzer kann über eine **grafische Benutzeroberfläche** einen **Temperatur-Mindestwert** und einen **Temperatur-Höchstwert** definieren.
- Liegt die gemessene Temperatur **außerhalb des definierten Bereichs**, wird automatisch eine **Warnung** erzeugt.
- Die Warnung wird über den **MQTT-Broker** veröffentlicht.
- Bei einer Grenzwertverletzung wird ein neues **MQTT-Topic** erstellt, auf das andere Systeme oder Komponenten zugreifen können (z. B. zur Steuerung von Aktoren).
- Die Benutzeroberfläche stellt ein **aktives Dashboard** dar, das die aktuellen Sensordaten in Echtzeit visualisiert.

## Nicht-funktionale Anforderungen

- Die **Verfügbarkeit des Systems** soll mindestens **99 % innerhalb eines Zeitraums von drei Tagen** betragen.
- Die Kommunikation zwischen Sensor und Server erfolgt **passwortgeschützt**, um unbefugten Zugriff zu verhindern.
- Das System soll modular aufgebaut sein, um spätere Erweiterungen zu ermöglichen.

## Optionale Erweiterungen

Die folgenden Funktionen sind nicht Bestandteil des MVPs, können jedoch zu einem späteren Zeitpunkt ergänzt werden:

- **Sensor zur Erkennung von Kohlenwasserstoffen** zur Überwachung der Luftqualität
- **Ultraschallsensor zur Türüberwachung**, z. B. zur Anwesenheitserkennung oder Zutrittskontrolle
- **Benachrichtigung per Push-Nachricht** bei Grenzwertüberschreitungen oder anderen definierten Ereignissen

## Hinweise

Da es sich um ein MVP handelt, liegt der Fokus zunächst auf der Umsetzung der Kernfunktionen (Datenaufnahme, Speicherung, Warnung). Erweiterte Funktionalitäten, Sicherheit auf Anwendungsebene sowie Skalierbarkeit sind nicht Bestandteil des ersten Releases, können aber im Rahmen weiterer Iterationen realisiert werden.
