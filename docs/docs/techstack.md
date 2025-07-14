# Technologien

## Frontend
Die Anwendung wird als **Webanwendung** umgesetzt, die in einem Browser läuft. <br/>
Dies hat mehrere Vorteile:
* **Plattformunabhängigkeit**: Die Anwendung läuft auf jedem Gerät mit einem modernen Webbrowser, unabhängig vom Betriebssystem (Windows, macOS, Linux, Android, iOS).
* **Einfache Verteilung**: Nutzer müssen keine Software installieren, sondern können die Anwendung direkt über eine URL aufrufen.
* **Zugänglichkeit**: Die Anwendung ist von überall aus zugänglich, solange eine Internetverbindung besteht.
* **Responsive Design**: Die Anwendung kann so gestaltet werden, dass sie auf verschiedenen Bildschirmgrößen (PC, Smartphone) gut aussieht und funktioniert.
* **Zukunftssicherheit**: Webanwendungen sind zukunftssicher, da sie nicht an ein bestimmtes Betriebssystem gebunden sind und sich leicht an neue Technologien anpassen lassen.
* **Einfache Updates**: Updates können zentral auf dem Server durchgeführt werden, ohne dass die Nutzer etwas installieren müssen.

Die Frontend-Entwicklung erfolgt mit dem Framework **React**. <br/>
Dies ergab sich nach dem Vergleich der populärsten Frontend-Frameworks: *React*, *Vue.js* und *Angular* [1] [2] [3] [4].

| Kriterium             | React                                                                                                                    | Vue.js                                                                                                                        | Angular                                                                                                                   |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| Grundkonzept          | Eine flexible UI\-Bibliothek mit einem großen Ökosystem; Baut auf wiederverwendbaren Komponenten auf.                    | Ein leichtgewichtiges Framework, das für seine Einfachheit bekannt ist.                                                       | Ein umfassendes Framework für große, strukturierte Enterprise\-Anwendungen.                                               |
| Performance           | Sehr hoch. Nutzt einen virtuellen DOM für schnelle und effiziente Updates der Benutzeroberfläche.                        | Sehr hoch. Gilt als sehr performant und leichtgewichtig, was zu schnellen Ladezeiten führt.                                   | Gut. Für große Anwendungen optimiert, kann aber durch seine Größe einen höheren Initialaufwand haben.                     |
| Lernkurve             | Mittel. Die Grundlagen sind schnell gelernt, Bestimmte Konzepte wie State\-Management erfordern aber Einarbeitung.       | Niedrig. Gilt als das am einfachsten zu lernende Framework, ideal für Einsteiger und Projekte mit schneller Entwicklungszeit. | Hoch. Erfordert das Verständnis von TypeScript und einer komplexen, festen Architektur.                                   |
| Community & Ökosystem | Sehr groß. Die mit Abstand größte Community, unzählige Tutorials, fertige Lösungen und Tools.                            | Groß. Eine größere Community mit vielen Plugins.                                                                              | Groß. Starker Rückhalt durch Google und eine große Enterprise\-Community.                                                 |
| UI Projekt-Eignung    | Sehr gut. Sehr große Auswahl an spezialisierten Charting\-Bibliotheken \(z\.B\. Recharts, Victory\) und UI\-Komponenten. | Gut. Bietet ebenfalls gute Bibliotheken \(z\.B\. vue\-echarts\) und eine reaktive Datenbindung, die für Dashboards ideal ist. | Gut. Bietet ebenfalls Bibliotheken, die feste Struktur kann aber bei sehr individuellen Visualisierungen hinderlich sein. |

Die Evaluation der Frontend-Frameworks ergab, dass React die beste Wahl für die Anwendung ist. <br/>
Die Vorteile liegen hier vor allem in der Flexibilität und dem riesigen Ökosystem. <br/>
So sind für viele (projektgegebene) Anwendungsfälle fertige Bibliothek gegeben, insbesondere für Datenvisualisierung und Dashboards. <br/>
Die komponentenbasierte Architektur fördert weiter die Wiederverwendbarkeit von Code, sodass z.B. ein Sensor-Widget einmal gebaut und
mehrfach verwendet werden kann.

### Next.js [5]
Für die Umsetzung der Anwendung wird **Next.js** als Framework für React gewählt. <br/>
Next.js ist ein beliebtes Framework, das auf React aufbaut und zusätzliche Funktionen wie Server-Side Rendering (SSR), statische Seitengenerierung (SSG) und API-Routen bietet. <br/>
Dadurch vereinfacht es die Entwicklung von Webanwendungen und bietet eine bessere Performance. <br/>

## Backend
Die Anwendung wird mit der Programmiersprache **Python** entwickelt. <br/>
Hierfür lassen sich insbesondere folgende Vorteile anführen:
* Python ist eine weit verbreitete Sprache, die sich mit seinen Frameworks gut für Webanwendungen eignet.
* Python hat eine große Community und viele Bibliotheken, die die Entwicklung erleichtern.
* Python ist im Team bereits gut bekannt, was die Einarbeitungszeit reduziert.
* Python ermöglicht aufgrund seiner Einfachheit eine schnelle Entwicklung und Anpassung (z.B. spätere Erweiterung) der Anwendung.

Als Framework für den Backend-Teil der Anwendung wird **FastAPI** gewählt.
Dies ergab sich nach dem Vergleich der populärsten Frameworks, die für die Entwicklung von Webanwendungen in Python geeignet sind: *FastAPI*, *Flask* und *Django* [6] [7] [8].

| Kriterium            | FastAPI                                                                                                                                                                                                                                                                                          | Flask                                                                                                                     | Django                                                                                                                                       |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| Grundkonzept         | Modernes, hochperformantes, leichtgewichtiges API-Framework.                                                                                                                                                                                                                                     | Kompaktes Framework, das sich auf das Wesentliche konzentriert.                                                           | Umfassendes, komplexes Full-Stack-Framework für große Webanwendungen.                                                                        |
| Performance          | Sehr gut. Eines der schnellsten Python-Frameworks, da es auf Starlette und Pydantic basiert. Zudem arbeitet es asynchron.                                                                                                                                                                        | Gut. Als Micro-Framework sehr schlank, die Gesamtperformance hängt aber stark von den gewählten Erweiterungen ab.         | Gut. Für Webanwendungen sehr performant, aber möglicherweise erst nach umfassender Konfiguration bzw Optimierung.                            |
| Erweiterbarkeit      | Sehr gut. Das moderne Design und die automatische API-Dokumentation (Swagger) erleichtern die Anbindung neuer Module und externer Dienste.                                                                                                                                                       | Sehr gut. Das ist die Kernstärke von Flask - modular bindet man nur das ein, was man braucht und hat die volle Kontrolle. | Gut. Besitzt ein ausgereiftes App-Konzept - die feste Struktur kann die Flexibilität und Schnelligkeit in der Entwicklung aber einschränken. |
| Lernkurve            | Niedrig/Mittel. Die Grundlagen sind schnell gelernt, die asynchrone Programmierung erfordert (ohne Vorwissen) Einarbeitung.                                                                                                                                                                      | Niedrig. Gilt als das am einfachsten zu lernende Framework, ideal für Einsteiger und kleinere Projekte.                   | Hoch. Die Fülle an integrierten Konzepten und Features erfordert eine längere Einarbeitungszeit.                                             |
| Integrierte Features | Wenige. Fokussiert auf API-Erstellung, Datenvalidierung und Dokumentation. Alles Weitere wird flexibel mit Bibliotheken ergänzt.                                                                                                                                                                 | Sehr wenige. Bringt nur einen Webserver und Routing mit. Datenbanken, Nutzerverwaltung etc. müssen selbst gewählt werden. | Sehr viele. Integrierter ORM (Datenbankzugriff), Nutzerverwaltung, Admin-Oberfläche, Sicherheitsfunktionen etc..                             |
| IoT-Kompatibilität   | Sehr gut. Nativ asynchron und so somit sehr gut für die parallele Verarbeitung vieler Sensor-Daten und Echtzeit-Kommunikation geeignet. <br/>Ein MQTT-Client, der permanent auf Nachrichten wartet, läuft so reibungslos ohne den Anwendungs-Worker (bspw. Anfragen vom Frontend) zu blockieren. | Gut. Benötigt Erweiterungen (z.B. Flask-SocketIO), ist aber gut anpassbar.                       | Gut. Asynchronität wird über eine zusätzliche Schicht ("Django Channels") realisiert und ist nicht im Kern verankert.                        |

Die Evaluation der Backend-Frameworks ergab, dass FastAPI die beste Wahl für die Anwendung ist. <br/>
Zum einen ist FastAPI leichtgewichtig, performant und basiert nativ auf einer sehr asynchronen Architektur, die für die parallele Verarbeitung von IoT-Daten bzw MQTT-Nachrichten, aber auch für die Bedienung eines Frontends, geeignet ist.
So kann die Anwendung verschiedene Aufgaben gleichzeitig und ohne Blockierung der Anwendungs-Worker erledigen. <br/>
Zum anderen ist FastAPI sehr gut erweiterbar, was die Anbindung neuer Module erleichtert. <br/>
Die automatisch generierte API-Dokumentation (über Swagger) beschleunigt weiter die Entwicklung und verbessert die Wartbarkeit der Anwendung.

### MQTT-Client
Die Anbindung eines MQTT-Clients zur Kommunikation mit der Hardware lässt sich in FastAPI gut umsetzen. <br/>
Durch das asynchrone Kernkonzept kann der MQTT-Client nahtlos im Event-Loop der Anwendung mitlaufen und permanent auf Nachrichten lauschen, ohne die Performance des restlichen Systems zu beeinträchtigen. <br/>
Als MQTT-Client lässt sich so die Bibliothek **fastapi-mqtt** [9] verwenden, die eine einfache Integration in FastAPI ermöglicht.

### Frontend-Integration
Hinsichtlich der Frontend-Kompatibilität ist FastAPI für eine entkoppelte Architektur ausgelegt. <br/>
Es fungiert als reine API-Schnittstelle und kann mit jedem modernen (JavaScript-)Framework wie React kommunizieren. <br/>
Dies ermöglicht eine klare Trennung zwischen der Benutzeroberfläche und der Logik im Backend, was die Entwicklung (und Skalierbarkeit) des Gesamtsystems vereinfacht.


Quellen:
* [1] https://roadmap.sh/frontend/frameworks
* [2] https://7span.com/blog/angular-vs-react-vs-vue
* [3] https://content.techgig.com/web-stories/react-vs-vue-vs-angular-which-one-to-choose-in-2025/web_stories/118657485.cms
* [4] https://www.octalsoftware.com/blog/best-front-end-frameworks
* [5] https://kinsta.com/blog/nextjs-vs-react/
* [6]https://www.geeksforgeeks.org/python/comparison-of-fastapi-with-django-and-flask/
* [7] https://blog.jetbrains.com/pycharm/2025/02/django-flask-fastapi/
* [8] https://dev.to/leapcell/top-10-python-web-frameworks-compared-3o82
* [9] https://sabuhish.github.io/fastapi-mqtt/
