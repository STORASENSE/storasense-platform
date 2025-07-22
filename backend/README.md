# "Modular Monolith" Backend Architecture
## Grundsätzlich (Kriterien)

### Modularisierung
* Module sollten in sich geschlossene, in sich konsistente Einheiten sein - die leicht entfernbar oder austauschbar sind ("plug and play")

### Lose Kopplung
* Module sollten möglichst unabhängig voneinander sein

### Geheimnisprinzip, Abstraktion
* Module sollten möglichst wenig Wissen über andere Module haben
* Module sollten nur **über klar definierte Schnittstellen bzw Abstraktionen miteinander kommunizieren**

### Hohe Konsistenz der Module => Konzeptuelle Integrität
* Module sollten ähnliche Strukturen und Konventionen verwenden (ähnliche Problem ähnlich lösen)

## Pattern / Techniken

### Relevante Prinzipien:
#### SOLID
* Open-Closed Principle (OCP)
* Dependency Inversion Principle (DIP): durchgängig einhalten, zwischen MODULES und zwischen MODULES-SHARED_STUFF
  * ggf. mit Dependency Injection realisiert (Depdency Injector verwaltet die Instanz der abstrakten Klassen)

### Pattern:
#### Adapter Pattern
* Module sollten nur über Adapter auf Shared Stuff zugreifen
* Shared Stuff sollte nur über Adapter auf Module zugreifen
* Module sollten nur über Adapter auf andere Module zugreifen
