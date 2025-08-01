# Shared-Logging

## 1. Überblick & Log-Level
`configure_logging()` initialisiert den Root-Logger zentral:

- **LOG_LEVEL** steuerbar über Umgebungsvariable `LOG_LEVEL` (Standard: `INFO`)
- Meldungen **unter** `ERROR` (`INFO` & `WARNING`) → **stdout**
- Meldungen **ab** `ERROR` → **stderr**
- **RotatingFileHandler** rotiert die Logdatei (`app.log`) nach konfigurierbarer Größe und behält bis zu fünf Backups

```
export LOG_LEVEL=DEBUG
export LOG_FILE=myapp.log
export LOG_MAX_BYTES=5242880      # 5 MB
export LOG_BACKUP_COUNT=3
```

## 2. Strukturierte Logs (JSON)

Alle Log-Einträge werden über **structlog** als JSON ausgegeben. Automatisch ergänzt um:

- `timestamp` (ISO-Format)
- `level` (INFO, WARNING, ERROR, …)
- benannte Felder wie `event`, `method`, `path`, `duration`

**Beispiel:**

```json
{
  "event": "http_request",
  "method": "GET",
  "path": "/users",
  "status_code": 200,
  "duration": "0.0045s",
  "level": "info",
  "timestamp": "2025-07-31T14:35:22.123Z"
}
```

## 3. HTTP-Request-Middleware

Die Funktion `add_request_middleware(app: FastAPI)` bindet eine Middleware ein, die bei **jedem** Request automatisch loggt:

```python
from shared.logging import add_request_middleware
from fastapi import FastAPI

app = FastAPI()
add_request_middleware(app)
```
### Geloggte Felder pro Request

- **HTTP-Methode** (`request.method`)
- **Pfad** (`request.url.path`)
- **Status-Code** (`response.status_code`)
- **Dauer** (`duration` in Sekunden)

## 4. Schnellstart (Inbetriebnahme)

Damit dein Shared-Logging sofort aktiv ist, führst du diese Schritte in deinem Hauptskript (z.B. `main.py` oder `app.py`) aus:

```python
from fastapi import FastAPI
from shared.logging import configure_logging, add_request_middleware, get_logger

# 1) Globale Logging-Konfiguration aktivieren
configure_logging()

# 2) FastAPI-Anwendung erstellen
app = FastAPI()

# 3) Request-Middleware anhängen (automatisches Protokollieren aller HTTP-Requests)
add_request_middleware(app)

# 4) Logger für dieses Modul holen und einen Start-Eintrag schreiben
logger = get_logger(__name__)
logger.info("Application startup complete")
```
### Erklärung der Schritte

1. **configure_logging()**
   Initialisiert die zentralen Logging-Handler (Konsole, Datei, optional ELK) und stellt das JSON-Format über structlog bereit.

2. **FastAPI()**
   Erstellt die Instanz der FastAPI-Anwendung, an welche die Middleware angebunden wird.

3. **add_request_middleware(app)**
   Registriert eine Middleware, die bei jeder Anfrage automatisch HTTP-Methode, Pfad, Statuscode und Bearbeitungsdauer in das Log schreibt.

4. **get_logger(__name__)**
   Stellt einen strukturierten Logger für das aktuelle Modul bereit. Damit können anwendungsweit konsistente Log-Einträge (z.B. mittels `logger.info(...)`) erzeugt werden.
