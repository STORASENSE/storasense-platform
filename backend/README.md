# "Modular Monolith" Backend Architecture
## Grundsätzlich (Kriterien)

### Modularisierung (Separation of Concerns)
* Backend-System wird in sich geschlossene Bausteine zerlegt, die jeweils eine bestimmte Funktionalität bereitstellen (Serparation of Concerns)
* Module sollten in sich geschlossene, in sich konsistente Einheiten sein - die leicht entfernbar oder austauschbar sind ("plug and play")

### Lose Kopplung
* Module sollten möglichst unabhängig voneinander sein

### Geheimnisprinzip, Abstraktion
* Module sollten möglichst wenig Wissen über andere Module haben
* Module sollten nur **über klar definierte Schnittstellen bzw Abstraktionen miteinander kommunizieren**

### Hohe Konsistenz der Module => Konzeptuelle Integrität
* Module sollten ähnliche Strukturen und Konventionen verwenden (ähnliche Problem ähnlich lösen)

## Pattern / Techniken

### Principles:
#### SOLID: Open-Closed Principle (OCP)
#### SOLID: Dependency Inversion Principle (DIP)
* durchgängig einhalten, zwischen MODULES und zwischen MODULES-SHARED_STUFF
* ggf. mit Dependency Injection realisiert (Depdency Injector verwaltet die Instanz der abstrakten Klassen)

### Pattern (Principles, Kriterien umsetzen): Hexagonal Pattern (Ports, Adapter)
* Module sollten nur über Adapter auf Shared Stuff zugreifen
* Module sollten nur über Adapter auf andere Module zugreifen

* https://blog.artisivf.com/2024/08/29/how-to-build-a-modular-monolith-with-hexagonal-architecture/
