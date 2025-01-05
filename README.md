# W∞dii Live-Dashboard

Ein interaktives Dashboard zur Anzeige von Echtzeit-Messwerten wie Temperatur, CO2-Gehalt, Luftfeuchtigkeit, Lautstärke und mehr. Das Dashboard wird regelmäßig aktualisiert und bietet eine visuelle Darstellung der Messdaten in Form von Diagrammen und Tabellen.


## Inhaltsverzeichnis

- [Projektbeschreibung](#projektbeschreibung)
- [Funktionen](#funktionen)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Datenquellen](#datenquellen)
- [Verzögerungen und Fehlerbehandlung](#verzögerungen-und-fehlerbehandlung)
- [Lizenz](#lizenz)

## Projektbeschreibung

Dieses Dashboard wurde entwickelt, um eine benutzerfreundliche Anzeige von Umwelt- und Messdaten in Echtzeit zu ermöglichen. Es visualisiert Daten wie Lufttemperatur, CO2-Gehalt, Luftfeuchtigkeit und andere relevante Messwerte in einem ansprechenden Design. Es wird regelmäßig aktualisiert, sodass die angezeigten Werte immer auf dem neuesten Stand sind.

## Funktionen

- **Echtzeit-Datenanzeige**: Zeigt aktuelle Messwerte (z.B. Temperatur, CO2-Gehalt, Luftfeuchtigkeit) an.
- **QR-Code**: Ein QR-Code, der alle 60 Sekunden aktualisiert wird.
- **Grafische Darstellung**: Zwei Diagramme (Linie und Oberfläche) zur Visualisierung der Daten.
- **Historische Daten**: Zeigt historische Messdaten in einer Tabelle an.
- **Regelmäßige Aktualisierungen**: Daten werden alle 1–5 Minuten aktualisiert, abhängig von der Art der Information.

## Installation

### Voraussetzungen
- Python 3.7 oder höher
- Die folgenden Python-Bibliotheken müssen installiert werden:
  - `dash`
  - `plotly`
  - `pandas`
  - `time`
  - `datetime`

### Schritt-für-Schritt-Anleitung

1. **Projekt klonen**:
    ```bash
    git clone https://github.com/DEIN_USERNAMEN/Woodii-Live-Dashboard.git
    cd Woodii-Live-Dashboard
    ```

2. **Abhängigkeiten installieren**:
    Stelle sicher, dass du die Abhängigkeiten mit `pip` installierst:
    ```bash
    pip install -r requirements.txt
    ```

3. **Dashboard starten**:
    Starte das Dashboard mit dem folgenden Befehl:
    ```bash
    python app.py
    ```
    Das Dashboard wird nun auf `http://127.0.0.1:8080` verfügbar sein.

## Verwendung

- Sobald das Dashboard läuft, kannst du es im Webbrowser öffnen.
- Die Seite zeigt in Echtzeit verschiedene Messwerte an, die regelmäßig aktualisiert werden.
- Die Daten werden aus lokalen JSON-Dateien geladen, die regelmäßig aktualisiert werden.

### Funktionen im Dashboard:

1. **Aktueller Zeitstempel**:
   - Zeigt die aktuelle Uhrzeit an, die jede Sekunde aktualisiert wird.

2. **Messwerte**:
   - Zeigt Messwerte wie Temperatur, CO2-Gehalt, Luftfeuchtigkeit, Lautstärke und Luftdruck an. Diese Werte werden jede Minute aktualisiert.

3. **QR-Code**:
   - Ein QR-Code, der regelmäßig aktualisiert wird. Scanne ihn, um auf eine andere Seite weitergeleitet zu werden.

4. **Diagramme**:
   - Zwei Diagramme, die die Messdaten visuell darstellen. Diese Diagramme werden alle 5 Minuten aktualisiert.

5. **Tabelle**:
   - Zeigt eine Tabelle mit historischen Messwerten, die alle 60 Sekunden aktualisiert wird.

## Datenquellen

Die Daten für das Dashboard werden aus lokalen JSON-Dateien geladen, die regelmäßig aktualisiert werden. Die Dateien enthalten Messwerte zu verschiedenen Umweltparametern, die für die Anzeige im Dashboard genutzt werden. Diese JSON-Dateien befinden sich im Ordner `assets/`.

- **Aktuelle Messwerte**: `assets/CurrentData.json`
- **Historische Messwerte**: `assets/DataDescription.json`
- **Diagrammdaten (Linie und Oberfläche)**: `assets/LinePlot.json` und `assets/SurfacePlot.json`

## Verzögerungen und Fehlerbehandlung

- **Verzögerungen bei der Aktualisierung**: Es kann zu kleinen Verzögerungen bei der Datenaktualisierung kommen, wenn die Anwendung auf die neuesten Daten wartet. Dies passiert aufgrund der Lesevorgänge von lokalen JSON-Dateien.
- **Fehlerbehandlung**: Falls Daten nicht sofort verfügbar sind, versucht die Anwendung weiterhin, sie zu laden, ohne dass sie abstürzt. Dies gewährleistet, dass das Dashboard stabil bleibt, auch wenn es Probleme beim Laden der Daten gibt.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert – siehe die [LICENSE](LICENSE)-Datei für Details.
