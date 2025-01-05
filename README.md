# W∞d.ii Live-Dashboard

Ein interaktives Dashboard zur Anzeige von Echtzeit-Messwerten wie Temperatur, CO2-Gehalt, Luftfeuchtigkeit, Lautstärke und mehr. 
Das Dashboard wird regelmäßig aktualisiert und bietet eine visuelle Darstellung der Messdaten in Form von Diagrammen und Tabellen.

![Screenshot 2025-01-05 141634](https://github.com/user-attachments/assets/6170a756-0e98-4323-8a20-1857902c2936)


## Inhaltsverzeichnis

- [Projektbeschreibung](#projektbeschreibung)
- [Setup](#setup)
- [Verwendung](#verwendung)
- [Features im Dashboard](#features-im-dashboard)

## Projektbeschreibung

Dieses Projekt wurde in Kooperation zwischen [WoodenValley](https://woodenvalley.de/), [Rysta](https://www.rysta.de/) und der [Hochschule Esslingen](https://www.hs-esslingen.de/) durchgeführt.

Ziele der Projektarbeit:
- **Datenexport**: Herunterladen von Messwerten des Umgebungssensors Rysta Protect über die [Rysta API](https://rysta-api.com/docs).
- **Künstliche Intelligenz**: KI-Prognose zukünftiger CO2-Werte der Raumluft.
- **Dashboard**: Grafische Darstellungen der Messwerte, Prognose und historischen Daten.
- **Automatisierung**: Automatische Aktualisierung der Daten über [Node-RED](https://nodered.org/) Workflows

## Setup

### Voraussetzungen
- `Python 3.12` oder höher
- `Raspberry Pi 3` oder neuer (`64 Bit` Betriebssystem benötigt)

### Schritt-für-Schritt-Anleitung

1. **Projekt klonen**:
    ```bash
    git clone https://github.com/AntonValentinKress/WoodenValley-DASHBoard.git
    cd WoodenValley-DASHBoard
    ```
    oder als `.zip` herunterladen/extrahieren.

2. **Virtuelle Umgebung erstellen und aktivieren**
    ```bash
    python -m venv venv
    ./venv/source/activate
    ```
    falls Fehler auftreten den jeweiligen Aktivierungsbefehl des verwendeten Betriebssystems prüfen.

3. **Abhängigkeiten installieren**:
    Stelle sicher, dass du die Abhängigkeiten mit `pip` installierst und das `venv` aktiviert ist:
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Node-RED installieren**:
    [Installationsanleitung](https://nodered.org/docs/getting-started/) für das jeweilige Betriebssystem folgen.
    Raspberry Pi wird dringend empfohlen! Falls andere Plattformen gewählt wurden müssen evtl. kleine Anpassungen im Code und Node-RED Workflow vorgenommen werden.
    Stelle sicher das Node-RED beim starten des Raspberry Pi (oder alternativen Plattform) automatisch gestartet wird.

5. **Nutzerdaten hinterlegen**:
    Die Datei `rystavariables.py` in einem Editor öffnen und [`device`](## "Device ID des Rysta Protect Sensors"), [`email`](## "E-Mail Adresse des Rysta Kontos unter welchem der Rysta Sensor registriert ist") und [`password`](## "Passwort des Rysta Kontos")

6. **Node-RED Workflow importieren und starten**:
    Inhalt der Workflow Vorlage `Node-RED-DASHBoard-Template.json` kopieren und in [Node-RED importieren](https://nodered.org/docs/user-guide/editor/workspace/import-export).

## Verwendung
Vorrausgesetzt das Setup wurde korrekt durchgeführt kann das Dashboard nun geöffnet werden.

> [!WARNING]
> Das Dashboard kann nur innerhalb des gleichen WLAN Netzwerkes geöffnet werden, in dem auch der Raspberry Pi (oder Alternative) registriert ist.

Benötigt wird:
- `IPv4` des Raspberry Pi (oder Alternative)
- `Port` des Dashboards, welcher unter 'rystavariables.py' definiert wurde (Standard: 8080)

Das Dashboard kann damit über jeden Browser aufgerufen werden. Gib dafür die `IPv4-Adresse` und `Port` und die Suchleiste ein.

```url
http://127.0.0.1:8080
```
`IPv4` und `Port` müssen entsprechend der jeweiligen Konfiguration angepasst werden!

### Features im Dashboard:

1. **Diagramm: CO2-Prognose**:
<img src="https://github.com/user-attachments/assets/e1ef9260-ee64-4ddc-b8a1-018cabf06a2c" width="400" />

Liniendiagramm mit CO2-Messwerten der letzten Stunden. KI-Modell erstellt eine Vorhersage von kommenden CO2-Werten im Raum über die kommende Stunde.

2. **Diagramm: Historische Messwerte**:
<img src="https://github.com/user-attachments/assets/3030e207-935e-41ca-814a-cf2a191644d0" width="400" />

Oberflächendiagramm welches alle Historische Messwerte pro Tag/Stunde/Messwert darstellt. (X-Achse: Tag; Y-Achse: Stunde; Z-Achse: Messwert). Über das Dropdown Menü kann zwischen den verschiedenen Messwerten gewechselt werden.

3. **Tabelle: Aktuelle Messwerte**:
<img src="https://github.com/user-attachments/assets/1b9c7d97-b2b9-47f8-b92e-a42952411dc1" width="400" />

Darstellung der aktuellsten Messwerte als Tabelle. Die Messwerte werden eingestuft und Handlungsempfehlungen an den Bewohner des Raumes ausgegeben (z.B: Lüften wenn CO2-Werte hoch sind).

4. **Tabelle: Historische Messwerte**:
<img src="https://github.com/user-attachments/assets/41c86aab-79f8-4b31-b23c-e4c686974884" width="400" />

Darstellung von Durchschnitt/Maximum und Minimum der verschiedenen Messwerte über den gesamten heruntergeladenen Zeitraum 

5. **Zeitstempel**:
<img src="https://github.com/user-attachments/assets/f6388b8e-629b-4557-8df9-b54179c08a7a" width="400" />

Unter der Überschrift wird die aktuelle Uhrzeit als Zeitstempel im Format 'DD.MM.YYYY HH:MM:SS' dargestellt. 

6. **QR-Code**:
<img src="https://github.com/user-attachments/assets/ce93eeeb-2c03-4088-90eb-ad879353b85b" width="200" />

In der Überschrift wird ein QR-Code angezeigt, welcher direkt auf das Dashboard verlinkt. Das Dashboard ist nicht für Smartphones geschaffen (Diagramme werden zu klein dargestellt). Es wird mindestens ein Tablet als anzeigendes Gerät empfohlen.
