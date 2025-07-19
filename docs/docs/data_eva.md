# Datendomäne

## Datenmodellierung
Vor der Auswahl einer spezifischen Datenbanktechnologie wird das fachliche Datenmodell definiert, das alle für das Überwachungssystem relevanten Informationen und deren Beziehungen
zueinander abbildet.
Das Modell basiert auf drei zentralen Entitäten:

* Lagerort: Repräsentiert einen physischen Ort (z.B. "Weinkeller A", "Lagerhalle B"), der überwacht wird. Jeder Lagerort besitzt eindeutige Attribute wie eine ID und einen Namen.

* Benutzer: Stellt eine Person dar, die mit dem System interagiert. Ein Benutzer hat Attribute wie einen Benutzernamen, ein Passwort und eine zugewiesene Rolle (z.B. "Admin", "User"), die seine Berechtigungen bestimmt.

* Messwert: Repräsentiert eine einzelne, zu einem exakten Zeitpunkt erfasste Messung (z.B. Temperatur, Luftfeuchtigkeit). Jeder Messwert ist immer genau einem Lagerort zugeordnet.

##
