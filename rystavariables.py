""" Diese Datei enthält die für die Arbeit mit dem Rysta Sensor benötigten Variablen.
"""

""" Nutzerdaten """
device = "your_device_id"
email = "your-awesome-email@xyz.com"
password = "your_secure_password"

""" Zeitspanne an heruntergeladenen Daten (ab heute).
    Daten werden von KI auf Minutenbasis benötigt. Wenn hier nicht "min" wird Qualität der KI beeinträchtigt!
"""
count_of_days = 30
reg = "min"


""" Bezeichnungen der Messwerte. 
    Evtl. müssen Programme mehrfach gestartet werden bis Änderungen überall greifen. 
"""
tst = "Zeitstempel"
mt6 = "Lufttemperatur"
mb0 = "Helligkeit"
mc1 = "CO2-Gehalt"
mh6 = "Luftfeuchtigkeit"
ml0 = "Lautstärke"
mp0 = "Luftdruck"

""" Dashboard Parameter 
    Legt Port und Debug Modus des Dashboards fest.
"""
debug = True
port = 8080

""" Zeitspanne an historischen Messwerten (Minuten) 
    Legt fest wie viele Datenpunkte im Liniendiagramm angezeigt werden.
"""
past_minutes_shown = 300